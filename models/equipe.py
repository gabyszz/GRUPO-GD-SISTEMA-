from database.database import db

from models.equipe_funcionario import equipe_funcionario


class Equipe(db.Model):

    __tablename__ = "equipes"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    supervisor = db.Column(db.String(100))

    descricao = db.Column(db.Text)

    funcionarios = db.relationship(
        "Funcionario",
        secondary=equipe_funcionario,
        backref="equipes"
    )