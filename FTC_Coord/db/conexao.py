# db/conexao.py
import sqlite3, os, sys

def get_base_path():
    if hasattr(sys, "_MEIPASS"):
        # Executável empacotado (PyInstaller)
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def get_db_path():
    raiz = os.path.dirname(os.path.abspath(sys.argv[0]))  # raiz onde está o main.py ou o .exe
    caminho = os.path.join(raiz, "db", "nexugest.db")
    return caminho

def conectar():
    caminho_db = get_db_path()
    return sqlite3.connect(caminho_db)
# db/conexao.py (continuação)
def verificar_banco():
    caminho = get_db_path()
    if not os.path.exists(caminho):
        print(f"⚠️ Banco de dados não encontrado em: {caminho}")
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w") as f: pass  # cria arquivo vazio
        print("🟢 Banco criado. É necessário executar criação de tabelas.")
    else:
        print(f"✅ Banco de dados localizado em: {caminho}")
