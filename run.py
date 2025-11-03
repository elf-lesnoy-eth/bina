import os
import asyncio
from aiohttp import web
from flask import Flask, send_from_directory, request, jsonify
from downloader import download_user_files
from bot import bot, dp

# === Настройки ===
ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, "data")

flask_app = Flask(__name__, static_folder=ROOT, static_url_path="")

@flask_app.route("/")
def index():
    """Отдаём index.html из корня проекта"""
    file_path = os.path.join(ROOT, "index.html")
    print(f"⚡ Serving index.html from: {file_path}")
    return send_from_directory(ROOT, "index.html")

@flask_app.route("/download")
def download_from_drive():
    username = request.args.get("username", "anon")
    pdf = request.args.get("pdf", "")
    photos = request.args.get("photos", "")
    print(f"📥 /download → {username}")

    try:
        download_user_files(username, pdf, photos)
        return jsonify({"ok": True})
    except Exception as e:
        print(f"❌ Ошибка при скачивании: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@flask_app.route("/data/<username>/<path:filename>")
def serve_user_file(username, filename):
    folder = os.path.join(DATA_DIR, username)
    path = os.path.join(folder, filename)
    if os.path.exists(path):
        return send_from_directory(folder, filename)
    return jsonify({"error": "Файл не найден"}), 404

@flask_app.after_request
def add_headers(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# === aiohttp сервер для здоровья и запуска ===
async def health(request):
    return web.Response(text="✅ Bot is alive")

async def start_bot():
    print("🤖 Starting bot polling...")
    asyncio.create_task(dp.start_polling(bot))


def main():
    port = int(os.getenv("PORT", 10000))

    # Запускаем Flask в фоне через aiohttp
    from threading import Thread
    Thread(target=lambda: flask_app.run(host="0.0.0.0", port=port, debug=False)).start()

    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    loop.run_forever()


if __name__ == "__main__":
    main()
