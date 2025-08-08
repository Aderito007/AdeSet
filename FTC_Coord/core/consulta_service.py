# core/consulta_servicos.py
from ttkbootstrap import *
import sqlite3
from components.CardServico import CardServico
from db.conexao import conectar


class ConsultaServicos:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root, padding=20)
        self.frame.pack(fill=BOTH, expand=True)

        Label(self.frame, text="Consulta de Serviços", font=("Arial", 16)).pack(pady=10)

        self.filtro_status = Combobox(self.frame, values=["", "pendente", "em andamento", "concluído"])
        self.filtro_actividade = Entry(self.frame)
        self.filtro_local = Entry(self.frame)

        filtros = [("Status", self.filtro_status), ("Actividade", self.filtro_actividade), ("Local", self.filtro_local)]
        for label, widget in filtros:
            Label(self.frame, text=f"{label}").pack(anchor="w")
            widget.pack(fill=X, pady=3)

        Button(self.frame, text="Filtrar", bootstyle="primary", command=self.carregar).pack(pady=10)

        self.area_resultado = Frame(self.frame)
        self.area_resultado.pack(fill=BOTH, expand=True)

        self.carregar()

    def carregar(self):
        for widget in self.area_resultado.winfo_children():
            widget.destroy()

        query = "SELECT * FROM servicos WHERE 1=1"
        params = []

        if self.filtro_status.get():
            query += " AND status=?"
            params.append(self.filtro_status.get())

        if self.filtro_actividade.get():
            query += " AND actividade LIKE ?"
            params.append(f"%{self.filtro_actividade.get()}%")

        if self.filtro_local.get():
            query += " AND local_trabalho LIKE ?"
            params.append(f"%{self.filtro_local.get()}%")

        conn = conectar()
        c = conn.cursor()
        c.execute(query, params)

        for serv in c.fetchall():
            dados = {
                "titulo": serv[1],
                "responsavel": serv[6],
                "status": serv[7],
                "local": serv[5],
                "actividade": serv[3],
                "data_inicio": serv[8]
            }
            card = CardServico(self.area_resultado, dados)
            card.pack(fill=X, pady=6)

        conn.close()

        