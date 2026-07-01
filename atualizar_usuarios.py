import sqlite3

conn = sqlite3.connect("topografia.db")
cursor = conn.cursor()

colunas = [
    ("data_criacao", "DATETIME"),
    ("ultimo_login", "DATETIME"),
    ("ultimo_acesso", "DATETIME"),
    ("foto", "VARCHAR(255)"),
    ("telefone", "VARCHAR(20)"),
    ("observacoes", "TEXT")
]

cursor.execute("PRAGMA table_info(usuarios)")
existentes = [c[1] for c in cursor.fetchall()]

for nome, tipo in colunas:

    if nome not in existentes:

        print(f"Criando coluna: {nome}")

        cursor.execute(
            f"ALTER TABLE usuarios ADD COLUMN {nome} {tipo}"
        )

conn.commit()
conn.close()

print("\nBanco atualizado com sucesso!")