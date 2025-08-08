from ttkbootstrap import *
import sqlite3
from components.CardPessoa import CardPessoa
from db.conexao import conectar


class ConsultaPessoas:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root, padding=30)
        self.frame.pack(fill=BOTH, expand=True)

        # Campo de filtro
        Label(self.frame, text="Filtrar por tipo").pack()
        self.filtro = Combobox(self.frame, values=["", "admin", "membro", "prestador"])
        self.filtro.pack()
        Button(self.frame, text="Pesquisar", command=self.carregar).pack(pady=10)

        # Área de resultados
        self.area_resultado = Frame(self.frame)
        self.area_resultado.pack(fill=BOTH, expand=True)

        self.carregar()

    def carregar(self):
        for widget in self.area_resultado.winfo_children():
            widget.destroy()

        tipo = self.filtro.get()
        conn = conectar()
        cursor = conn.cursor()

        if tipo:
            cursor.execute("SELECT * FROM pessoas WHERE tipo=?", (tipo,))
        else:
            cursor.execute("SELECT * FROM pessoas")

        for linha in cursor.fetchall():
            dados = {
                "nome": linha[1],
                "tipo": linha[2],
                "cargo": linha[3]
            }
            card = CardPessoa(self.area_resultado, dados)
            card.pack(fill=X, pady=5)

        conn.close()