# downloader.py
import os
import re
import requests

def extract_id(url: str) -> str | None:
    match = re.search(r"[-\w]{25,}", url or "")
    return match.group(0) if match else None

def download_drive_file(url: str, path: str):
    file_id = extract_id(url)
    if not file_id:
        print(f"⚠️ Неверная ссылка: {url}")
        return False

    dl_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    print(f"⬇️ Скачиваем {dl_url} → {path}")
    resp = requests.get(dl_url, stream=True)
    if resp.status_code == 200:
        with open(path, "wb") as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        print(f"✅ Готово: {path}")
        return True
    else:
        print(f"❌ Ошибка {resp.status_code}")
        return False

def download_user_files(username: str, pdf_link: str, photos_links: str):
    base = os.path.join("data", username)
    os.makedirs(base, exist_ok=True)

    if pdf_link:
        download_drive_file(pdf_link, os.path.join(base, "contract.pdf"))

    if photos_links:
        for i, link in enumerate(photos_links.split(","), 1):
            link = link.strip()
            if not link:
                continue
            download_drive_file(link, os.path.join(base, f"photo_{i}.jpg"))

    print(f"📂 Все файлы сохранены в: {base}")
