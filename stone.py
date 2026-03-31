# handlers/stone.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
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

def zodiac_keyboard():
builder = InlineKeyboardBuilder()
for label, val in ZODIAC_SIGNS.items():
builder.button(text=label, callback_data=f”stone_{val}”)
builder.button(text=“◀️ Назад”, callback_data=“menu”)
builder.adjust(3, 3, 3, 3, 1)
return builder.as_markup()

def back_keyboard():
builder = InlineKeyboardBuilder()
builder.button(text=“💎 Ще камінь”, callback_data=“stone”)
builder.button(text=“◀️ Меню”, callback_data=“menu”)
builder.adjust(2)
return builder.as_markup()

def check_limit(user_id):
if db.is_premium(user_id):
return True
return db.get_requests_count(user_id) < FREE_REQUESTS

@router.callback_query(F.data == “stone”)
async def stone_start(callback: CallbackQuery):
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
“💎 *Лунний камінь*\n\nОбери свій знак зодіаку:”,
parse_mode=“Markdown”, reply_markup=zodiac_keyboard()
)

@router.callback_query(F.data.startswith(“stone_”))
async def stone_generate(callback: CallbackQuery):
sign = callback.data.replace(“stone_”, “”)
await callback.message.edit_text(“💎 Шукаю твій камінь… ✨”)
try:
result = await ai.get_moon_stone(sign)
db.increment_requests(callback.from_user.id)
await callback.message.edit_text(
f”💎 *Лунний камінь — {sign}*\n\n{result}”,
parse_mode=“Markdown”, reply_markup=back_keyboard()
)
except Exception:
await callback.message.edit_text(“❌ Помилка. Спробуй ще раз.”, reply_markup=back_keyboard())
