from database.database import db


class Calendario(db.Model):

    __tablename__ = "calendario"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    titulo = db.Column(
        db.String(150),
        nullable=False
    )

    descricao = db.Column(
        db.Text
    )

    data_inicio = db.Column(
        db.Date,
        nullable=False
    )

    data_fim = db.Column(
        db.Date
    )

    hora_inicio = db.Column(
        db.Time
    )

    hora_fim = db.Column(
        db.Time
    )

    status = db.Column(
        db.String(30),
        default="Planejado"
    )

    cor = db.Column(
        db.String(20),
        default="#FFC107"
    )

    planejamento_id = db.Column(
        db.Integer,
        db.ForeignKey("planejamentos.id"),
        nullable=True
    )

    planejamento = db.relationship(
        "Planejamento",
        backref="eventos_calendario"
    )