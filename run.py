import asyncio
import uvicorn
import webbrowser
from main import app
from bot import start_bot
from aiogram import F
from aiogram.types import CallbackQuery, InputMediaPhoto


async def start():
    """
    Запускает одновременно:
    - FastAPI сервер (для веб-приложения)
    - Telegram-бота (aiogram)
    И автоматически открывает мини-апп в браузере.
    """

    # Настраиваем веб-сервер
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False,  # можно включить True во время разработки
        log_level="info",
    )
    server = uvicorn.Server(config)

    # Создаём отдельные задачи
    app_task = asyncio.create_task(server.serve())
    bot_task = asyncio.create_task(start_bot())

    # Открываем мини-апп в браузере автоматически
    webbrowser.open("http://127.0.0.1:8000")

    # Запускаем обе задачи параллельно
    await asyncio.gather(bot_task, app_task)


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(start())
    except RuntimeError as e:
        if "already running" in str(e):
            print("⚠️ Async loop is already running. Use 'await start()' in a notebook.")
        else:
            raise
