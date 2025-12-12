import sqlite3

conn = sqlite3.connect("tabela_periodica.db")
cursor = conn.cursor()

cursor.execute(
        """INSERT INTO informacoes (numero_atomico, info) 
		VALUES (26, 'Encontra-se no núcleo das hemoglobinas e enzimas redox.');""")

cursor.execute(
        """INSERT INTO informacoes (numero_atomico, info) 
		VALUES (1, 'https://pt.wikipedia.org/wiki/Hidrog%C3%AAnio');""")

conn.commit()

conn.close()

