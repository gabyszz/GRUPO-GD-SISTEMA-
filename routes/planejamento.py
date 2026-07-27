from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from datetime import datetime

from database.database import db

from models.planejamento import Planejamento
from models.projeto import Projeto
from models.equipe import Equipe
from models.veiculo import Veiculo

from services.log_service import registrar_log
from services.permissoes import perfis_permitidos
from services.backup_manager import backup_antes_de_alteracao

planejamento = Blueprint("planejamento", __name__)


# ==========================
# LISTAR
# ==========================

@planejamento.route("/planejamento")
@perfis_permitidos("Administrador", "Gerente", "Operador", "Executor")
def listar_planejamento():

    planejamentos = Planejamento.query.order_by(
        Planejamento.id.desc()
    ).all()

    return render_template(
        "planejamento.html",
        planejamentos=planejamentos
    )


# ==========================
# NOVO
# ==========================

@planejamento.route("/planejamento/novo")
@perfis_permitidos("Administrador", "Gerente", "Operador", "Executor")
def novo_planejamento():

    if not somente_nao_executor():
      return redirect("/planejamento")

    projetos = Projeto.query.order_by(
        Projeto.nome
    ).all()

    equipes = Equipe.query.order_by(
        Equipe.nome
    ).all()

    veiculos = Veiculo.query.order_by(
        Veiculo.modelo
    ).all()

    return render_template(
        "novo_planejamento.html",
        projetos=projetos,
        equipes=equipes,
        veiculos=veiculos
    )


# ==========================
# SALVAR
# ==========================

@planejamento.route("/planejamento/salvar", methods=["POST"])
@perfis_permitidos("Administrador", "Gerente", "Operador")
def salvar_planejamento():

    data_inicio = request.form.get("data_inicio")
    data_fim = request.form.get("data_fim")

    planejamento_obj = Planejamento(

        projeto_id=request.form["projeto_id"],

        equipe_id=request.form["equipe_id"],

        veiculo_id=request.form["veiculo_id"],

        data_inicio=datetime.strptime(
            data_inicio,
            "%Y-%m-%d"
        ).date() if data_inicio else None,

        data_fim=datetime.strptime(
            data_fim,
            "%Y-%m-%d"
        ).date() if data_fim else None,

        responsavel=request.form["responsavel"],

        status=request.form["status"],

        observacoes=request.form["observacoes"]

    )

    db.session.add(planejamento_obj)

    db.session.commit()

    registrar_log(
        f"Criou o planejamento #{planejamento_obj.id}"
    )

    return redirect("/planejamento")


# ==========================
# EDITAR
# ==========================

@planejamento.route("/planejamento/editar/<int:id>")
@perfis_permitidos("Administrador", "Gerente", "Operador", "Executor")
def editar_planejamento(id):

    planejamento_obj = Planejamento.query.get_or_404(id)

    projetos = Projeto.query.order_by(
        Projeto.nome
    ).all()

    equipes = Equipe.query.order_by(
        Equipe.nome
    ).all()

    veiculos = Veiculo.query.order_by(
        Veiculo.modelo
    ).all()

    projeto = Projeto.query.get_or_404(
        planejamento_obj.projeto_id
    )

    return render_template(
        "editar_planejamento.html",
        planejamento=planejamento_obj,
        projeto=projeto,
        projetos=projetos,
        equipes=equipes,
        veiculos=veiculos
    )

# ==========================
# ATUALIZAR
# ==========================

@planejamento.route("/planejamento/atualizar/<int:id>", methods=["POST"])
@perfis_permitidos("Administrador", "Gerente", "Operador", "Executor")
def atualizar_planejamento(id):

    planejamento_obj = Planejamento.query.get_or_404(id)

    planejamento_obj.projeto_id = request.form["projeto_id"]
    planejamento_obj.equipe_id = request.form["equipe_id"]
    planejamento_obj.veiculo_id = request.form["veiculo_id"]

    data_inicio = request.form.get("data_inicio")
    data_fim = request.form.get("data_fim")

    planejamento_obj.data_inicio = (
        datetime.strptime(
            data_inicio,
            "%Y-%m-%d"
        ).date()
        if data_inicio else None
    )

    planejamento_obj.data_fim = (
        datetime.strptime(
            data_fim,
            "%Y-%m-%d"
        ).date()
        if data_fim else None
    )

    planejamento_obj.responsavel = request.form["responsavel"]
    planejamento_obj.status = request.form["status"]
    planejamento_obj.observacoes = request.form["observacoes"]

    db.session.commit()

    registrar_log(
        f"Editou o planejamento #{planejamento_obj.id}"
    )

    return redirect("/planejamento")


# ==========================
# EXCLUIR
# ==========================

@planejamento.route("/planejamento/excluir/<int:id>")
@perfis_permitidos("Administrador", "Gerente", "Operador")
def excluir_planejamento(id):

    planejamento_obj = Planejamento.query.get_or_404(id)

    # BACKUP AUTOMÁTICO
    backup_antes_de_alteracao()

    identificador = planejamento_obj.id

    db.session.delete(planejamento_obj)

    db.session.commit()

    registrar_log(
        f"Excluiu o planejamento #{identificador}"
    )

    return redirect("/planejamento")