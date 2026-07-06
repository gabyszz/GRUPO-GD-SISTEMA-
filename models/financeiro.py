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

    # ==========================
    # VALORES
    # ==========================

    valor_contrato = db.Column(
        db.Float,
        default=0
    )

    valor_recebido = db.Column(
        db.Float,
        default=0
    )

    # ==========================
    # FATURAMENTO
    # ==========================

    recibo_sinal = db.Column(
        db.String(50)
    )

    recibo_saldo = db.Column(
        db.String(50)
    )

    faturado_por = db.Column(
        db.String(120)
    )

    data_faturamento = db.Column(
        db.Date
    )

    # ==========================
    # DADOS PARA FATURAMENTO
    # ==========================

    faturamento_nome = db.Column(
        db.String(150)
    )

    faturamento_cpf_cnpj = db.Column(
        db.String(30)
    )

    faturamento_telefone = db.Column(
        db.String(30)
    )

    faturamento_contato = db.Column(
        db.String(100)
    )

    faturamento_email = db.Column(
        db.String(150)
    )

    faturamento_endereco = db.Column(
        db.String(200)
    )

    faturamento_cidade = db.Column(
        db.String(100)
    )

    faturamento_uf = db.Column(
        db.String(2)
    )

    # ==========================
    # RECEBIMENTO
    # ==========================

    data_prevista_recebimento = db.Column(
        db.Date
    )

    data_recebimento = db.Column(
        db.Date
    )

    # ==========================
    # STATUS
    # ==========================

    status = db.Column(
        db.String(30),
        default="A Faturar"
    )

    # ==========================
    # OBSERVAÇÕES
    # ==========================

    observacoes = db.Column(
        db.Text
    )

    # ==========================
    # PROPRIEDADES
    # ==========================

    @property
    def valor_aberto(self):
        return (self.valor_contrato or 0) - (self.valor_recebido or 0)