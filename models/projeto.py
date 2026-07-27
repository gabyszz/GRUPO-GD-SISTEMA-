from database.database import db


class Projeto(db.Model):

    __tablename__ = "projetos"

    # ==========================================
    # DADOS DO PROJETO
    # ==========================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    nome = db.Column(
        db.String(150),
        nullable=False
    )

    centro_custo = db.Column(
        db.String(50)
    )

    contato = db.Column(
        db.String(100)
    )

    telefone = db.Column(
        db.String(20)
    )

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False
    )

    cliente = db.relationship(
        "Cliente",
        backref="projetos"
    )

    responsavel = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(50)
    )

    # ==========================================
    # DADOS PARA EMISSÃO DA TRT
    # ==========================================

    trt_nome = db.Column(
        db.String(150)
    )

    trt_cpf_cnpj = db.Column(
        db.String(30)
    )

    trt_telefone = db.Column(
        db.String(30)
    )

    trt_contato = db.Column(
        db.String(100)
    )

    trt_email = db.Column(
        db.String(150)
    )

    trt_endereco = db.Column(
        db.String(200)
    )

    trt_cidade = db.Column(
        db.String(100)
    )

    trt_uf = db.Column(
        db.String(2)
    )