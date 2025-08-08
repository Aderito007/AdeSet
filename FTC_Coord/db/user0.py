from db.conexao import conectar

def criar_usuario_teste():
    conn = conectar()
    cursor = conn.cursor()

    nome = "Usuário de Testes"
    usuario = "teste"
    senha = "1234"
    nivel = "admin"     # ou "admin"
    email = "teste@nexugest.org"

    try:
        cursor.execute('''
            INSERT INTO usuarios_sistema (
                nome, usuario, senha, nivel, email, ativo, data_criacao
            ) VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (
            nome, usuario, senha, nivel, email, 1
        ))
        conn.commit()
        print("🟢 Usuário de teste criado com sucesso.")
    except Exception as e:
        print(f"🔴 Erro ao criar usuário: {e}")
    finally:
        conn.close()