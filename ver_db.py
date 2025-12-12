import sqlite3

conn = sqlite3.connect("tabela_periodica.db")
cursor = conn.cursor()

cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
schema = cursor.fetchall()

for table, ddl in schema:
    print(f"--- Tabela: {table} ---")
    print(ddl)
    print()

conn.close()

