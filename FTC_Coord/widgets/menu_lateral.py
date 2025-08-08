# widgets/menu_lateral.py
from ttkbootstrap import *

# widgets/menu_lateral.py
class MenuLateralFixado:
    """
    Menu lateral fixo institucional com controle de acesso por tipo de usuário.
    """
    def __init__(self, root, ao_navegar, ao_logout, usuario, tipo):
        """
        Cria o menu lateral com botões de navegação e logout.
        :param root: widget pai
        :param ao_navegar: função chamada ao clicar em um botão de módulo
        :param ao_logout: função chamada ao clicar em logout
        :param usuario: nome do usuário
        :param tipo: tipo do usuário (admin, gestor, etc)
        """

        # Cor de fundo personalizada
        cor_fundo = "#232946"  # Exemplo: azul escuro institucional
        style = Style()
        style.configure("MenuLateral.TFrame", background=cor_fundo)

        self.frame = Frame(root, padding=10, width=160, style="MenuLateral.TFrame")
        self.frame.pack(side=LEFT, fill=Y)
        # Fallback para cor de fundo caso o style não funcione
        try:
            self.frame.configure(bg=cor_fundo)
        except Exception:
            pass
        print("[DEBUG] Menu lateral instanciado e exibido.")

        Label(self.frame, text="📌 NexuGest", font=("Arial", 14, "bold")).pack(pady=8)
        Label(self.frame, text=f"👤 {usuario.title()} ({tipo})", font=("Arial", 10)).pack()

        self.botoes = [
            {"texto": "🏠 Dashboard", "modulo": "dashboard"},
            {"texto": "👥 Membros", "modulo": "membros", "tipo": "admin"},
            {"texto": "📜 Logs de Acesso", "modulo": "logs", "tipo": "admin"},
            {"texto": "📦 Backup", "modulo": "backup", "tipo": "admin"},
            {"texto": "🧾 Serviços", "modulo": "servicos", "tipo": "gestor"},
            {"texto": "⚙️ Configurações", "modulo": "config", "tipo": "admin"},
        ]

        # Evita botões duplicados por módulo
        modulos_adicionados = set()
        for btn in self.botoes:
            if btn["modulo"] in modulos_adicionados:
                continue
            modulos_adicionados.add(btn["modulo"])
            permitido = self.usuario_tem_acesso(btn.get("tipo"), tipo)
            botao = Button(
                self.frame,
                text=f"   {btn['texto']}",  # simula alinhamento à esquerda
                width=22,
                command=lambda m=btn["modulo"]: ao_navegar(m)
            )
            botao.pack(fill="x", padx=8, pady=4)
            if not permitido:
                botao.configure(state="disabled")

        # 🚪 Botão de logout institucional
        Button(self.frame, text="🚪 Logout", bootstyle="danger", command=ao_logout).pack(pady=(30, 10))

    @staticmethod
    def usuario_tem_acesso(modulo_tipo, tipo_usuario):
        """
        Verifica se o usuário tem acesso ao módulo.
        :param modulo_tipo: tipo exigido pelo módulo
        :param tipo_usuario: tipo do usuário logado
        :return: True se permitido, False caso contrário
        """
        return tipo_usuario == "admin" or modulo_tipo is None or modulo_tipo == tipo_usuario
    