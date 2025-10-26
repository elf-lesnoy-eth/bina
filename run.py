import asyncio
from bot import start_bot

if __name__ == "__main__":
    try:
        print("🚀 Запуск Telegram-бота на Render...")
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        print("❌ Бот остановлен.")
