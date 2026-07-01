from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from database.database import db
from models.cliente import Cliente

from services.log_service import registrar_log
from services.backup_manager import backup_antes_de_alteracao


clientes = Blueprint("clientes", __name__)


# ==========================
# LISTAR CLIENTES
# ==========================

@clientes.route("/clientes")
@login_required
def listar_clientes():

    lista = Cliente.query.order_by(Cliente.nome).all()

    return render_template(
        "clientes.html",
        clientes=lista
    )


# ==========================
# NOVO CLIENTE
# ==========================

@clientes.route("/clientes/novo")
@login_required
def novo_cliente():

    return render_template("novo_cliente.html")


# ==========================
# SALVAR CLIENTE
# ==========================

@clientes.route("/clientes/salvar", methods=["POST"])
@login_required
def salvar_cliente():

    cliente = Cliente(
        nome=request.form["nome"],
        cnpj=request.form["cnpj"],
        telefone=request.form["telefone"],
        email=request.form["email"],
        endereco=request.form["endereco"],
        cidade=request.form["cidade"],
        estado=request.form["estado"],
        responsavel=request.form["responsavel"],
        centro_custo=request.form["centro_custo"]
    )

    db.session.add(cliente)
    db.session.commit()

    registrar_log(
        f"Criou o cliente '{cliente.nome}'"
    )

    return redirect("/clientes")


# ==========================
# EDITAR CLIENTE
# ==========================

@clientes.route("/clientes/editar/<int:id>")
@login_required
def editar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    return render_template(
        "editar_cliente.html",
        cliente=cliente
    )


# ==========================
# ATUALIZAR CLIENTE
# ==========================

@clientes.route("/clientes/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    nome_antigo = cliente.nome

    cliente.nome = request.form["nome"]
    cliente.cnpj = request.form["cnpj"]
    cliente.telefone = request.form["telefone"]
    cliente.email = request.form["email"]
    cliente.endereco = request.form["endereco"]
    cliente.cidade = request.form["cidade"]
    cliente.estado = request.form["estado"]
    cliente.responsavel = request.form["responsavel"]
    cliente.centro_custo = request.form["centro_custo"]

    db.session.commit()

    registrar_log(
        f"Editou o cliente '{nome_antigo}'"
    )

    return redirect("/clientes")


# ==========================
# EXCLUIR CLIENTE
# ==========================

@clientes.route("/clientes/excluir/<int:id>")
@login_required
def excluir_cliente(id):

    cliente = Cliente.query.get_or_404(id)

    # Backup automático antes da exclusão
    backup_antes_de_alteracao()

    nome = cliente.nome

    db.session.delete(cliente)
    db.session.commit()

    registrar_log(
        f"Excluiu o cliente '{nome}'"
    )

    return redirect("/clientes")