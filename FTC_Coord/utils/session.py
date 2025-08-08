# utils/session.py
import json, datetime, os

def salvar_sessao(usuario, nivel):
    pasta = "session"
    os.makedirs(pasta, exist_ok=True)  # cria a pasta se ainda não existir

    dados = {
        "usuario": usuario,
        "nivel": nivel,
        "data": datetime.datetime.now().isoformat()
    }
    with open("session/ultimo_login.json", "w", encoding="utf-8") as f:
        json.dump(dados, f)

def obter_sessao():
    try:
        with open("session/ultimo_login.json", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None


def limpar_sessao():
    if os.path.exists("session.txt"):
        os.remove("session.txt")
