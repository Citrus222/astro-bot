# bot.py

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
import database as db
import start
import horoscope
import tarot
import stone
import compatibility

logging.basicConfig(level=logging.INFO)

async def main():
    db.init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(horoscope.router)
    dp.include_router(tarot.router)
    dp.include_router(stone.router)
    dp.include_router(compatibility.router)

    print("🔮 AstroUA Bot запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
