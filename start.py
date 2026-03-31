# handlers/start.py

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
import database as db
from config import FREE_REQUESTS

router = Router()

def main_menu_keyboard():
builder = InlineKeyboardBuilder()
builder.button(text=“♈ Персональний гороскоп”, callback_data=“horoscope”)
builder.button(text=“🃏 Розклад Таро”, callback_data=“tarot”)
builder.button(text=“💎 Мій лунний камінь”, callback_data=“stone”)
builder.button(text=“💑 Сумісність двох людей”, callback_data=“compatibility”)
builder.button(text=“💳 Підписка / Баланс”, callback_data=“subscription”)
builder.adjust(1)
return builder.as_markup()

@router.message(CommandStart())
async def cmd_start(message: Message):
user = message.from_user
db.add_user(user.id, user.username or “”, user.full_name or “”)
used = db.get_requests_count(user.id)
premium = db.is_premium(user.id)

```
if premium:
    status = "✨ У тебе активна підписка — безлімітний доступ!"
else:
    left = max(0, FREE_REQUESTS - used)
    status = f"🆓 Безкоштовних запитів залишилось: {left}/{FREE_REQUESTS}"

await message.answer(
    f"🌙 *Вітаю, {user.first_name}!*\n\n"
    f"Я — твій персональний астролог. Розкрию зірки, карти Таро та магію каменів спеціально для тебе.\n\n"
    f"{status}\n\nОбери що тебе цікавить 👇",
    parse_mode="Markdown",
    reply_markup=main_menu_keyboard()
)
```

@router.callback_query(F.data == “menu”)
async def back_to_menu(callback: CallbackQuery):
await callback.message.edit_text(
“🌙 *Головне меню*\n\nОбери що тебе цікавить 👇”,
parse_mode=“Markdown”,
reply_markup=main_menu_keyboard()
)

@router.callback_query(F.data == “subscription”)
async def subscription_info(callback: CallbackQuery):
user_id = callback.from_user.id
used = db.get_requests_count(user_id)
premium = db.is_premium(user_id)
builder = InlineKeyboardBuilder()
builder.button(text=“◀️ Назад”, callback_data=“menu”)

```
if premium:
    text = (
        "✨ *Твоя підписка активна!*\n\n"
        f"Використано запитів: {used}"
    )
else:
    left = max(0, FREE_REQUESTS - used)
    text = (
        "💳 *Підписка AstroUA*\n\n"
        f"🆓 Залишилось безкоштовних: *{left}*\n\n"
        "За підпискою:\n"
        "• ♾️ Безлімітні запити\n"
        "• 🔮 Всі функції\n"
        "• ⚡️ Пріоритет\n\n"
        "💰 *Ціна: 4.99€ / місяць*\n\n"
        "Для оплати напиши адміну: @your_username"
    )
await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=builder.as_markup())
```
