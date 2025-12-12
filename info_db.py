import sqlite3

conn = sqlite3.connect("tabela_periodica.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(elementos)")
columns = cursor.fetchall()

for col in columns:
    print(col)

conn.close()

