# core/dashboard.py
from ttkbootstrap import *
from core.logs_acesso import TelaLogs
from core.membros_rh.cadastro_membros import TelaGestaoMembros
from core.backup import TelaBackup
from tkinter import LEFT, RIGHT, X, BOTH
from widgets.cards import criar_card_indicador


class TelaDashboard:
    def __init__(self, root, tipo, login_usuario, ao_navegar):
        self.root = root
        self.tipo = tipo
        self.login_usuario = login_usuario
        self.ao_navegar = ao_navegar

        self.frame = Frame(root, padding=30)
        self.frame.pack(side=RIGHT, fill=BOTH, expand=True)
         # 🎯 Container visual das seções institucionais
        self.secao_dados = Frame(self.frame)
        self.secao_dados.pack(fill=BOTH, expand=True)


        self.criar_cabecalho()
        self.criar_indicadores()
        self.criar_agenda()
        self.criar_tarefas()


    def abrir_logs(self):
        self.frame.destroy()
        TelaLogs(self.secao_dados)

    def abrir_gestor_usuarios(self):
        self.frame.destroy()
        TelaGestaoMembros(self.secao_dados)

    def abrir_backup(self):
        self.frame.destroy()
        TelaBackup(self.secao_dados)


    def criar_cabecalho(self):
        Label(self.secao_dados, text="NexuGest | Painel Institucional", font=("Arial", 18, "bold")).pack()
        Label(self.secao_dados, text=f"🔄 Sessão ativa: {self.login_usuario.title()} ({self.tipo})", font=("Arial", 10, "italic")).pack(pady=(0, 10))

    def criar_indicadores(self):
        linha_cards = Frame(self.secao_dados)
        linha_cards.pack(fill=X)

        criar_card_indicador(linha_cards, valor="12", texto="Usuários ativos", icone="👥")
        criar_card_indicador(linha_cards, valor="6", texto="Serviços pendentes", icone="🧾")
        criar_card_indicador(linha_cards, valor="3", texto="Backups semanais", icone="📦")
    
    def criar_agenda(self):
        Label(self.secao_dados, text="🗓️ Agenda institucional (simulada)", bootstyle="info", font=("Arial", 12, "bold")).pack(anchor="w", pady=(15, 5))

        agenda = Treeview(self.secao_dados, columns=("hora", "evento"), bootstyle="warning", show="headings")
        agenda.heading("hora", text="Horário")
        agenda.heading("evento", text="Atividade")

        eventos = [("09:00", "Login de gestor 'Mário'"), ("11:30", "Backup agendado"), ("15:00", "Exportação de relatórios")]

        for e in eventos:
            agenda.insert("", "end", values=e)

        agenda.pack(fill=X)


    def criar_tarefas(self):
        Label(self.secao_dados, text="📍 Tarefas de hoje", font=("Arial", 12, "bold")).pack(anchor="w", pady=(15, 5))

        tarefas = Treeview(self.secao_dados, columns=("descricao",), show="headings", height=5)
        tarefas.heading("descricao", text="Descrição")
        tarefas.column("descricao", anchor="w")

        tarefas_dia = [
            "✓ Revisar logins e acessos",
            "📦 Gerar backup manual",
            "⏳ Validar permissões 'gestor'",
            "🔁 Atualizar painel de relatórios",
            "🧾 Exportar estatísticas de uso"
        ]

        for item in tarefas_dia:
            tarefas.insert("", "end", values=(item,))

        tarefas.pack(fill=X)


