# serve.py
from flask import Flask, send_from_directory
import os

# === Параметры проекта ===
ROOT = os.path.dirname(os.path.abspath(__file__))

# Создаём Flask-приложение, указываем папку, где лежат все статические файлы
app = Flask(__name__, static_folder=ROOT, static_url_path="")

# === Главная страница ===
@app.route("/")
def index():
    file_path = os.path.join(ROOT, "index.html")
    print(f"⚡ Serving index.html from: {file_path}")
    return send_from_directory(ROOT, "index.html")

# === Любые статические файлы (CSS, JS, изображения и т.п.) ===
@app.route("/<path:path>")
def static_files(path):
    file_path = os.path.join(ROOT, path)
    print(f"📦 Serving static file: {file_path}")
    return send_from_directory(ROOT, path)

# === Отключаем кэширование для всех ответов ===
@app.after_request
def add_header(response):
    """
    Этот хук добавляет заголовки, чтобы браузер и Flask не кэшировали старые версии файлов.
    """
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# === Точка входа ===
if __name__ == "__main__":
    # 127.0.0.1 — только локально, порт 8080 можно пробросить через ngrok
    print("🚀 Flask сервер запущен на http://127.0.0.1:8080")
    print("💡 Подсказка: если страница не обновляется — нажми Cmd+Shift+R (или Ctrl+Shift+R).")
    app.run(host="127.0.0.1", port=8080, debug=True)
