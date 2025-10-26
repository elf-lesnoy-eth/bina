import os
import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Если хочешь, чтобы ngrok поднимался автоматически
from pyngrok import ngrok

BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(title="EasyHome")

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(index_path):
        return HTMLResponse("<h1>index.html not found</h1>", status_code=404)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/photos", response_class=HTMLResponse)
async def photos(request: Request, user: str = "elf_lesnoy"):
    photos_path = os.path.join(TEMPLATES_DIR, "photos.html")
    if not os.path.exists(photos_path):
        return HTMLResponse("<h1>photos.html not found</h1>", status_code=404)
    return templates.TemplateResponse("photos.html", {"request": request, "username": user})


@app.get("/docs", response_class=HTMLResponse)
async def docs(request: Request, user: str = "elf_lesnoy"):
    docs_path = os.path.join(TEMPLATES_DIR, "docs.html")
    if not os.path.exists(docs_path):
        return HTMLResponse("<h1>docs.html not found</h1>", status_code=404)
    return templates.TemplateResponse("docs.html", {"request": request, "username": user})


async def start_server():
    port = 8000

    # === Запускаем ngrok ===
    public_url = ngrok.connect(port).public_url
    print(f"🌍 Публичная ссылка через ngrok: {public_url}")
    print(f"🏠 Локально: http://127.0.0.1:{port}")

    # === Запускаем FastAPI ===
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("❌ Остановка сервера...")
