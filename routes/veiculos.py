from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required

from database.database import db
from models.veiculo import Veiculo

from services.log_service import registrar_log
from services.backup_manager import backup_antes_de_alteracao

veiculos = Blueprint("veiculos", __name__)


# ==========================
# LISTAR
# ==========================

@veiculos.route("/veiculos")
@login_required
def listar_veiculos():

    lista = Veiculo.query.order_by(
        Veiculo.modelo
    ).all()

    return render_template(
        "veiculos.html",
        veiculos=lista
    )


# ==========================
# NOVO
# ==========================

@veiculos.route("/veiculos/novo")
@login_required
def novo_veiculo():

    return render_template(
        "novo_veiculo.html"
    )


# ==========================
# SALVAR
# ==========================

@veiculos.route("/veiculos/salvar", methods=["POST"])
@login_required
def salvar_veiculo():

    backup_antes_de_alteracao()

    veiculo = Veiculo(

        placa=request.form["placa"],
        modelo=request.form["modelo"],
        marca=request.form["marca"],
        ano=request.form["ano"],
        quilometragem=request.form["quilometragem"],
        status=request.form["status"]

    )

    db.session.add(veiculo)

    db.session.commit()

    registrar_log(
        f"Criou o veículo '{veiculo.placa}'"
    )

    return redirect(url_for("veiculos.listar_veiculos"))


# ==========================
# EDITAR
# ==========================

@veiculos.route("/veiculos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_veiculo(id):

    veiculo = Veiculo.query.get_or_404(id)

    if request.method == "POST":

        backup_antes_de_alteracao()

        placa_antiga = veiculo.placa

        veiculo.placa = request.form["placa"]
        veiculo.modelo = request.form["modelo"]
        veiculo.marca = request.form["marca"]
        veiculo.ano = request.form["ano"]
        veiculo.quilometragem = request.form["quilometragem"]
        veiculo.status = request.form["status"]

        db.session.commit()

        registrar_log(
            f"Editou o veículo '{placa_antiga}'"
        )

        return redirect(url_for("veiculos.listar_veiculos"))

    return render_template(
        "editar_veiculo.html",
        veiculo=veiculo
    )


# ==========================
# EXCLUIR
# ==========================

@veiculos.route("/veiculos/excluir/<int:id>", methods=["POST"])
@login_required
def excluir_veiculo(id):

    veiculo = Veiculo.query.get_or_404(id)

    backup_antes_de_alteracao()

    placa = veiculo.placa

    db.session.delete(veiculo)

    db.session.commit()

    registrar_log(
        f"Excluiu o veículo '{placa}'"
    )

    return redirect(url_for("veiculos.listar_veiculos"))