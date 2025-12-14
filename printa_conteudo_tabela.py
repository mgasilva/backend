import sqlite3

def listar_tabela(nome_banco, nome_tabela):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    # Verifica se a tabela existe
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name=?
    """, (nome_tabela,))
    
    if cursor.fetchone() is None:
        print(f"⚠️ A tabela '{nome_tabela}' não existe no banco de dados.")
        conn.close()
        return

    # Busca os dados
    cursor.execute(f"SELECT * FROM {nome_tabela}")
    linhas = cursor.fetchall()

    # Busca os nomes das colunas
    colunas = [desc[0] for desc in cursor.description]

    print(f"\n📌 Conteúdo da tabela '{nome_tabela}':")
    print("-" * 60)
    print(" | ".join(colunas))
    print("-" * 60)

    for linha in linhas:
        print(" | ".join(str(c) for c in linha))

    print("-" * 60)
    print(f"Total de linhas: {len(linhas)}")

    conn.close()

# Exemplo de uso:

listar_tabela("tabela_periodica.db", "informacoes")
