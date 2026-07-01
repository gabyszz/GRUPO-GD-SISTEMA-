import os


class Config:

    # Chave utilizada para sessões, login e segurança
    SECRET_KEY = "GDTopografia@2026"

    # Caminho absoluto da pasta do projeto
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # Banco de dados SQLite
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "topografia.db")

    # Desabilita aviso do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False