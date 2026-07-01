from datetime import datetime

from database.database import db


class Log(db.Model):

    __tablename__ = "logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    usuario = db.Column(
        db.String(100),
        nullable=False
    )

    acao = db.Column(
        db.String(300),
        nullable=False
    )

    data = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    ip = db.Column(
        db.String(45),
        nullable=True
    )