from flask import Blueprint, render_template
from flask_login import login_required

from models.cliente import Cliente
from models.projeto import Projeto
from models.planejamento import Planejamento

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
@login_required
def inicio():

    total_clientes = Cliente.query.count()

    total_projetos = Projeto.query.count()

    total_planejamentos = Planejamento.query.count()

    return render_template(
        "index.html",
        total_clientes=total_clientes,
        total_projetos=total_projetos,
        total_planejamentos=total_planejamentos
    )