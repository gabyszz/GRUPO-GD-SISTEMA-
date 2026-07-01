from database.database import db


class Funcionario(db.Model):

    __tablename__ = "funcionarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(150), nullable=False)

    cpf = db.Column(db.String(14))

    telefone = db.Column(db.String(20))

    email = db.Column(db.String(150))

    cargo = db.Column(db.String(80))

    funcao = db.Column(db.String(80))

    status = db.Column(
        db.String(20),
        default="Disponível"
    )

    observacoes = db.Column(db.Text)

    def __repr__(self):
        return self.nome