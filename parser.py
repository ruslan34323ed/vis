import aiohttp
import ssl
import certifi
from bs4 import BeautifulSoup
from config import URL

last_news_title = None  # Переменная для хранения последней новости

async def fetch_news():
    """Запрашивает страницу и парсит последнюю новость"""
    global last_news_title

    ssl_context = ssl.create_default_context(cafile=certifi.where())  # Устранение ошибки SSL

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, ssl=ssl_context) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    news_blocks = soup.find_all("div", class_="d-flex py-4 align-items-start align-items-md-baseline mt-4")

    if not news_blocks:
        return None  # Если новости не найдены

    latest_news = news_blocks[0]  # Берём первую новость
    title = latest_news.find("h3").text.strip()

    if title == last_news_title:  # Если новость уже была отправлена
        return None

    last_news_title = title  # Обновляем последнюю новость

    # Собираем весь текст между этой и следующей новостью
    news_text = []
    for element in latest_news.find_next_siblings():
        if element.name == "div":  # Если следующий заголовок h3 — останавливаемся
            break
        news_text.append(element.text.strip())

    return f"🆕 *{title}*\n\n" + "\n".join(news_text)
