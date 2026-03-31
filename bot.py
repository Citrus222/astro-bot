import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.horoscope import router as horoscope_router
from handlers.tarot import router as tarot_router
from handlers.stone import router as stone_router
from handlers.compatibility import router as compatibility_router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключаем роутеры
dp.include_router(start_router)
dp.include_router(horoscope_router)
dp.include_router(tarot_router)
dp.include_router(stone_router)
dp.include_router(compatibility_router)

async def main():
    print("✅ Бот запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
