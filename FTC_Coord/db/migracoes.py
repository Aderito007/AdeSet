
from db.conexao import conectar


def migrar_tabela_pessoas():
    conn = conectar()
    cursor = conn.cursor()

    # Lista das colunas que devem existir
    colunas_necessarias = {
        "codigo": "TEXT UNIQUE",
        "formacao": "TEXT",
        "sexo": "TEXT",
        "lingua_bantu": "TEXT",
        "telefone1": "TEXT",
        "telefone2": "TEXT",
        "data_nascimento": "TEXT",
        "data_ingresso": "TEXT"
    }

    # Recupera colunas atuais da tabela
    cursor.execute("PRAGMA table_info(pessoas)")
    colunas_existentes = [coluna[1] for coluna in cursor.fetchall()]

    # Adiciona colunas faltantes
    for nome, tipo in colunas_necessarias.items():
        if nome not in colunas_existentes:
            try:
                cursor.execute(f"ALTER TABLE pessoas ADD COLUMN {nome} {tipo}")
                print(f"🟢 Coluna adicionada: {nome}")
            except Exception as e:
                print(f"🔴 Erro ao adicionar coluna {nome}: {e}")

    conn.commit()
    conn.close()

def migrar_login_em_pessoas():
    conn = conectar()
    cursor = conn.cursor()

    # Obter colunas atuais
    cursor.execute("PRAGMA table_info(pessoas)")
    colunas = [col[1] for col in cursor.fetchall()]

    # Lista completa de novas colunas
    novas_colunas = {
        "usuario": "TEXT",
        "senha": "TEXT",
        "estado_civil": "TEXT",
        "endereco": "TEXT",
        "provincia": "TEXT",
        "rua_bairro": "TEXT",
        "codigo_postal": "TEXT",
        "camisete": "TEXT"
    }
    # Verifica e adiciona cada coluna individualmente
    for nome, tipo in novas_colunas.items():
        if nome not in colunas:
            try:
                cursor.execute(f"ALTER TABLE pessoas ADD COLUMN {nome} {tipo}")
                print(f"🟢 Coluna adicionada: {nome}")
            except Exception as e:
                print(f"🔴 Erro ao adicionar coluna {nome}: {e}")

    conn.commit()
    conn.close()


def migrar_tabela_servicos():
    conn = conectar()
    cursor = conn.cursor()

    colunas_necessarias = {
        "actividade": "TEXT",
        "servico_adjudicado": "TEXT",
        "local_trabalho": "TEXT"
    }

    cursor.execute("PRAGMA table_info(servicos)")
    colunas_existentes = [col[1] for col in cursor.fetchall()]

    for nome, tipo in colunas_necessarias.items():
        if nome not in colunas_existentes:
            try:
                cursor.execute(f"ALTER TABLE servicos ADD COLUMN {nome} {tipo}")
                print(f"🟢 Coluna adicionada: {nome}")
            except Exception as e:
                print(f"🔴 Erro ao adicionar coluna {nome}: {e}")

    conn.commit()
    conn.close()



def migrar_banco_completo():
    print("🔁 Iniciando migração institucional...")

    try:
        migrar_tabela_pessoas()
        print("✅ Migração de tabela 'pessoas' concluída.")
    except Exception as e:
        print(f"❌ Erro ao migrar tabela 'pessoas': {e}")

    try:
        migrar_login_em_pessoas()
        print("✅ Campos adicionais de login e perfil aplicados.")
    except Exception as e:
        print(f"❌ Erro ao aplicar campos de login/perfil: {e}")

    try:
        migrar_tabela_servicos()
        print("✅ Migração de tabela 'servicos' concluída.")
    except Exception as e:
        print(f"❌ Erro ao migrar tabela 'servicos': {e}")

    print("🏁 Migração concluída.")
