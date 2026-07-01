import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(BASE_DIR, "topografia.db")

conn = sqlite3.connect(BANCO)
cursor = conn.cursor()


def coluna_existe(tabela, coluna):

    cursor.execute(f"PRAGMA table_info({tabela})")

    colunas = [c[1] for c in cursor.fetchall()]

    return coluna in colunas


novas_colunas = {

    "data_criacao": "DATETIME",
    "ultimo_login": "DATETIME",
    "ultimo_acesso": "DATETIME",
    "foto": "TEXT",
    "telefone": "TEXT",
    "observacoes": "TEXT"

}


for coluna, tipo in novas_colunas.items():

    if not coluna_existe("usuarios", coluna):

        print(f"Criando coluna {coluna}...")

        cursor.execute(
            f"ALTER TABLE usuarios ADD COLUMN {coluna} {tipo}"
        )

conn.commit()

conn.close()

print("\nBanco atualizado com sucesso.")