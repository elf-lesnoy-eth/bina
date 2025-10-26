import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# === ПУТИ ===
BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# === FASTAPI ПРИЛОЖЕНИЕ ===
app = FastAPI()

# === СТАТИКА и ШАБЛОНЫ ===
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# === ГЛАВНАЯ СТРАНИЦА ===
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(index_path):
        print(f"❌ index.html not found at {index_path}")
        return HTMLResponse("<h1>index.html not found</h1>", status_code=404)
    print(f"✅ index.html found and served from {index_path}")
    return templates.TemplateResponse("index.html", {"request": request})


# === СТРАНИЦА ФОТО (для арендатора) ===
@app.get("/photos", response_class=HTMLResponse)
async def photos_page(request: Request, user: str = "elf_lesnoy"):
    """Показывает все фото арендатора"""
    photos_path = os.path.join(TEMPLATES_DIR, "photos.html")
    if not os.path.exists(photos_path):
        print(f"❌ photos.html not found at {photos_path}")
        return HTMLResponse("<h1>photos.html not found</h1>", status_code=404)
    print(f"✅ photos.html found and served for {user}")
    return templates.TemplateResponse("photos.html", {"request": request, "username": user})


# === СТРАНИЦА ДОКУМЕНТОВ (договоры арендатора) ===
@app.get("/docs", response_class=HTMLResponse)
async def docs_page(request: Request, user: str = "elf_lesnoy"):
    """Показывает PDF-документы арендатора"""
    docs_path = os.path.join(TEMPLATES_DIR, "docs.html")
    if not os.path.exists(docs_path):
        print(f"❌ docs.html not found at {docs_path}")
        return HTMLResponse("<h1>docs.html not found</h1>", status_code=404)
    print(f"✅ docs.html found and served for {user}")
    return templates.TemplateResponse("docs.html", {"request": request, "username": user})
