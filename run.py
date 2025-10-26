import asyncio
import os
from aiohttp import web
from bot import start_bot


async def handle(request):
    return web.Response(text="✅ Bot is alive and serving HTTP requests!")


async def main():
    print("🚀 [INIT] Starting Render process...")

    # 1. Проверим PORT
    port = int(os.environ.get("PORT", 8080))
    print(f"🌐 [CONFIG] Using port = {port}")

    # 2. Создаем aiohttp сервер
    app = web.Application()
    app.router.add_get("/", handle)
    app.router.add_get("/health", handle)

    runner = web.AppRunner(app)
    await runner.setup()
    print("🛠 [SERVER] Runner setup complete")

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"✅ [SERVER] Listening on 0.0.0.0:{port}")

    # 3. Запускаем бота
    print("🤖 [BOT] Starting Telegram bot...")
    try:
        await start_bot()
    except Exception as e:
        print(f"❌ [BOT] Failed: {e}")
        raise

    print("🎉 [ALL OK] Bot and server running.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"🔥 [FATAL] {e}")
