
from ttkbootstrap import Window
from core.splash import TelaSplash
from core.login import TelaLogin
from core.roteador import navegar_para, cache_telas
from utils.session import obter_sessao, limpar_sessao
from utils.logs import log_acesso
from db.conexao import verificar_banco
from db.modelos import criar_tabela_usuarios, criar_tabelas, inicializar_listas_institucionais
from db.user0 import criar_usuario_teste
from db.migracoes import migrar_banco_completo

# 🧠 Variáveis institucionais globais de sessão
nivel = None  # Nível do usuário logado
login = None  # Nome do usuário logado

def mostrar_dashboard(nivel_usuario, login_usuario):
    """Exibe o dashboard principal após login bem-sucedido e ajusta o tamanho da janela."""
    global nivel, login
    nivel = nivel_usuario
    login = login_usuario
    # Redimensiona e centraliza para o tamanho padrão do app
    centralizar_janela(root, largura=1080, altura=800)
    log_acesso(login)
    navegar_para(root, login, nivel, "dashboard", ao_logout=logout)  # 🔄 Usa o roteador institucional


def mostrar_login():
    """Exibe a tela de login institucional com janela compacta e centralizada."""
    for w in root.winfo_children():
        w.destroy()
    # Redimensiona e centraliza para tela de login pequena
    centralizar_janela(root, largura=400, altura=350)
    TelaLogin(root, ao_logar=mostrar_dashboard)


def iniciar_app():
    """Inicia o app mostrando a tela splash e depois o login."""
    TelaSplash(root, ao_carregar=mostrar_login)



def logout():
    """Realiza logout do usuário, limpando sessão e cache."""
    global nivel, login
    nivel = None
    login = None
    try:
        limpar_sessao()  # 🔒 Limpa a sessão persistente
    except Exception as e:
        print(f"Erro ao limpar sessão: {e}")
    try:
        cache_telas.clear()  # 🧹 Limpa o cache de telas
    except Exception as e:
        print(f"Erro ao limpar cache de telas: {e}")
    mostrar_login()  # 🔄 Volta à tela de login institucional


def centralizar_janela(janela, largura=1080, altura=800):
    """Centraliza a janela principal na tela."""
    janela.update_idletasks()  # garante medidas atualizadas
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    pos_x = (largura_tela // 2) - (largura // 2)
    pos_y = (altura_tela // 2) - (altura // 2)
    janela.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")


inicializar_listas_institucionais()
sessao = obter_sessao()

# 🖥️ Inicialização principal
if __name__ == "__main__":
    try:
        root = Window(themename="cosmo")
        centralizar_janela(root)
        verificar_banco()
        criar_tabelas()
        inicializar_listas_institucionais()
        criar_tabela_usuarios()
        criar_usuario_teste()
        migrar_banco_completo()
        sessao = obter_sessao()
        if sessao:
            print(f"🧠 Último login foi: {sessao['usuario']} ({sessao['nivel']})")
            mostrar_dashboard(nivel_usuario=sessao["nivel"], login_usuario=sessao["usuario"])
        else:
            iniciar_app()
        root.mainloop()
    except Exception as e:
        print(f"Erro na inicialização do aplicativo: {e}")
