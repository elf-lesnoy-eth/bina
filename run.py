import asyncio
import os
from aiohttp import web
from bot import start_bot


async def handle(request):
    return web.Response(text="🤖 Telegram bot is running on Render!")


async def main():
    # создаем aiohttp web-сервер, чтобы Render видел открытый порт
    app = web.Application()
    app.router.add_get("/", handle)

    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"🌐 Web server started on port {port}")
    print("🚀 Launching Telegram bot...")

    # Запускаем Telegram-бота параллельно
    await start_bot()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("❌ Bot stopped.")
