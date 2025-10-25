import asyncio
from main import app
from bot import start_bot
import uvicorn
from aiogram import F
from aiogram.types import CallbackQuery, InputMediaPhoto



async def start():
    # запускаем uvicorn как задачу
    config = uvicorn.Config(app, host="127.0.0.1", port=8000, reload=False)
    server = uvicorn.Server(config)
    app_task = asyncio.create_task(server.serve())
    bot_task = asyncio.create_task(start_bot())

    await asyncio.gather(bot_task, app_task)


# Если loop уже работает (например, в Jupyter) — используем его
try:
    asyncio.get_event_loop().run_until_complete(start())
except RuntimeError as e:
    if "already running" in str(e):
        print("⚠️ Async loop is already running. Use 'await start()' in a notebook.")
    else:
        raise