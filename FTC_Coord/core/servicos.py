from ttkbootstrap import *
from core.cadastro_servicos import CadastroServico
from core.consulta_service import ConsultaServicos


class TelaServicos:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root)
        self.frame.pack(fill=BOTH, expand=True)

        tabs = Notebook(self.frame)
        tabs.pack(fill=BOTH, expand=True, padx=10, pady=10)

        tab_cadastro = Frame(tabs)
        CadastroServico(tab_cadastro)
        tabs.add(tab_cadastro, text="Cadastrar Serviço")

        tab_consulta = Frame(tabs)
        ConsultaServicos(tab_consulta)
        tabs.add(tab_consulta, text="Consultar Serviços")