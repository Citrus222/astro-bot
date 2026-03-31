# handlers/compatibility.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database as db
import ai
from config import FREE_REQUESTS

router = Router()

ZODIAC_SIGNS = {
“♈ Овен”: “Овен”, “♉ Телець”: “Телець”, “♊ Близнюки”: “Близнюки”,
“♋ Рак”: “Рак”, “♌ Лев”: “Лев”, “♍ Діва”: “Діва”,
“♎ Терези”: “Терези”, “♏ Скорпіон”: “Скорпіон”, “♐ Стрілець”: “Стрілець”,
“♑ Козеріг”: “Козеріг”, “♒ Водолій”: “Водолій”, “♓ Риби”: “Риби”
}

def zodiac_keyboard(prefix):
builder = InlineKeyboardBuilder()
for label, val in ZODIAC_SIGNS.items():
builder.button(text=label, callback_data=f”{prefix}_{val}”)
builder.button(text=“◀️ Назад”, callback_data=“menu”)
builder.adjust(3, 3, 3, 3, 1)
return builder.as_markup()

def back_keyboard():
builder = InlineKeyboardBuilder()
builder.button(text=“💑 Ще перевірка”, callback_data=“compatibility”)
builder.button(text=“◀️ Меню”, callback_data=“menu”)
builder.adjust(2)
return builder.as_markup()

def check_limit(user_id):
if db.is_premium(user_id):
return True
return db.get_requests_count(user_id) < FREE_REQUESTS

@router.callback_query(F.data == “compatibility”)
async def compat_start(callback: CallbackQuery):
if not check_limit(callback.from_user.id):
builder = InlineKeyboardBuilder()
builder.button(text=“💳 Підписка”, callback_data=“subscription”)
builder.button(text=“◀️ Меню”, callback_data=“menu”)
builder.adjust(1)
await callback.message.edit_text(
“😔 *Безкоштовні запити вичерпано*\n\nОформи підписку — лише *4.99€/міс*”,
parse_mode=“Markdown”, reply_markup=builder.as_markup()
)
return
await callback.message.edit_text(
“💑 *Сумісність*\n\n*Крок 1:* Обери свій знак:”,
parse_mode=“Markdown”, reply_markup=zodiac_keyboard(“compat1”)
)

@router.callback_query(F.data.startswith(“compat1_”))
async def compat_sign1(callback: CallbackQuery, state: FSMContext):
sign1 = callback.data.replace(“compat1_”, “”)
await state.update_data(sign1=sign1)
await callback.message.edit_text(
f”💑 Твій знак: *{sign1}* ✅\n\n*Крок 2:* Обери знак партнера:”,
parse_mode=“Markdown”, reply_markup=zodiac_keyboard(“compat2”)
)

@router.callback_query(F.data.startswith(“compat2_”))
async def compat_generate(callback: CallbackQuery, state: FSMContext):
sign2 = callback.data.replace(“compat2_”, “”)
data = await state.get_data()
sign1 = data.get(“sign1”, “невідомий”)
await state.clear()
await callback.message.edit_text(f”💑 Аналізую {sign1} і {sign2}… ✨”)
try:
result = await ai.get_compatibility(sign1, sign2)
db.increment_requests(callback.from_user.id)
await callback.message.edit_text(
f”💑 *{sign1} & {sign2}*\n\n{result}”,
parse_mode=“Markdown”, reply_markup=back_keyboard()
)
except Exception:
await callback.message.edit_text(“❌ Помилка. Спробуй ще раз.”, reply_markup=back_keyboard())
