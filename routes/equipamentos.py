from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from datetime import datetime

from database.database import db
from models.equipamento import Equipamento

from services.log_service import registrar_log
from services.backup_manager import backup_antes_de_alteracao

equipamentos = Blueprint("equipamentos", __name__)


# ==========================
# LISTAR
# ==========================

@equipamentos.route("/equipamentos")
@login_required
def listar_equipamentos():

    lista = Equipamento.query.order_by(
        Equipamento.nome
    ).all()

    return render_template(
        "equipamentos.html",
        equipamentos=lista
    )


# ==========================
# NOVO
# ==========================

@equipamentos.route("/equipamentos/novo")
@login_required
def novo_equipamento():

    return render_template(
        "novo_equipamento.html"
    )


# ==========================
# SALVAR
# ==========================

@equipamentos.route("/equipamentos/salvar", methods=["POST"])
@login_required
def salvar_equipamento():

    ultima = request.form.get("ultima_calibracao")
    proxima = request.form.get("proxima_calibracao")

    equipamento = Equipamento(

        patrimonio=request.form["patrimonio"],
        nome=request.form["nome"],
        categoria=request.form["categoria"],
        fabricante=request.form["fabricante"],
        modelo=request.form["modelo"],
        numero_serie=request.form["numero_serie"],
        status=request.form["status"],

        ultima_calibracao=datetime.strptime(
            ultima,
            "%Y-%m-%d"
        ).date() if ultima else None,

        proxima_calibracao=datetime.strptime(
            proxima,
            "%Y-%m-%d"
        ).date() if proxima else None,

        observacoes=request.form["observacoes"]

    )

    db.session.add(equipamento)

    db.session.commit()

    registrar_log(
        f"Criou o equipamento '{equipamento.nome}'"
    )

    return redirect("/equipamentos")


# ==========================
# EDITAR
# ==========================

@equipamentos.route("/equipamentos/editar/<int:id>")
@login_required
def editar_equipamento(id):

    equipamento = Equipamento.query.get_or_404(id)

    return render_template(
        "editar_equipamento.html",
        equipamento=equipamento
    )


# ==========================
# ATUALIZAR
# ==========================

@equipamentos.route("/equipamentos/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_equipamento(id):

    equipamento = Equipamento.query.get_or_404(id)

    nome_antigo = equipamento.nome

    equipamento.patrimonio = request.form["patrimonio"]
    equipamento.nome = request.form["nome"]
    equipamento.categoria = request.form["categoria"]
    equipamento.fabricante = request.form["fabricante"]
    equipamento.modelo = request.form["modelo"]
    equipamento.numero_serie = request.form["numero_serie"]
    equipamento.status = request.form["status"]

    ultima = request.form.get("ultima_calibracao")
    proxima = request.form.get("proxima_calibracao")

    equipamento.ultima_calibracao = (
        datetime.strptime(
            ultima,
            "%Y-%m-%d"
        ).date()
        if ultima else None
    )

    equipamento.proxima_calibracao = (
        datetime.strptime(
            proxima,
            "%Y-%m-%d"
        ).date()
        if proxima else None
    )

    equipamento.observacoes = request.form["observacoes"]

    db.session.commit()

    registrar_log(
        f"Editou o equipamento '{nome_antigo}'"
    )

    return redirect("/equipamentos")


# ==========================
# EXCLUIR
# ==========================

@equipamentos.route("/equipamentos/excluir/<int:id>")
@login_required
def excluir_equipamento(id):

    equipamento = Equipamento.query.get_or_404(id)

    # BACKUP AUTOMÁTICO
    backup_antes_de_alteracao()

    nome = equipamento.nome

    db.session.delete(equipamento)

    db.session.commit()

    registrar_log(
        f"Excluiu o equipamento '{nome}'"
    )

    return redirect("/equipamentos")