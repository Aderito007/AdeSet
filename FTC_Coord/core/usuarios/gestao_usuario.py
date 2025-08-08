# core/gestao_usuarios.py
from ttkbootstrap import *
from db.conexao import conectar


class TelaGestaoUsuarios:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root, padding=20)
        self.frame.pack(fill=BOTH, expand=True)

        Label(self.frame, text="👥 Gestão de Usuários", font=("Arial", 16)).pack(pady=10)

        self.tabela = Treeview(self.frame, columns=("nome", "usuario", "nivel", "ativo"), show="headings")
        for col in self.tabela["columns"]:
            self.tabela.heading(col, text=col.title())
        self.tabela.pack(fill=BOTH, expand=True)

        Button(self.frame, text="🔄 Atualizar", command=self.carregar).pack(pady=10)
        self.carregar()

    def carregar(self):
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT nome, usuario, nivel, ativo FROM usuarios_sistema")
        dados = c.fetchall()
        conn.close()

        self.tabela.delete(*self.tabela.get_children())
        for linha in dados:
            ativo_str = "ativo" if linha[3] == 1 else "inativo"
            self.tabela.insert("", "end", values=(linha[0], linha[1], linha[2], ativo_str))