# components/CardServico.py
from ttkbootstrap import *

class CardServico(Frame):
    def __init__(self, parent, dados):
        super().__init__(parent, padding=15, bootstyle="light")
        Label(self, text=f"🧾 {dados['titulo']}", font=("Arial", 12, "bold")).pack(anchor="w")
        Label(self, text=f"Responsável: {dados['responsavel']}").pack(anchor="w")
        Label(self, text=f"Actividade: {dados['actividade']}").pack(anchor="w")
        Label(self, text=f"Local: {dados['local']}").pack(anchor="w")
        Label(self, text=f"Status: {dados['status']}").pack(anchor="w")
        Label(self, text=f"Início: {dados['data_inicio'][:10]}").pack(anchor="w")