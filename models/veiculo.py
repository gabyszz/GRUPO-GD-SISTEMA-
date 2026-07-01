from database.database import db


class Veiculo(db.Model):

    __tablename__ = "veiculos"

    id = db.Column(db.Integer, primary_key=True)

    placa = db.Column(db.String(10), unique=True, nullable=False)

    modelo = db.Column(db.String(100), nullable=False)

    marca = db.Column(db.String(100))

    ano = db.Column(db.Integer)

    quilometragem = db.Column(db.Integer, default=0)

    status = db.Column(
        db.String(30),
        default="Disponível"
    )