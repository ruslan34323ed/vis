import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN
from handlers import router
from scheduler import send_news

logging.basicConfig(level=logging.INFO)

async def start_bot():
    """Запуск бота"""
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
    dp = Dispatcher()
    dp.include_router(router)

    asyncio.create_task(send_news())  # Запуск проверки новостей

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
