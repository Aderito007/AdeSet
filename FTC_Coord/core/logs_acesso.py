# core/logs_acesso.py
from ttkbootstrap import *
import os

class TelaLogs:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root, padding=20)
        self.frame.pack(fill=BOTH, expand=True)

        Label(self.frame, text="📜 Logs de Acesso", font=("Arial", 16)).pack(pady=10)

        self.busca_usuario = Entry(self.frame)
        self.busca_usuario.pack(fill=X)
        Button(self.frame, text="Filtrar", bootstyle="info", command=self.carregar_logs).pack(pady=10)

        self.area_texto = Text(self.frame, height=20)
        self.area_texto.pack(fill=BOTH, expand=True)

        self.carregar_logs()

    def carregar_logs(self):
        self.area_texto.delete("1.0", "end")
        filtro = self.busca_usuario.get().lower()
        caminho = "logs/log_acessos.txt"

        if not os.path.exists(caminho):
            self.area_texto.insert("end", "Nenhum log encontrado.")
            return

        with open(caminho, encoding="utf-8") as f:
            for linha in f:
                if filtro in linha.lower():
                    self.area_texto.insert("end", linha)