from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from database.database import db
from models.funcionario import Funcionario

from services.log_service import registrar_log
from services.backup_manager import backup_antes_de_alteracao

funcionarios = Blueprint("funcionarios", __name__)


# ==========================
# LISTAR
# ==========================

@funcionarios.route("/funcionarios")
@login_required
def listar_funcionarios():

    lista = Funcionario.query.order_by(
        Funcionario.nome
    ).all()

    return render_template(
        "funcionarios.html",
        funcionarios=lista
    )


# ==========================
# NOVO
# ==========================

@funcionarios.route("/funcionarios/novo")
@login_required
def novo_funcionario():

    return render_template(
        "novo_funcionario.html"
    )


# ==========================
# SALVAR
# ==========================

@funcionarios.route("/funcionarios/salvar", methods=["POST"])
@login_required
def salvar_funcionario():

    funcionario = Funcionario(
        nome=request.form.get("nome"),
        cpf=request.form.get("cpf"),
        telefone=request.form.get("telefone"),
        email=request.form.get("email"),
        cargo=request.form.get("cargo"),
        funcao=request.form.get("funcao"),
        status=request.form.get("status"),
        observacoes=request.form.get("observacoes")
    )

    db.session.add(funcionario)
    db.session.commit()

    registrar_log(
        f"Criou o funcionário '{funcionario.nome}'"
    )

    return redirect("/funcionarios")


# ==========================
# EDITAR
# ==========================

@funcionarios.route("/funcionarios/editar/<int:id>")
@login_required
def editar_funcionario(id):

    funcionario = Funcionario.query.get_or_404(id)

    return render_template(
        "editar_funcionario.html",
        funcionario=funcionario
    )


# ==========================
# ATUALIZAR
# ==========================

@funcionarios.route("/funcionarios/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_funcionario(id):

    funcionario = Funcionario.query.get_or_404(id)

    # Backup automático antes da alteração
    backup_antes_de_alteracao()

    nome_antigo = funcionario.nome

    funcionario.nome = request.form.get("nome")
    funcionario.cpf = request.form.get("cpf")
    funcionario.telefone = request.form.get("telefone")
    funcionario.email = request.form.get("email")
    funcionario.cargo = request.form.get("cargo")
    funcionario.funcao = request.form.get("funcao")
    funcionario.status = request.form.get("status")
    funcionario.observacoes = request.form.get("observacoes")

    db.session.commit()

    registrar_log(
        f"Editou o funcionário '{nome_antigo}'"
    )

    return redirect("/funcionarios")


# ==========================
# EXCLUIR
# ==========================

@funcionarios.route("/funcionarios/excluir/<int:id>")
@login_required
def excluir_funcionario(id):

    funcionario = Funcionario.query.get_or_404(id)

    # Backup automático
    backup_antes_de_alteracao()

    nome = funcionario.nome

    db.session.delete(funcionario)
    db.session.commit()

    registrar_log(
        f"Excluiu o funcionário '{nome}'"
    )

    return redirect("/funcionarios")