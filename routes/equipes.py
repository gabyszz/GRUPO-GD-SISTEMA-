from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from database.database import db
from models.equipe import Equipe
from models.funcionario import Funcionario

from services.log_service import registrar_log
from services.backup_manager import backup_antes_de_alteracao
from services.permissoes import perfis_permitidos

equipes = Blueprint("equipes", __name__)


# ==========================
# LISTAR
# ==========================

@equipes.route("/equipes")
@perfis_permitidos("Administrador", "Gerente")
def listar_equipes():

    lista = Equipe.query.order_by(
        Equipe.nome
    ).all()

    return render_template(
        "equipes.html",
        equipes=lista
    )


# ==========================
# NOVA EQUIPE
# ==========================

@equipes.route("/equipes/nova")
@perfis_permitidos("Administrador", "Gerente")
def nova_equipe():

    funcionarios = Funcionario.query.order_by(
        Funcionario.nome
    ).all()

    return render_template(
        "nova_equipe.html",
        funcionarios=funcionarios
    )


# ==========================
# SALVAR
# ==========================

@equipes.route("/equipes/salvar", methods=["POST"])
@perfis_permitidos("Administrador", "Gerente")
def salvar_equipe():

    equipe = Equipe(
        nome=request.form["nome"],
        supervisor=request.form["supervisor"],
        descricao=request.form["descricao"]
    )

    funcionarios_ids = request.form.getlist("funcionarios")

    for funcionario_id in funcionarios_ids:

        funcionario = Funcionario.query.get(int(funcionario_id))

        if funcionario:
            equipe.funcionarios.append(funcionario)

    db.session.add(equipe)

    db.session.commit()

    registrar_log(
        f"Criou a equipe '{equipe.nome}'"
    )

    return redirect("/equipes")


# ==========================
# EDITAR
# ==========================

@equipes.route("/equipes/editar/<int:id>")
@perfis_permitidos("Administrador", "Gerente")
def editar_equipe(id):

    equipe = Equipe.query.get_or_404(id)

    funcionarios = Funcionario.query.order_by(
        Funcionario.nome
    ).all()

    return render_template(
        "editar_equipe.html",
        equipe=equipe,
        funcionarios=funcionarios
    )


# ==========================
# ATUALIZAR
# ==========================

@equipes.route("/equipes/atualizar/<int:id>", methods=["POST"])
@perfis_permitidos("Administrador", "Gerente")
def atualizar_equipe(id):

    equipe = Equipe.query.get_or_404(id)

    nome_antigo = equipe.nome

    equipe.nome = request.form["nome"]
    equipe.supervisor = request.form["supervisor"]
    equipe.descricao = request.form["descricao"]

    equipe.funcionarios.clear()

    funcionarios_ids = request.form.getlist("funcionarios")

    for funcionario_id in funcionarios_ids:

        funcionario = Funcionario.query.get(int(funcionario_id))

        if funcionario:
            equipe.funcionarios.append(funcionario)

    db.session.commit()

    registrar_log(
        f"Editou a equipe '{nome_antigo}'"
    )

    return redirect("/equipes")


# ==========================
# EXCLUIR
# ==========================

@equipes.route("/equipes/excluir/<int:id>")
@perfis_permitidos("Administrador", "Gerente")
def excluir_equipe(id):

    equipe = Equipe.query.get_or_404(id)

    # BACKUP AUTOMÁTICO
    backup_antes_de_alteracao()

    nome = equipe.nome

    db.session.delete(equipe)

    db.session.commit()

    registrar_log(
        f"Excluiu a equipe '{nome}'"
    )

    return redirect("/equipes")