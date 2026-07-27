from flask import Blueprint, render_template, request, redirect

from database.database import db

from models.projeto import Projeto
from models.cliente import Cliente

from services.log_service import registrar_log
from services.backup_manager import backup_antes_de_alteracao
from services.permissoes import perfis_permitidos


projetos = Blueprint(
    "projetos",
    __name__
)



# ==========================
# LISTAR PROJETOS
# ==========================

@projetos.route("/projetos")
@perfis_permitidos(
    "Administrador",
    "Gerente",
    "Operador"
)
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
@perfis_permitidos(
    "Administrador",
    "Gerente",
    "Operador"
)
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

@projetos.route(
    "/projetos/salvar",
    methods=["POST"]
)
@perfis_permitidos(
    "Administrador",
    "Gerente",
    "Operador"
)
def salvar_projeto():


    backup_antes_de_alteracao()


    projeto = Projeto(

        nome=request.form["nome"],

        cliente_id=request.form["cliente_id"],

        responsavel=request.form["responsavel"],

        status=request.form["status"],

        centro_custo=request.form["centro_custo"],

        contato=request.form["contato"],

        telefone=request.form["telefone"],


        # ==========================
        # TRT
        # ==========================

        trt_nome=request.form.get("trt_nome"),

        trt_cpf_cnpj=request.form.get("trt_cpf_cnpj"),

        trt_telefone=request.form.get("trt_telefone"),

        trt_contato=request.form.get("trt_contato"),

        trt_email=request.form.get("trt_email"),

        trt_endereco=request.form.get("trt_endereco"),

        trt_cidade=request.form.get("trt_cidade"),

        trt_uf=request.form.get("trt_uf")

    )


    db.session.add(projeto)

    db.session.commit()


    registrar_log(
        f"Criou o projeto '{projeto.nome}'"
    )


    return redirect(
        "/projetos"
    )



# ==========================
# EDITAR PROJETO
# ==========================

@projetos.route(
    "/projetos/editar/<int:id>"
)
@perfis_permitidos(
    "Administrador",
    "Gerente",
    "Operador"
)
def editar_projeto(id):


    projeto = Projeto.query.get_or_404(
        id
    )


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

@projetos.route(
    "/projetos/atualizar/<int:id>",
    methods=["POST"]
)
@perfis_permitidos(
    "Administrador",
    "Gerente",
    "Operador"
)
def atualizar_projeto(id):


    backup_antes_de_alteracao()


    projeto = Projeto.query.get_or_404(
        id
    )


    nome_antigo = projeto.nome


    projeto.nome = request.form["nome"]

    projeto.cliente_id = request.form["cliente_id"]

    projeto.responsavel = request.form["responsavel"]

    projeto.status = request.form["status"]

    projeto.centro_custo = request.form["centro_custo"]

    projeto.contato = request.form["contato"]

    projeto.telefone = request.form["telefone"]



    # ==========================
    # TRT
    # ==========================

    projeto.trt_nome = request.form.get(
        "trt_nome"
    )

    projeto.trt_cpf_cnpj = request.form.get(
        "trt_cpf_cnpj"
    )

    projeto.trt_telefone = request.form.get(
        "trt_telefone"
    )

    projeto.trt_contato = request.form.get(
        "trt_contato"
    )

    projeto.trt_email = request.form.get(
        "trt_email"
    )

    projeto.trt_endereco = request.form.get(
        "trt_endereco"
    )

    projeto.trt_cidade = request.form.get(
        "trt_cidade"
    )

    projeto.trt_uf = request.form.get(
        "trt_uf"
    )



    db.session.commit()


    registrar_log(
        f"Editou o projeto '{nome_antigo}'"
    )


    return redirect(
        "/projetos"
    )



# ==========================
# EXCLUIR PROJETO
# ==========================

@projetos.route(
    "/projetos/excluir/<int:id>"
)
@perfis_permitidos(
    "Administrador",
    "Gerente",
    "Operador"
)
def excluir_projeto(id):


    projeto = Projeto.query.get_or_404(
        id
    )


    backup_antes_de_alteracao()


    nome = projeto.nome


    db.session.delete(
        projeto
    )


    db.session.commit()


    registrar_log(
        f"Excluiu o projeto '{nome}'"
    )


    return redirect(
        "/projetos"
    )