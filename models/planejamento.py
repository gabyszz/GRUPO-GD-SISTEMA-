from database.database import db


class Planejamento(db.Model):

    __tablename__ = "planejamentos"


    # ==========================
    # IDENTIFICAÇÃO
    # ==========================

    id = db.Column(
        db.Integer,
        primary_key=True
    )



    # ==========================
    # RELACIONAMENTOS
    # ==========================

    projeto_id = db.Column(
        db.Integer,
        db.ForeignKey("projetos.id"),
        nullable=False
    )

    projeto = db.relationship(
        "Projeto",
        backref="planejamentos"
    )



    equipe_id = db.Column(
        db.Integer,
        db.ForeignKey("equipes.id"),
        nullable=False
    )

    equipe = db.relationship(
        "Equipe"
    )



    veiculo_id = db.Column(
        db.Integer,
        db.ForeignKey("veiculos.id"),
        nullable=False
    )

    veiculo = db.relationship(
        "Veiculo"
    )



    # ==========================
    # FINANCEIRO
    # ==========================

    # Relacionamento criado pelo Financeiro:
    #
    # planejamento.financeiro
    #
    # Um planejamento possui apenas um financeiro.



    # ==========================
    # DATAS
    # ==========================

    data_inicio = db.Column(
        db.Date
    )

    data_fim = db.Column(
        db.Date
    )



    # ==========================
    # DADOS DO PLANEJAMENTO
    # ==========================

    responsavel = db.Column(
        db.String(100)
    )

    status = db.Column(
        db.String(50)
    )

    observacoes = db.Column(
        db.Text
    )