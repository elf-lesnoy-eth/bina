# start_tunnel.py
import os
from pyngrok import ngrok, conf

# где может лежать ngrok (Apple Silicon / Intel / локальный файл)
candidates = [
    "/opt/homebrew/bin/ngrok",   # Apple Silicon
    "/usr/local/bin/ngrok",      # Intel
    os.path.join(os.getcwd(), "ngrok"),  # если положишь рядом с проектом
]
for p in candidates:
    if os.path.exists(p):
        conf.get_default().ngrok_path = p
        break

# токен из окружения (так удобнее)
token = "2yulEA4G4kjphLxnYAiYFILlQVo_7bnuULDi5DDUCa7M9zU6v"
if token:
    ngrok.set_auth_token(token)

tunnel = ngrok.connect(8080, "http")   # твой Flask на 8080
print("PUBLIC URL:", tunnel.public_url)

# держим процесс живым
proc = ngrok.get_ngrok_process()
try:
    proc.proc.wait()
except KeyboardInterrupt:
    ngrok.kill()
