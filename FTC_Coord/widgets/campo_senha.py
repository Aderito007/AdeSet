# widgets/campo_senha.py
from ttkbootstrap import *
from tkinter import StringVar

class CampoSenhaTTK(Frame):
    def __init__(self, master, texto="Senha:", largura=28, placeholder="", **kwargs):
        super().__init__(master, **kwargs)

        self.senha_visivel = False
        self.var_senha = StringVar()

        Label(self, text=texto).pack(anchor="w")
        
        self.frame_entry = Frame(self)
        self.frame_entry.pack(fill=X)

        self.entry = Entry(self.frame_entry, textvariable=self.var_senha, show="*", width=largura)
        self.entry.insert(0, placeholder)
        self.entry.pack(side=LEFT, fill=X, expand=True)

        self.btn_toggle = Button(
            self.frame_entry, text="👁️", width=3, command=self.alternar_visibilidade
        )
        self.btn_toggle.pack(side=RIGHT, padx=3)

    def alternar_visibilidade(self):
        self.senha_visivel = not self.senha_visivel
        self.entry.configure(show="" if self.senha_visivel else "*")
        self.btn_toggle.configure(text="🙈" if self.senha_visivel else "👁️")

    def get(self):
        return self.var_senha.get()

    def set(self, texto):
        self.var_senha.set(texto)

        