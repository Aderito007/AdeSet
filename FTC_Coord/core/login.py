# core/login.py
from ttkbootstrap import *
from widgets.campo_senha import CampoSenhaTTK
from ttkbootstrap.dialogs import Messagebox
from db.conexao import conectar
from utils.session import salvar_sessao, obter_sessao



class TelaLogin:
    def __init__(self, root, ao_logar):
        self.root = root
        self.ao_logar = ao_logar
        self.frame = Frame(root, padding=30)
        self.frame.pack()

        Label(self.frame, text="Usuário").pack(anchor="w")
        self.usuario = Entry(self.frame)
        self.usuario.pack(fill=X, pady=8)

        #Label(self.frame, text="Senha").pack()
        self.senha = CampoSenhaTTK(self.frame, texto="Senha:")
        self.senha.pack(fill=X, pady=8)

        sessao = obter_sessao()
        if sessao:
            self.usuario.insert(0, sessao["usuario"])
            Label(self.frame, text=f"Último login: {sessao['usuario']}").pack(pady=(0, 5))

        Button(self.frame, text="Entrar", bootstyle="success", command=self.validar).pack(pady=10)

    def validar(self):
        usuario_input = self.usuario.get().strip()
        senha_input = self.senha.get().strip()

        if not usuario_input or not senha_input:
            Messagebox.show_error("Preencha todos os campos.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT senha, nivel, ativo FROM usuarios_sistema WHERE usuario=?", (usuario_input,))
            usuario = cursor.fetchone()
            conn.close()
        except Exception as e:
            Messagebox.show_error(f"Erro ao acessar o banco de dados: {e}")
            return

        if usuario and usuario[0] == senha_input and usuario[2] == 1:
            nivel = usuario[1]
            usuario_atual = usuario_input
            try:
                salvar_sessao(usuario=usuario_atual, nivel=nivel)
            except Exception as e:
                Messagebox.show_error(f"Erro ao salvar sessão: {e}")
            self.ao_logar(nivel_usuario=nivel, login_usuario=usuario_atual)
        else:
            Messagebox.show_error("Login inválido ou usuário inativo.")
