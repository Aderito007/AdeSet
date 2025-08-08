
from datetime import datetime
from db.conexao import conectar


def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,                  -- Ex: FTC2025-0001
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL,                 -- 'admin', 'membro', 'prestador'
        cargo TEXT,
        formacao TEXT,                      -- Formação ou profissão
        sexo TEXT,                          -- 'Masculino', 'Feminino'
        lingua_bantu TEXT,                  -- Ex: Macua, Sena, Changana...
        telefone1 TEXT,
        telefone2 TEXT,
        email TEXT,
        data_nascimento TEXT,
        data_ingresso TEXT,
        data_registro TEXT
    )

    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        actividade TEXT,                 -- Nome do projeto ou atividade associada
        servico_adjudicado TEXT,        -- Tipo ou nome do serviço prestado
        local_trabalho TEXT,            -- Local onde o serviço foi ou será executado
        responsavel TEXT,               -- Nome vinculado
        status TEXT,                    -- 'pendente', 'em andamento', 'concluído', etc.
        data_inicio TEXT,
        data_conclusao TEXT
    )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servico_membros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servico_id INTEGER NOT NULL,
            membro_id INTEGER NOT NULL,
            papel TEXT,                    -- 'coordenador', 'prestador', 'beneficiário'
            observacao TEXT,
            FOREIGN KEY (servico_id) REFERENCES servicos(id),
            FOREIGN KEY (membro_id) REFERENCES pessoas(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS avaliacoes_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servico_id INTEGER NOT NULL,
            avaliador_id INTEGER NOT NULL,        -- Pode ser membro ou usuário
            nota INTEGER CHECK(nota BETWEEN 1 AND 10),
            comentario TEXT,
            data_avaliacao TEXT,
            FOREIGN KEY (servico_id) REFERENCES servicos(id),
            FOREIGN KEY (avaliador_id) REFERENCES usuarios_sistema(id)
        )
    ''')

    conn.commit()
    conn.close()


def inicializar_listas_institucionais():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS listas_institucionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campo TEXT NOT NULL,
            valor TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
def gerar_codigo_unico():
    ano = datetime.now().year
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pessoas")
    total = cursor.fetchone()[0] + 1
    conn.close()
    contador_formatado = str(total).zfill(4)  # ex: '0007'
    return f"FTC{ano}{contador_formatado}"

def criar_tabela_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios_sistema (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nivel TEXT NOT NULL,        -- 'admin', 'gestor', etc.
            email TEXT,
            ativo INTEGER DEFAULT 1,
            data_criacao TEXT
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissoes_usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            modulo TEXT,                 -- 'servicos', 'avaliacoes', 'cadastro_membros', etc.
            acao TEXT,                   -- 'visualizar', 'editar', 'avaliar'
            FOREIGN KEY (usuario_id) REFERENCES usuarios_sistema(id)
            )
        ''')

    conn.commit()
    conn.close()


def gerar_codigo_institucional():
    ano_atual = datetime.now().year
    conn = conectar()
    cursor = conn.cursor()
    prefixo = "FTC"
    ano_str = str(ano_atual)
    # Conta quantos códigos já existem para esse ano
    cursor.execute("SELECT COUNT(*) FROM pessoas WHERE codigo LIKE ?", (f"{prefixo}{ano_str}%",))
    numero = cursor.fetchone()[0] + 1  # próximo número disponível
    codigo = f"{prefixo}{ano_str}-{numero:04d}"
    conn.close()
    return codigo
