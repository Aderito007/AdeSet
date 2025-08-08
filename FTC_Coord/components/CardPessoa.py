# components/CardPessoa.py
from ttkbootstrap import Frame, Label

class CardPessoa(Frame):
    def __init__(self, parent, dados):
        super().__init__(parent, padding=10)
        Label(self, text=f"Nome: {dados['nome']}").pack(anchor="w")
        Label(self, text=f"Cargo: {dados['cargo']}").pack(anchor="w")
        Label(self, text=f"Tipo: {dados['tipo']}").pack(anchor="w")
        