from database.database import db


class Projeto(db.Model):

    __tablename__ = "projetos"

    id = db.Column(db.Integer, primary_key=True)
    centro_custo = db.Column(db.String(50))
    contato = db.Column(db.String(100))
    telefone = db.Column(db.String(20))
    nome = db.Column(db.String(150), nullable=False)

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False
    )

    cliente = db.relationship(
        "Cliente",
        backref="projetos"
    )

    responsavel = db.Column(db.String(100))

    status = db.Column(db.String(50))