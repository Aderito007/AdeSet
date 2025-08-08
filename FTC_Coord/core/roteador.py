# core/roteador.py
from widgets.menu_lateral import MenuLateralFixado
from core.dashboard import TelaDashboard
from core.logs_acesso import TelaLogs
from core.backup import TelaBackup
from ttkbootstrap import Label, Frame
from core.membros_rh.cadastro_membros import TelaGestaoMembros
from core.servicos import TelaServicos


# 🔁 Cache institucional de telas já carregadas
cache_telas = {}

def navegar_para(root, login, nivel, modulo, ao_logout):
    """
    Navega para o módulo/tela desejado, limpando a janela e renderizando o menu lateral.
    Armazena a tela criada no cache (ainda não reutiliza o cache).
    """
    # Limpa todos os elementos da janela (compatível com versões mais novas)
    for w in root.winfo_children():
        w.destroy()

    # 🧭 Renderiza menu lateral fixo institucional
    try:
        MenuLateralFixado(
            root,
            ao_navegar=lambda m: navegar_para(root, login, nivel, m, ao_logout),
            ao_logout=ao_logout,
            usuario=login,
            tipo=nivel
        )
    except Exception as e:
        print(f"Erro ao renderizar menu lateral: {e}")

    # 🧠 Criação da tela conforme o módulo
    try:
        match modulo:
            case "dashboard":
                nova_tela = TelaDashboard(
                    root,
                    tipo=nivel,
                    login_usuario=login,
                    ao_navegar=lambda m: navegar_para(root, login, nivel, m, ao_logout)
                )
            case "membros":
                nova_tela = TelaGestaoMembros(root)
            case "logs":
                nova_tela = TelaLogs(root)
            case "backup":
                nova_tela = TelaBackup(root)
            case "servicos":
                nova_tela = TelaServicos(root)
            case _:
                nova_tela = Frame(root)
                Label(nova_tela, text="🚧 Página em construção").pack()
                nova_tela.pack(fill="both", expand=True)
    except Exception as e:
        nova_tela = Frame(root)
        Label(nova_tela, text=f"Erro ao carregar módulo '{modulo}': {e}").pack()
        nova_tela.pack(fill="both", expand=True)

    # 💾 Armazena nova tela no cache (ainda não reutiliza, mas pode ser implementado)
    cache_telas[modulo] = nova_tela
