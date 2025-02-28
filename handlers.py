from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from parser import fetch_news

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Команда /start"""
    await message.answer("Привет! Я уведомляю о новых новостях TLScontact.\n\nИспользуй /news, чтобы проверить новости.")

@router.message(Command("news"))
async def cmd_news(message: Message):
    """Команда /news — проверяет последнюю новость"""
    news = await fetch_news()
    if news:
        await message.answer(
            f"{news}\n\n[Сайт](https://it.tlscontact.com/by/msq/page.php?pid=news&l=ru)",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    else:
        await message.answer("Нет новых новостей.")
