from database.database import db


equipe_funcionario = db.Table(

    "equipe_funcionario",

    db.Column(
        "equipe_id",
        db.Integer,
        db.ForeignKey("equipes.id"),
        primary_key=True
    ),

    db.Column(
        "funcionario_id",
        db.Integer,
        db.ForeignKey("funcionarios.id"),
        primary_key=True
    )

)