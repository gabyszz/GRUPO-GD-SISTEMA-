import os


class Config:

    # Chave utilizada para sessões, login e segurança
    SECRET_KEY = "GDTopografia@2026"

    # Caminho absoluto da pasta do projeto
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Banco de dados PostgreSQL
    SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://postgres:Gd%40102030@localhost:5432/gd_topografia"
)
    # Desabilita aviso do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False