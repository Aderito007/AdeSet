import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from ttkbootstrap.widgets import DateEntry
from db.conexao import conectar
from db.modelos import gerar_codigo_institucional
from utils.validador import Validador


class TelaGestaoMembros:
    def __init__(self, root):
        self.root = root
        self.root.title("📋 Cadastro Institucional de Membros")
        self.root.geometry("1440x920")

        self._modo_edicao = False  # usa @property em_edicao
        self.codigo_atual = None   # necessário para edição/exclusão

        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill=BOTH, expand=True)

        # 🗂️ Seções visuais
        self.secao_pessoal = ttk.LabelFrame(self.frame, text="👤 Dados Pessoais", padding=10)
        self.secao_pessoal.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.secao_institucional = ttk.LabelFrame(self.frame, text="🏛️ Dados Institucionais", padding=10)
        self.secao_institucional.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 📌 Campos Pessoais
        self.vars = {}
        campos_pessoais = [
            ("Nome", "nome"),
            ("Formação", "formacao"),
            ("Sexo", "sexo"),
            ("Língua Bantu", "lingua_bantu"),
            ("Email", "email"),
            ("Telefone 1", "telefone1"),
            ("Telefone 2", "telefone2"),
            ("Nascimento", "data_nascimento"),
            ("Estado Civil", "estado_civil")
        ]
        for i, (label, key) in enumerate(campos_pessoais):
            ttk.Label(self.secao_pessoal, text=label).grid(row=i, column=0, sticky=W, pady=4)
            if key == "sexo":
                self.vars[key] = ttk.Combobox(self.secao_pessoal, values=["Masculino", "Feminino"], state="readonly", width=30)
            elif key == "estado_civil":
                self.vars[key] = ttk.Combobox(self.secao_pessoal, values=["Solteiro", "Casado", "Divorciado"], state="readonly", width=30)
            elif key in ["formacao", "lingua_bantu"]:
                valores = self.carregar_valores(key)
                self.vars[key] = ttk.Combobox(self.secao_pessoal, values=valores, state="normal", width=30)
                self.vars[key].bind("<FocusOut>", lambda e, cb=self.vars[key], k=key: self.adicionar_item_e_salvar(cb, cb.get(), k))
            elif key == "data_nascimento":
                self.vars[key] = DateEntry(self.secao_pessoal, bootstyle="secondary", width=20)
            else:
                self.vars[key] = ttk.Entry(self.secao_pessoal, width=30)
            self.vars[key].grid(row=i, column=1, pady=4)

        self.detalhes = ttk.LabelFrame(self.secao_pessoal, text="📋 Detalhes", padding=10)
        self.detalhes.grid(row=0, column=2, rowspan=9,padx=10, pady=10, sticky="nsew")
        campos_detalhes = [
            ("Endereco", "endereco"),
            ("Prov-Residencia", "provincia"),
            ("Rua/Bairro/cidade", "rua_bairro"),
            ("Codigo Postal", "codigo_postal"),
            ("Camisete", "camisete")
        ]

        for i, (label, key) in enumerate(campos_detalhes):
            ttk.Label(self.detalhes, text=label).grid(row=i, column=0, sticky=W, pady=4)
            if key == "provincia":
                self.vars[key] = ttk.Combobox(self.detalhes, values=["Maputo","Sofala","Nampula","Manica","Tete","Niassa",
                                                                     "Cabo Delgado","Inhambane","Gaza","Zambezia"], state="readonly", width=30)
            elif key == "camisete":
                self.vars[key] = ttk.Combobox(self.detalhes, values=["S", "M", "L", "XL", "XXL"], state="readonly", width=10)
            else:
                self.vars[key] = ttk.Entry(self.detalhes, width=30)
            self.vars[key].grid(row=i, column=1, pady=4)

        # 📌 Campos Institucionais
        ttk.Label(self.secao_institucional, text="Código (auto)").grid(row=0, column=0, sticky=W, pady=4)
        self.vars["codigo"] = ttk.Entry(self.secao_institucional, width=30, state="disabled")
        self.vars["codigo"].grid(row=0, column=1, pady=4)

        ttk.Label(self.secao_institucional, text="Cargo").grid(row=1, column=0, sticky=W, pady=4)
        self.vars["cargo"] = ttk.Entry(self.secao_institucional, width=30)
        self.vars["cargo"].grid(row=1, column=1, pady=4)

        ttk.Label(self.secao_institucional, text="Tipo").grid(row=2, column=0, sticky=W, pady=4)
        self.vars["tipo"] = ttk.Combobox(self.secao_institucional, values=["admin", "membro", "prestador"], state="readonly", width=25)
        self.vars["tipo"].grid(row=2, column=1, pady=4)

        ttk.Label(self.secao_institucional, text="Ingresso").grid(row=3, column=0, sticky=W, pady=4)
        self.vars["data_ingresso"] = DateEntry(self.secao_institucional, bootstyle="secondary", width=20)
        self.vars["data_ingresso"].grid(row=3, column=1, pady=4)

        # 🧠 Geração de código automático
        codigo = gerar_codigo_institucional()
        self.vars["codigo"].config(state="normal")
        self.vars["codigo"].insert(0, codigo)
        self.vars["codigo"].config(state="disabled")

        # 🧾 Botões institucionais
        frame_botoes = ttk.Frame(self.frame)
        frame_botoes.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(frame_botoes, text="💾 Salvar", bootstyle=SUCCESS, command=self.salvar).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes, text="❌ Excluir", bootstyle=WARNING, command=self.excluir_membro).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes, text="🧹 Limpar", bootstyle=WARNING, command=self.limpar_campos).grid(row=0, column=2, padx=5)

        self.botao_editar = ttk.Button(frame_botoes, text="🔁 Editar", bootstyle=INFO, command=self.editar_membro)
        self.botao_editar.grid(row=0, column=3, padx=5)
        self.botao_editar.config(state="disabled")  

        # ⬇️ Treeview institucional
        #colunas = list(self.vars.keys()) + ["data_registro"]
        colunas = [
                "nome", "formacao", "sexo", "estado_civil", "lingua_bantu",
                "email", "telefone1", "telefone2", "data_nascimento", "endereco",
                "provincia", "rua_bairro", "codigo_postal", "camisete",
                "data_ingresso", "cargo", "tipo", "codigo", "data_registro"
            ]
        self.tree = ttk.Treeview(self.frame, columns=colunas, show="headings", bootstyle=INFO)
        for col in colunas:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100)
        self.tree.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

        scroll = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=2, column=2, sticky='ns')

        scroll_x = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=scroll_x.set)
        scroll_x.grid(row=3, column=0, columnspan=2, sticky='ew')

        # Ativação do botão de edição ao selecionar membro
        self.tree.bind("<<TreeviewSelect>>", lambda e: self.botao_editar.config(state="normal"))
        self.tree.bind("<Double-1>", lambda e: self.editar_membro())

        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.carregar_membros()

    def campos_preenchidos(self):
        obrigatorios = ["nome", "tipo", "cargo"]
        return all(self.vars[c].get().strip() for c in obrigatorios)
    
    def salvar(self):
        if not self.validar_dados():
            return
        conn = conectar()
        cursor = conn.cursor()
        # Coleta de valores com todos os campos
        valores = (
            self.vars["nome"].get(),
            self.vars["formacao"].get(),
            self.vars["sexo"].get(),
            self.vars["estado_civil"].get(),
            self.vars["lingua_bantu"].get(),
            self.vars["email"].get(),
            self.vars["telefone1"].get(),
            self.vars["telefone2"].get(),
            self.vars["data_nascimento"].get_date().isoformat(),
            self.vars["endereco"].get(),
            self.vars["provincia"].get(),
            self.vars["rua_bairro"].get(),
            self.vars["codigo_postal"].get(),
            self.vars["camisete"].get(),
            self.vars["cargo"].get(),
            self.vars["tipo"].get(),
            self.vars["data_ingresso"].get_date().isoformat()
        )

        if self.em_edicao:
            cursor.execute("""
                UPDATE pessoas SET
                    nome=?, formacao=?, sexo=?, estado_civil=?, lingua_bantu=?, email=?,
                    telefone1=?, telefone2=?, data_nascimento=?, endereco=?, provincia=?,
                    rua_bairro=?, codigo_postal=?, camisete=?, cargo=?, tipo=?, data_ingresso=?
                WHERE codigo=?
            """, valores + (self.codigo_atual,))
            conn.commit()
            messagebox.showinfo("✅ Edição", f"Membro '{valores[0]}' atualizado com sucesso.")
            self.em_edicao = False
            self.codigo_atual = None
        else:
            codigo = gerar_codigo_institucional()
            self.vars["codigo"].config(state="normal")
            self.vars["codigo"].delete(0, ttk.END)
            self.vars["codigo"].insert(0, codigo)
            self.vars["codigo"].config(state="disabled")

            # Verifica duplicidade por nome
            cursor.execute("SELECT COUNT(*) FROM pessoas WHERE nome = ?", (self.vars["nome"].get(),))
            if cursor.fetchone()[0] > 0:
                messagebox.showwarning("🟡 Duplicidade", "Já existe um membro com esse nome.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO pessoas (
                    nome, formacao, sexo, estado_civil, lingua_bantu, email,
                    telefone1, telefone2, data_nascimento, endereco, provincia,
                    rua_bairro, codigo_postal, camisete, cargo, tipo,
                    data_ingresso, data_registro, codigo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, valores + (datetime.datetime.now().isoformat(), codigo))
            conn.commit()

        conn.close()
        self.carregar_membros()
        self.limpar_campos()

    def carregar_membros(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nome, formacao, sexo, estado_civil, lingua_bantu, email, telefone1, telefone2,
                data_nascimento, endereco, provincia, rua_bairro, codigo_postal, camisete,
                data_ingresso, cargo, tipo, codigo, data_registro
            FROM pessoas
        """)
        for row in cursor.fetchall():
            dados_formatados = []
            for i, valor in enumerate(row):
                if i in [7, 8, 12]:  # índices das colunas de data
                    try:
                        if isinstance(valor, str):
                            valor = valor.split("T")[0]  # remove T00:00:00
                            valor = datetime.datetime.strptime(valor, "%Y-%m-%d").strftime("%d/%m/%Y")
                        elif isinstance(valor, (datetime.datetime, datetime.date)):
                            valor = valor.strftime("%d/%m/%Y")
                    except:
                        pass
                dados_formatados.append(valor)
            self.tree.insert("", "end", values=dados_formatados)

        conn.close()

    def limpar_campos(self):
        for key, widget in self.vars.items():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, END)
            elif isinstance(widget, ttk.Combobox):
                widget.set("")
            elif isinstance(widget, DateEntry):
                widget.set_date(datetime.date.today())
        self.secao_institucional.config(bootstyle="default")  # ou outro estilo institucional

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

    def membro_selecionado(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Seleção", "Selecione um membro na lista.")
            return None
        self.botao_editar.config(state="normal")
        return self.tree.item(item)["values"]  

    def editar_membro(self):
        self.secao_institucional.config(bootstyle="warning")
        dados = self.membro_selecionado()
        if not dados:
            return
        # --- Índices conforme SELECT ---
        # [0] nome
        self.vars["nome"].delete(0, ttk.END)
        self.vars["nome"].insert(0, dados[0])

        # [1] formacao
        self.vars["formacao"].set(dados[1])

        # [2] sexo
        self.vars["sexo"].set(dados[2])

        # [3] estado_civil
        self.vars["estado_civil"].set(dados[3])

        # [4] lingua_bantu
        self.vars["lingua_bantu"].set(dados[4])

        # [5] email
        self.vars["email"].delete(0, ttk.END)
        self.vars["email"].insert(0, dados[5])

        # [6] telefone1
        self.vars["telefone1"].delete(0, ttk.END)
        self.vars["telefone1"].insert(0, dados[6])

        # [7] telefone2
        self.vars["telefone2"].delete(0, ttk.END)
        self.vars["telefone2"].insert(0, dados[7])

        # [8] data_nascimento
        data_nascimento = dados[8].split("T")[0]
        self.vars["data_nascimento"].set_date(datetime.datetime.strptime(data_nascimento, "%d/%m/%Y"))

        # [9] endereco
        self.vars["endereco"].delete(0, ttk.END)
        self.vars["endereco"].insert(0, dados[9])

        # [10] provincia
        self.vars["provincia"].set(dados[10])

        # [11] rua_bairro
        self.vars["rua_bairro"].delete(0, ttk.END)
        self.vars["rua_bairro"].insert(0, dados[11])

        # [12] codigo_postal
        self.vars["codigo_postal"].delete(0, ttk.END)
        self.vars["codigo_postal"].insert(0, dados[12])

        # [13] camisete
        self.vars["camisete"].set(dados[13])

        # [14] data_ingresso
        data_ingresso = dados[14].split("T")[0]
        # Converte ISO para formato desejado antes de usar no set_date
        data_formatada = datetime.datetime.strptime(data_ingresso, "%Y-%m-%d")
        self.vars["data_ingresso"].set_date(data_formatada)
        # [15] cargo
        self.vars["cargo"].delete(0, ttk.END)
        self.vars["cargo"].insert(0, dados[15])

        # [16] tipo
        self.vars["tipo"].set(dados[16])

        # [17] codigo
        self.vars["codigo"].config(state="normal")
        self.vars["codigo"].delete(0, ttk.END)
        self.vars["codigo"].insert(0, dados[17])
        self.vars["codigo"].config(state="disabled")

        # Estado de edição
        self._modo_edicao = True
        self.codigo_atual = dados[17]
        messagebox.showinfo("Edição", f"Membro '{dados[0]}' carregado para edição.")

    def excluir_membro(self):
        if not self.codigo_atual:
            messagebox.showwarning("⚠️ Exclusão", "Nenhum membro em edição selecionado.")
            return
        membro_nome = self.vars["nome"].get()
        resposta = messagebox.askyesno(
            "🗑️ Confirmar exclusão",
            f"Deseja realmente excluir o membro '{membro_nome}' (Código: {self.codigo_atual})?"
        )
        if not resposta:
            return
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM pessoas WHERE codigo=?", (self.codigo_atual,))
                conn.commit()
            messagebox.showinfo("✅ Exclusão", f"Membro '{membro_nome}' removido com sucesso.")
            self.recarregar_treeview()
            self.limpar_campos()
            self.em_edicao = False
            self.codigo_atual = None
            self.secao_institucional.config(bootstyle="default")
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Ocorreu um problema ao excluir: {e}")

    def recarregar_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.carregar_membros()

    def validar_dados(self):
        if not self.campos_preenchidos():
            messagebox.showwarning("⚠️ Campos obrigatórios", "Preencha todos os campos obrigatórios.")
            return False
        erros = []
        # Validação da data de nascimento
        try:
            nascimento = self.vars["data_nascimento"].get_date()
            if not Validador.validar_data(nascimento):
                erros.append("🚫 Data de nascimento inválida. Deve estar no passado.")
        except ValueError:
            erros.append("❌ Formato inválido. Use o formato DD/MM/AAAA.")

        # Validação de e-mail
        email = self.vars["email"].get()
        if email and not Validador.validar_email(email):
            erros.append("📧 E-mail inválido. Verifique o formato.")

        # Validação de telefones
        for campo in ["telefone1", "telefone2"]:
            telefone = self.vars[campo].get()
            if telefone and not Validador.validar_telefone(telefone):
                erros.append(f"📱 '{campo}' deve conter ao menos 7 dígitos e ser numérico.")

        # Validação de código postal
        codigo_postal = self.vars["codigo_postal"].get()
        if codigo_postal and not Validador.validar_codigo_postal(codigo_postal):
            erros.append("🏷️ Código postal inválido. Use apenas números.")

        if erros:
            messagebox.showerror("Validação de Dados", "\n".join(erros))
            return False

        return True

    @property
    def em_edicao(self):
        return getattr(self, "_modo_edicao", False)

    @em_edicao.setter
    def em_edicao(self, valor):
        self._modo_edicao = bool(valor)



import tkinter as tk

class ComboboxPadronizado(ttk.Frame):
    def __init__(self, master, label_text, values, var=None, width=30):
        super().__init__(master)
        
        self.var = var or tk.StringVar()
        
        # Label institucional
        self.label = ttk.Label(self, text=label_text, anchor="w")
        self.label.grid(row=0, column=0, sticky="w", pady=(0, 2))
        
        # Combobox visual padronizado
        self.combo = ttk.Combobox(self, textvariable=self.var, values=values, width=width)
        self.combo.grid(row=1, column=0, sticky="ew")
        self.combo.state(["readonly"])
        
        # Salvamento automático de novos valores
        self.combo.bind("<FocusOut>", self.salvar_valor_novo)
        
        self.grid_columnconfigure(0, weight=1)

    def salvar_valor_novo(self, event=None):
        valor = self.var.get()
        if valor and valor not in self.combo['values']:
            valores = list(self.combo['values'])
            valores.append(valor)
            self.combo['values'] = valores
            print(f"Novo valor adicionado: {valor}")  # pode virar log institucional

    def get(self):
        return self.var.get()

    def set(self, value):
        self.var.set(value)