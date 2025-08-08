
from ttkbootstrap import *
import datetime
from utils.logs import log_acesso
from db.conexao import conectar
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.widgets import DateEntry

class CadastroServico:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root, padding=20)
        self.frame.pack(fill=BOTH, expand=True)

        Label(self.frame, text="Cadastro de Serviço", font=("Arial", 16)).pack(pady=10)

        self.titulo = Entry(self.frame)
        self.descricao = Text(self.frame, height=4)

        valores_actividade = self.carregar_valores("actividade")
        self.actividade = ttk.Combobox(self.frame, values=valores_actividade, state="normal")
        self.actividade.bind("<FocusOut>", lambda e: self.adicionar_item_e_salvar(self.actividade, self.actividade.get(), "actividade"))
        self.actividade.bind("<Double-1>", lambda e: self.abrir_gestor_listas())

        valores_servico = self.carregar_valores("servico_adjudicado")
        self.servico_adjudicado = ttk.Combobox(self.frame, values=valores_servico, state="normal")
        self.servico_adjudicado.bind("<FocusOut>", lambda e: self.adicionar_item_e_salvar(self.servico_adjudicado, self.servico_adjudicado.get(), "servico_adjudicado"))
        
        self.local_trabalho = Entry(self.frame)

        self.responsavel = Combobox(self.frame, values=self.carregar_membros())
        self.status = Combobox(self.frame, values=["pendente", "em andamento", "concluído"])
        self.data_conclusao = DateEntry(self.frame)

        campos = [
            ("Título", self.titulo),
            ("Descrição", self.descricao),
            ("Actividade / Projeto", self.actividade),
            ("Serviço Adjudicado", self.servico_adjudicado),
            ("Local de Trabalho", self.local_trabalho),
            ("Responsável", self.responsavel),
            ("Status", self.status),
            ("Data Conclusão", self.data_conclusao)
        ]

        for label, widget in campos:
            Label(self.frame, text=label).pack(anchor="w")
            widget.pack(fill=X, pady=3)

        Button(self.frame, text="Salvar Serviço", bootstyle="success", command=self.salvar).pack(pady=15)

    def carregar_membros(self):
        conn = conectar()
        c = conn.cursor()
        c.execute("SELECT id, nome FROM pessoas")
        self.membros_dict = {nome: mid for mid, nome in c.fetchall()}
        conn.close()
        return list(self.membros_dict.keys())

    
    def validar_campos(self):
        if not self.titulo.get().strip():
            return "O campo 'Título' está vazio."
        if not self.actividade.get().strip():
            return "O campo 'Actividade' está vazio."
        # outros campos...
        return None
    

    def salvar(self):
        erro = self.validar_campos()
        if erro:
            Messagebox.show_error(erro, title="Erro")
            return
        
        responsavel_id = self.membros_dict.get(self.responsavel.get())
        if not responsavel_id:
            Messagebox.show_error("Responsável não encontrado.", title="Erro")
            return
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO servicos (
                titulo, descricao, actividade, servico_adjudicado,
                local_trabalho, responsavel, status, data_inicio, data_conclusao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.titulo.get(),
            self.descricao.get("1.0", "end").strip(),
            self.actividade.get(),
            self.servico_adjudicado.get(),
            self.local_trabalho.get(),
            responsavel_id,
            self.status.get(),
            datetime.datetime.now().isoformat(),
            self.data_conclusao.get()
        ))
        conn.commit()
        
        log_acesso(self.titulo.get(), self.responsavel.get())
        conn.close()
        from tkinter import messagebox as Messagebox
        Messagebox.show_info("Serviço cadastrado com sucesso!", title="Confirmação")


    def carregar_valores(self, campo):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT valor FROM listas_institucionais WHERE campo = ?", (campo,))
        resultados = [row[0] for row in cursor.fetchall()]
        conn.close()
        return resultados
    
    def adicionar_item_e_salvar(self, combobox, valor, campo):
        if valor and valor not in combobox["values"]:
            novos = list(combobox["values"]) + [valor]
            combobox["values"] = sorted(novos)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO listas_institucionais (campo, valor) VALUES (?, ?)", (campo, valor))
            conn.commit()
            conn.close()
        combobox.set(valor)
    def abrir_gestor_listas(self):
        janela = tk.Toplevel()
        janela.title("Gestor de Listas Institucionais")

        tree = ttk.Treeview(janela, columns=("campo", "valor"), show="headings")
        tree.heading("campo", text="Campo")
        tree.heading("valor", text="Valor")
        tree.pack(fill="both", expand=True)

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, campo, valor FROM listas_institucionais")
        for row in cursor.fetchall():
            tree.insert("", "end", iid=row[0], values=(row[1], row[2]))
        conn.close()

        def remover_selecionado():
            item = tree.selection()
            if item:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM listas_institucionais WHERE id = ?", (item[0],))
                conn.commit()
                conn.close()
                tree.delete(item)

        btn_remover = ttk.Button(janela, text="🗑️ Remover Selecionado", command=remover_selecionado)
        btn_remover.pack(pady=10)