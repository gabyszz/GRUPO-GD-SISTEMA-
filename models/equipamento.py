from database.database import db


class Equipamento(db.Model):

    __tablename__ = "equipamentos"

    id = db.Column(db.Integer, primary_key=True)

    patrimonio = db.Column(db.String(30), unique=True)

    nome = db.Column(db.String(150), nullable=False)

    categoria = db.Column(db.String(100))

    fabricante = db.Column(db.String(100))

    modelo = db.Column(db.String(100))

    numero_serie = db.Column(db.String(100))

    status = db.Column(
        db.String(30),
        default="Disponível"
    )

    ultima_calibracao = db.Column(db.Date)

    proxima_calibracao = db.Column(db.Date)

    observacoes = db.Column(db.Text)