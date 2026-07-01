from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from database.database import db
from models.projeto import Projeto
from models.cliente import Cliente

from services.log_service import registrar_log
from services.backup_manager import backup_antes_de_alteracao

projetos = Blueprint("projetos", __name__)


# ==========================
# LISTAR PROJETOS
# ==========================

@projetos.route("/projetos")
@login_required
def listar_projetos():

    lista_projetos = Projeto.query.order_by(
        Projeto.id.desc()
    ).all()

    return render_template(
        "projetos.html",
        projetos=lista_projetos
    )


# ==========================
# NOVO PROJETO
# ==========================

@projetos.route("/projetos/novo")
@login_required
def novo_projeto():

    clientes = Cliente.query.order_by(
        Cliente.nome
    ).all()

    return render_template(
        "novo_projeto.html",
        clientes=clientes
    )


# ==========================
# SALVAR PROJETO
# ==========================

@projetos.route("/projetos/salvar", methods=["POST"])
@login_required
def salvar_projeto():

    projeto = Projeto(
        nome=request.form["nome"],
        cliente_id=request.form["cliente_id"],
        responsavel=request.form["responsavel"],
        status=request.form["status"]
    )

    db.session.add(projeto)

    db.session.commit()

    registrar_log(
        f"Criou o projeto '{projeto.nome}'"
    )

    return redirect("/projetos")


# ==========================
# EDITAR PROJETO
# ==========================

@projetos.route("/projetos/editar/<int:id>")
@login_required
def editar_projeto(id):

    projeto = Projeto.query.get_or_404(id)

    clientes = Cliente.query.order_by(
        Cliente.nome
    ).all()

    return render_template(
        "editar_projeto.html",
        projeto=projeto,
        clientes=clientes
    )


# ==========================
# ATUALIZAR PROJETO
# ==========================

@projetos.route("/projetos/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_projeto(id):

    projeto = Projeto.query.get_or_404(id)

    nome_antigo = projeto.nome

    projeto.nome = request.form["nome"]
    projeto.cliente_id = request.form["cliente_id"]
    projeto.responsavel = request.form["responsavel"]
    projeto.status = request.form["status"]

    db.session.commit()

    registrar_log(
        f"Editou o projeto '{nome_antigo}'"
    )

    return redirect("/projetos")


# ==========================
# EXCLUIR PROJETO
# ==========================

@projetos.route("/projetos/excluir/<int:id>")
@login_required
def excluir_projeto(id):

    projeto = Projeto.query.get_or_404(id)

    # BACKUP AUTOMÁTICO
    backup_antes_de_alteracao()

    nome = projeto.nome

    db.session.delete(projeto)

    db.session.commit()

    registrar_log(
        f"Excluiu o projeto '{nome}'"
    )

    return redirect("/projetos")