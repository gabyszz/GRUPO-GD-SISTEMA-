from flask import Blueprint, render_template, request, redirect

from datetime import date

from sqlalchemy import func

from database.database import db

from models.financeiro import Financeiro
from models.planejamento import Planejamento
from models.projeto import Projeto
from models.cliente import Cliente

from services.log_service import registrar_log
from services.permissoes import perfis_permitidos


financeiro = Blueprint("financeiro", __name__)


# ==========================
# LISTAR FINANCEIRO
# ==========================

@financeiro.route("/financeiro")
@perfis_permitidos("Administrador", "Gerente")
def listar_financeiro():

    projeto = request.args.get("projeto", "")
    cliente = request.args.get("cliente", "")
    status = request.args.get("status", "")

    consulta = (
        Financeiro.query
        .join(Planejamento)
        .join(Projeto)
        .join(Cliente)
    )

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

    # ==========================
    # TOTAIS DO PAINEL
    # ==========================

    hoje = date.today()

    total_receber = 0
    total_atraso = 0

    for financeiro_obj in Financeiro.query.all():

        saldo = (
            (financeiro_obj.valor_contrato or 0)
            -
            (financeiro_obj.valor_recebido or 0)
        )

        if saldo <= 0:
            continue

        if financeiro_obj.data_prevista_recebimento:

            if financeiro_obj.data_prevista_recebimento >= hoje:

                total_receber += saldo

            else:

                total_atraso += saldo

        else:

            total_receber += saldo

    return render_template(
        "financeiro.html",
        financeiros=lista_financeiro,
        quantidade=quantidade,
        total_receber=total_receber,
        total_atraso=total_atraso
    )


# ==========================
# EDITAR FINANCEIRO
# ==========================

@financeiro.route("/financeiro/editar/<int:id>")
@perfis_permitidos("Administrador", "Gerente")
def editar_financeiro(id):

    financeiro_obj = Financeiro.query.get_or_404(id)

    return render_template(
        "editar_financeiro.html",
        financeiro=financeiro_obj
    )


# ==========================
# ATUALIZAR FINANCEIRO
# ==========================

@financeiro.route("/financeiro/atualizar/<int:id>", methods=["POST"])
@perfis_permitidos("Administrador", "Gerente")
def atualizar_financeiro(id):

    financeiro_obj = Financeiro.query.get_or_404(id)

    # ==========================
    # VALORES
    # ==========================

    financeiro_obj.valor_contrato = float(
        request.form.get("valor_contrato") or 0
    )

    financeiro_obj.valor_recebido = float(
        request.form.get("valor_recebido") or 0
    )

    # ==========================
    # FATURAMENTO
    # ==========================

    financeiro_obj.recibo_sinal = request.form.get(
        "recibo_sinal"
    )

    financeiro_obj.recibo_saldo = request.form.get(
        "recibo_saldo"
    )

    financeiro_obj.faturado_por = request.form.get(
        "faturado_por"
    )

    financeiro_obj.data_faturamento = (
        request.form.get("data_faturamento")
        or None
    )

    # ==========================
    # DADOS PARA FATURAMENTO
    # ==========================

    financeiro_obj.faturamento_nome = request.form.get(
        "faturamento_nome"
    )

    financeiro_obj.faturamento_cpf_cnpj = request.form.get(
        "faturamento_cpf_cnpj"
    )

    financeiro_obj.faturamento_telefone = request.form.get(
        "faturamento_telefone"
    )

    financeiro_obj.faturamento_contato = request.form.get(
        "faturamento_contato"
    )

    financeiro_obj.faturamento_email = request.form.get(
        "faturamento_email"
    )

    financeiro_obj.faturamento_endereco = request.form.get(
        "faturamento_endereco"
    )

    financeiro_obj.faturamento_cidade = request.form.get(
        "faturamento_cidade"
    )

    financeiro_obj.faturamento_uf = request.form.get(
        "faturamento_uf"
    )

    # ==========================
    # RECEBIMENTO
    # ==========================

    financeiro_obj.data_prevista_recebimento = (
        request.form.get("data_prevista_recebimento")
        or None
    )

    financeiro_obj.data_recebimento = (
        request.form.get("data_recebimento")
        or None
    )

    # ==========================
    # OBSERVAÇÕES
    # ==========================

    financeiro_obj.observacoes = request.form.get(
        "observacoes"
    )

    # ==========================
    # STATUS AUTOMÁTICO
    # ==========================

    if financeiro_obj.valor_recebido <= 0:

        financeiro_obj.status = "A Faturar"

    elif financeiro_obj.valor_recebido < financeiro_obj.valor_contrato:

        financeiro_obj.status = "Recebimento Parcial"

    else:

        financeiro_obj.status = "Pago"

    db.session.commit()

    registrar_log(
        f"Atualizou o financeiro do planejamento #{financeiro_obj.planejamento.id}"
    )

    return redirect("/financeiro")


# ==========================
# SINCRONIZAR FINANCEIRO
# ==========================

@financeiro.route("/financeiro/sincronizar")
@perfis_permitidos("Administrador", "Gerente")
def sincronizar_financeiro():

    planejamentos = Planejamento.query.all()

    quantidade = 0

    for planejamento in planejamentos:

        existe = Financeiro.query.filter_by(
            planejamento_id=planejamento.id
        ).first()

        if not existe:

            db.session.add(
                Financeiro(
                    planejamento_id=planejamento.id
                )
            )

            quantidade += 1

    db.session.commit()

    return f"{quantidade} registros financeiros criados."