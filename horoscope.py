# handlers/horoscope.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
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

class HoroscopeState(StatesGroup):
waiting_birthdate = State()
waiting_sign = State()

def zodiac_keyboard():
builder = InlineKeyboardBuilder()
for label in ZODIAC_SIGNS:
builder.button(text=label, callback_data=f”sign_{ZODIAC_SIGNS[label]}”)
builder.button(text=“◀️ Назад”, callback_data=“menu”)
builder.adjust(3, 3, 3, 3, 1)
return builder.as_markup()

def back_keyboard():
builder = InlineKeyboardBuilder()
builder.button(text=“🔄 Ще раз”, callback_data=“horoscope”)
builder.button(text=“◀️ Меню”, callback_data=“menu”)
builder.adjust(2)
return builder.as_markup()

def check_limit(user_id):
if db.is_premium(user_id):
return True
return db.get_requests_count(user_id) < FREE_REQUESTS

@router.callback_query(F.data == “horoscope”)
async def horoscope_start(callback: CallbackQuery, state: FSMContext):
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
await state.set_state(HoroscopeState.waiting_birthdate)
await callback.message.edit_text(
“🗓 *Персональний гороскоп*\n\nВведи дату народження:\n`ДД.ММ.РРРР`\n\nНаприклад: `15.03.1995`”,
parse_mode=“Markdown”
)

@router.message(HoroscopeState.waiting_birthdate)
async def horoscope_get_date(message: Message, state: FSMContext):
await state.update_data(birthdate=message.text.strip())
await state.set_state(HoroscopeState.waiting_sign)
await message.answer(“♈ *Обери свій знак зодіаку:*”, parse_mode=“Markdown”, reply_markup=zodiac_keyboard())

@router.callback_query(F.data.startswith(“sign_”), HoroscopeState.waiting_sign)
async def horoscope_generate(callback: CallbackQuery, state: FSMContext):
sign = callback.data.replace(“sign_”, “”)
data = await state.get_data()
birthdate = data.get(“birthdate”, “невідома”)
await state.clear()
await callback.message.edit_text(“🔮 Читаю зірки… Зачекай ✨”)
try:
result = await ai.get_horoscope(sign, birthdate)
db.increment_requests(callback.from_user.id)
await callback.message.edit_text(
f”♈ *Твій гороскоп — {sign}*\n\n{result}”,
parse_mode=“Markdown”, reply_markup=back_keyboard()
)
except Exception:
await callback.message.edit_text(“❌ Помилка. Спробуй ще раз.”, reply_markup=back_keyboard())
