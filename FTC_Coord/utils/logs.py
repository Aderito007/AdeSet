import os
import datetime

def log_acesso(usuario):
    caminho_pasta = "logs"
    os.makedirs(caminho_pasta, exist_ok=True)  # cria a pasta se não existir

    with open(os.path.join(caminho_pasta, "log_acessos.txt"), "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] Login realizado por '{usuario}'\n")
