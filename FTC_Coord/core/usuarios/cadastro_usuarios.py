# core/cadastro_usuarios.py
from ttkbootstrap import *
from db.conexao import conectar
import datetime
from ttkbootstrap.dialogs import Messagebox
from widgets.campo_senha import CampoSenhaTTK


class CadastroUsuario:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root, padding=30)
        self.frame.pack(fill=BOTH, expand=True)

        Label(self.frame, text="Cadastro de Usuário do Sistema", font=("Arial", 16)).pack(pady=10)

        campos = {
            "Nome completo": "nome",
            "Nome de usuário (login)": "usuario",
            "Senha": "senha",
            "Email (opcional)": "email",
            "Nível de acesso": "nivel"
        }

        self.inputs = {}

        for label, key in campos.items():
            Label(self.frame, text=label).pack(anchor="w")
            if key == "senha":
                entry = CampoSenhaTTK(self.frame)
            elif key == "nivel":
                entry = Combobox(self.frame, values=["admin", "gestor"])
            else:
                entry = Entry(self.frame)
            entry.pack(fill=X, pady=4)
            self.inputs[key] = entry

        Button(self.frame, text="Cadastrar", bootstyle="success", command=self.salvar).pack(pady=10)

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO usuarios_sistema (
                    nome, usuario, senha, email, nivel, data_criacao
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.inputs["nome"].get(),
                self.inputs["usuario"].get(),
                self.inputs["senha"].get(),
                self.inputs["email"].get(),
                self.inputs["nivel"].get(),
                datetime.datetime.now().isoformat()
            ))
            conn.commit()
            Messagebox.show_info("Usuário cadastrado com sucesso.")
        except Exception as e:
            Messagebox.show_error(f"Erro: {e}")
        finally:
            conn.close()

