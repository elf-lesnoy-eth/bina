import asyncio
from aiohttp import web
from bot import bot, dp  # импорт твоего aiogram-бота

async def index(request):
    return web.FileResponse("templates/index.html")

async def health(request):
    return web.Response(text="✅ Bot is alive and serving HTTP requests!")

async def on_startup(app):
    print("🚀 Starting bot polling...")
    asyncio.create_task(dp.start_polling(bot))  # бот стартует в фоне

app = web.Application()
app.router.add_get("/", index)
app.router.add_get("/health", health)
app.on_startup.append(on_startup)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=10000)
