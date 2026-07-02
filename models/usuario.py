from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from database.database import db


class Usuario(UserMixin, db.Model):

    __tablename__ = "usuarios"

    # ==========================
    # IDENTIFICAÇÃO
    # ==========================

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    senha = db.Column(db.String(255), nullable=False)

    # ==========================
    # PERMISSÕES
    # ==========================

    perfil = db.Column(
        db.String(50),
        nullable=False,
        default="Administrador"
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    # ==========================
    # CONTROLE
    # ==========================

    data_criacao = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    ultimo_login = db.Column(
        db.DateTime,
        nullable=True
    )

    ultimo_acesso = db.Column(
        db.DateTime,
        nullable=True
    )

    # ==========================
    # FUTURAS IMPLEMENTAÇÕES
    # ==========================

    foto = db.Column(
        db.String(255),
        nullable=True
    )

    telefone = db.Column(
        db.String(20),
        nullable=True
    )

    observacoes = db.Column(
        db.Text,
        nullable=True
    )

    # ==========================
    # SENHA
    # ==========================

    def definir_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)

    # ==========================
    # LOGIN
    # ==========================

    def registrar_login(self):

        agora = datetime.utcnow()

        self.ultimo_login = agora
        self.ultimo_acesso = agora

    # ==========================
    # STATUS
    # ==========================

    @property
    def esta_ativo(self):
        return self.ativo

    # ==========================
    # REPRESENTAÇÃO
    # ==========================

    def __repr__(self):

        return f"<Usuario {self.nome}>"
