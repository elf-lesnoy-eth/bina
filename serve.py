# serve.py
from flask import Flask, send_from_directory
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=ROOT, static_url_path="")

@app.route("/")
def index():
    return send_from_directory(ROOT, "index.html")

# чтобы раздавать любые статические файлы (фото и т.п.)
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(ROOT, path)

if __name__ == "__main__":
    # важно: порт 8000 — его пробросим через ngrok
    app.run(host="127.0.0.1", port=8080, debug=True)
