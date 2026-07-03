from database.database import db
from sqlalchemy.orm import backref


class Financeiro(db.Model):

    __tablename__ = "financeiro"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    projeto_id = db.Column(
        db.Integer,
        db.ForeignKey("projetos.id"),
        nullable=False,
        unique=True
    )

    projeto = db.relationship(
        "Projeto",
        backref=backref(
            "financeiro",
            uselist=False
        )
    )

    valor_contrato = db.Column(
        db.Float,
        default=0
    )

    valor_recebido = db.Column(
        db.Float,
        default=0
    )

    nota_fiscal = db.Column(
        db.String(50)
    )

    data_faturamento = db.Column(
        db.Date
    )

    data_recebimento = db.Column(
        db.Date
    )

    status = db.Column(
        db.String(30),
        default="A Faturar"
    )

    observacoes = db.Column(
        db.Text
    )