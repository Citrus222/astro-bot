# handlers/tarot.py

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database as db
import ai
from config import FREE_REQUESTS

router = Router()

TAROT_TOPICS = [“💕 Кохання”, “💼 Кар’єра”, “💰 Фінанси”, “🌿 Здоров’я”, “👨‍👩‍👧 Сім’я”, “🔮 Загальне”]

class TarotState(StatesGroup):
waiting_custom = State()

def topics_keyboard():
builder = InlineKeyboardBuilder()
for topic in TAROT_TOPICS:
builder.button(text=topic, callback_data=f”tarot_{topic}”)
builder.button(text=“✏️ Своє питання”, callback_data=“tarot_custom”)
builder.button(text=“◀️ Назад”, callback_data=“menu”)
builder.adjust(2, 2, 2, 1, 1)
return builder.as_markup()

def back_keyboard():
builder = InlineKeyboardBuilder()
builder.button(text=“🃏 Ще розклад”, callback_data=“tarot”)
builder.button(text=“◀️ Меню”, callback_data=“menu”)
builder.adjust(2)
return builder.as_markup()

def check_limit(user_id):
if db.is_premium(user_id):
return True
return db.get_requests_count(user_id) < FREE_REQUESTS

@router.callback_query(F.data == “tarot”)
async def tarot_start(callback: CallbackQuery):
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
“🃏 *Розклад Таро*\n\nОбери сферу або постав своє питання:”,
parse_mode=“Markdown”, reply_markup=topics_keyboard()
)

@router.callback_query(F.data.startswith(“tarot_”) & ~F.data.endswith(“custom”))
async def tarot_generate(callback: CallbackQuery):
topic = callback.data.replace(“tarot_”, “”)
await callback.message.edit_text(“🃏 Тасую карти… ✨”)
try:
result = await ai.get_tarot(topic)
db.increment_requests(callback.from_user.id)
await callback.message.edit_text(
f”🃏 *Розклад Таро — {topic}*\n\n{result}”,
parse_mode=“Markdown”, reply_markup=back_keyboard()
)
except Exception:
await callback.message.edit_text(“❌ Помилка. Спробуй ще раз.”, reply_markup=back_keyboard())

@router.callback_query(F.data == “tarot_custom”)
async def tarot_custom(callback: CallbackQuery, state: FSMContext):
await state.set_state(TarotState.waiting_custom)
await callback.message.edit_text(“✏️ Напиши своє питання для карт:”)

@router.message(TarotState.waiting_custom)
async def tarot_custom_generate(message: Message, state: FSMContext):
question = message.text.strip()
await state.clear()
await message.answer(“🃏 Тасую карти… ✨”)
try:
result = await ai.get_tarot(question)
db.increment_requests(message.from_user.id)
await message.answer(f”🃏 *Розклад Таро*\n\n{result}”, parse_mode=“Markdown”, reply_markup=back_keyboard())
except Exception:
await message.answer(“❌ Помилка. Спробуй ще раз.”, reply_markup=back_keyboard())
