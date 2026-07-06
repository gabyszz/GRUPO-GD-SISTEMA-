from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from database.database import db
from models.financeiro import Financeiro
from models.projeto import Projeto
from models.cliente import Cliente

from services.log_service import registrar_log

financeiro = Blueprint("financeiro", __name__)


# ==========================
# LISTAR FINANCEIRO
# ==========================

@financeiro.route("/financeiro")
@login_required
def listar_financeiro():

    projeto = request.args.get("projeto", "")
    cliente = request.args.get("cliente", "")
    status = request.args.get("status", "")

    consulta = Financeiro.query.join(Projeto).join(Cliente)

    if projeto:
        consulta = consulta.filter(
            Projeto.nome.ilike(f"%{projeto}%")
        )

    if cliente:
        consulta = consulta.filter(
            Cliente.nome.ilike(f"%{cliente}%")
        )

    if status:
        consulta = consulta.filter(
            Financeiro.status == status
        )

    lista_financeiro = consulta.order_by(
        Financeiro.id.desc()
    ).all()

    quantidade = len(lista_financeiro)

    return render_template(
        "financeiro.html",
        financeiros=lista_financeiro,
        quantidade=quantidade
    )


# ==========================
# EDITAR FINANCEIRO
# ==========================

@financeiro.route("/financeiro/editar/<int:id>")
@login_required
def editar_financeiro(id):

    financeiro = Financeiro.query.get_or_404(id)

    return render_template(
        "editar_financeiro.html",
        financeiro=financeiro
    )


# ==========================
# ATUALIZAR FINANCEIRO
# ==========================

@financeiro.route("/financeiro/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_financeiro(id):

    financeiro = Financeiro.query.get_or_404(id)

    # ==========================
    # VALORES
    # ==========================

    financeiro.valor_contrato = float(
        request.form.get("valor_contrato") or 0
    )

    financeiro.valor_recebido = float(
        request.form.get("valor_recebido") or 0
    )

    # ==========================
    # FATURAMENTO
    # ==========================

    financeiro.recibo_sinal = request.form.get("recibo_sinal")

    financeiro.recibo_saldo = request.form.get("recibo_saldo")

    financeiro.faturado_por = request.form.get("faturado_por")

    financeiro.data_faturamento = (
        request.form.get("data_faturamento") or None
    )

    # ==========================
    # DADOS PARA FATURAMENTO
    # ==========================

    financeiro.faturamento_nome = request.form.get("faturamento_nome")
    financeiro.faturamento_cpf_cnpj = request.form.get("faturamento_cpf_cnpj")
    financeiro.faturamento_telefone = request.form.get("faturamento_telefone")
    financeiro.faturamento_contato = request.form.get("faturamento_contato")
    financeiro.faturamento_email = request.form.get("faturamento_email")
    financeiro.faturamento_endereco = request.form.get("faturamento_endereco")
    financeiro.faturamento_cidade = request.form.get("faturamento_cidade")
    financeiro.faturamento_uf = request.form.get("faturamento_uf")

    # ==========================
    # RECEBIMENTO
    # ==========================

    financeiro.data_prevista_recebimento = (
        request.form.get("data_prevista_recebimento") or None
    )

    financeiro.data_recebimento = (
        request.form.get("data_recebimento") or None
    )

    # ==========================
    # OBSERVAÇÕES
    # ==========================

    financeiro.observacoes = request.form.get("observacoes")

    # ==========================
    # STATUS AUTOMÁTICO
    # ==========================

    if financeiro.valor_recebido <= 0:

        financeiro.status = "A Faturar"

    elif financeiro.valor_recebido < financeiro.valor_contrato:

        financeiro.status = "Recebimento Parcial"

    else:

        financeiro.status = "Pago"

    db.session.commit()

    registrar_log(
        f"Atualizou o financeiro do projeto '{financeiro.projeto.nome}'"
    )

    return redirect("/financeiro")


# ==========================
# SINCRONIZAR FINANCEIRO
# ==========================

@financeiro.route("/financeiro/sincronizar")
@login_required
def sincronizar_financeiro():

    projetos = Projeto.query.all()

    quantidade = 0

    for projeto in projetos:

        existe = Financeiro.query.filter_by(
            projeto_id=projeto.id
        ).first()

        if not existe:

            db.session.add(
                Financeiro(
                    projeto_id=projeto.id
                )
            )

            quantidade += 1

    db.session.commit()

    return f"{quantidade} registros financeiros criados."