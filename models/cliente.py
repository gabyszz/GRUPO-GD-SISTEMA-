from database.database import db


class Cliente(db.Model):

    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)

    cnpj = db.Column(db.String(20))

    telefone = db.Column(db.String(20))

    email = db.Column(db.String(120))

    endereco = db.Column(db.String(200))

    cidade = db.Column(db.String(100))

    estado = db.Column(db.String(2))

    responsavel = db.Column(db.String(100))

