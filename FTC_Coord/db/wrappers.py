



def vincular_membro_servico(db_path, servico_id, membro_id, papel, observacao=''):
    import sqlite3
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO servico_membros (servico_id, membro_id, papel, observacao)
        VALUES (?, ?, ?, ?)
    ''', (servico_id, membro_id, papel, observacao))

    conn.commit()
    conn.close()

    