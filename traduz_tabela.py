import sqlite3

# Conexão
conn = sqlite3.connect("tabela_periodica.db")
cursor = conn.cursor()

# Dicionário de tradução
traducao = {
    "alkali metal": "metal alcalino",
    "alkaline earth metal": "metal alcalino-terroso",
    "transition metal": "metal de transição",
    "post-transition metal": "metal pós-transição",
    "lanthanide": "lantanídeo",
    "actinide": "actinídeo",
    "metalloid": "semimetal",
    "nonmetal": "não-metal",
    "noble gas": "gás nobre",
    "halogen": "halogênio"
}

# Atualizar todas as linhas
for categoria_en, categoria_pt in traducao.items():
    cursor.execute("""
        UPDATE elementos
        SET categoria = ?
        WHERE categoria = ?;
    """, (categoria_pt, categoria_en))

conn.commit()
conn.close()

print("Traduções aplicadas com sucesso!")

