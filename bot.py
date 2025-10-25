#мини апка

import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, Message

BOT_TOKEN = os.getenv("BOT_TOKEN", "8108367367:AAGgZXVaS0lVbacNjzcnVxoO1XddDSijD3M")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

NGROK_API = "http://127.0.0.1:4040/api/tunnels"  # локальный API ngrok
MINIAPP_URL = "https://a67428842ad4.ngrok-free.app/"  # можно задать вручную, иначе возьмём из ngrok

async def get_ngrok_https_url() -> str | None:
    # пытаемся достать публичный https-URL текущего туннеля
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(NGROK_API, timeout=5) as r:
                data = await r.json()
        for t in data.get("tunnels", []):
            url = t.get("public_url", "")
            if url.startswith("https://"):
                return url
    except Exception:
        return None
    return None

@dp.message(CommandStart())
async def start_handler(message: Message):
    global MINIAPP_URL
    # если не задано руками — попробуем спросить у ngrok на лету
    if not MINIAPP_URL:
        MINIAPP_URL = await get_ngrok_https_url()

    if not MINIAPP_URL:
        await message.answer(
            "Мини-апп пока недоступен (не найден публичный адрес).\n"
            "Убедись, что запущены: `serve.py` и `ngrok http 8000`."
        )
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="🪟 Открыть мини-апп",
            web_app=WebAppInfo(url=MINIAPP_URL)
        )
    ]])
    await message.answer("👋 Открой мини-апп — там всё красиво и в одном месте.", reply_markup=kb)

async def main():
    # на старте тоже попробуем подтянуть URL (чтобы не ждать /start)
    global MINIAPP_URL
    if not MINIAPP_URL:
        MINIAPP_URL = await get_ngrok_https_url()
    await dp.start_polling(bot)

async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
