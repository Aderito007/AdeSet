# core/backup.py
from ttkbootstrap import *
import shutil, os, datetime
from db.conexao import get_db_path

class TelaBackup:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root, padding=30)
        self.frame.pack(fill=BOTH, expand=True)

        Label(self.frame, text="🗄️ Backup do Sistema", font=("Arial", 16)).pack(pady=10)
        Button(self.frame, text="Gerar Backup Agora", bootstyle="primary", command=self.gerar).pack(pady=15)
        self.status = Label(self.frame, text="", font=("Arial", 12))
        self.status.pack()

    def gerar(self):
        origem = get_db_path()
        data = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        destino_pasta = "backup"
        os.makedirs(destino_pasta, exist_ok=True)
        destino_arquivo = os.path.join(destino_pasta, f"nexugest_backup_{data}.db")

        try:
            shutil.copy2(origem, destino_arquivo)
            self.status.config(text=f"🟢 Backup salvo em: {destino_arquivo}")
        except Exception as e:
            self.status.config(text=f"🔴 Erro ao gerar backup: {e}")