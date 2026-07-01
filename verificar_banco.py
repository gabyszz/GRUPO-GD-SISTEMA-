import sqlite3

conn = sqlite3.connect("topografia.db")
cursor = conn.cursor()

print("\nTABELAS\n")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

for tabela in cursor.fetchall():

    nome = tabela[0]

    print(f"\n===== {nome} =====")

    cursor.execute(f"PRAGMA table_info({nome})")

    for coluna in cursor.fetchall():

        print(coluna)

conn.close()