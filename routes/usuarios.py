from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from database.database import db
from models.usuario import Usuario
from services.permissoes import perfis_permitidos


usuarios = Blueprint("usuarios", __name__)



# ==========================================
# LISTAR USUÁRIOS
# ==========================================

@usuarios.route("/usuarios")
@perfis_permitidos("Administrador")
def listar_usuarios():



    lista = Usuario.query.order_by(Usuario.nome).all()

    return render_template(
        "usuarios.html",
        usuarios=lista
    )


# ==========================================
# NOVO USUÁRIO
# ==========================================

@usuarios.route("/usuarios/novo")
@perfis_permitidos("Administrador")
def novo_usuario():


    return render_template("novo_usuario.html")


# ==========================================
# SALVAR USUÁRIO
# ==========================================

@usuarios.route("/usuarios/salvar", methods=["POST"])
@perfis_permitidos("Administrador")
def salvar_usuario():


    email = request.form["email"]

    existe = Usuario.query.filter_by(email=email).first()

    if existe:

        flash("Já existe um usuário com este e-mail.", "warning")

        return redirect("/usuarios/novo")

    usuario = Usuario(

        nome=request.form["nome"],

        email=email,

        perfil=request.form["perfil"],

        ativo=True

    )

    usuario.definir_senha(request.form["senha"])

    db.session.add(usuario)

    db.session.commit()

    flash("Usuário cadastrado com sucesso.", "success")

    return redirect("/usuarios")


# ==========================================
# EDITAR
# ==========================================

@usuarios.route("/usuarios/editar/<int:id>")
@perfis_permitidos("Administrador")
def editar_usuario(id):


    usuario = Usuario.query.get_or_404(id)

    return render_template(

        "editar_usuario.html",

        usuario=usuario

    )


# ==========================================
# ATUALIZAR
# ==========================================

@usuarios.route("/usuarios/atualizar/<int:id>", methods=["POST"])
@perfis_permitidos("Administrador")
def atualizar_usuario(id):


    usuario = Usuario.query.get_or_404(id)

    usuario.nome = request.form["nome"]

    usuario.email = request.form["email"]

    usuario.perfil = request.form["perfil"]

    usuario.ativo = "ativo" in request.form

    db.session.commit()

    flash("Usuário atualizado com sucesso.", "success")

    return redirect("/usuarios")


# ==========================================
# ALTERAR SENHA
# ==========================================

@usuarios.route("/usuarios/senha/<int:id>", methods=["POST"])
@perfis_permitidos("Administrador")
def alterar_senha(id):


    usuario = Usuario.query.get_or_404(id)

    usuario.definir_senha(request.form["senha"])

    db.session.commit()

    flash("Senha alterada com sucesso.", "success")

    return redirect("/usuarios")


# ==========================================
# ATIVAR
# ==========================================

@usuarios.route("/usuarios/ativar/<int:id>")
@perfis_permitidos("Administrador")
def ativar_usuario(id):


    usuario = Usuario.query.get_or_404(id)

    usuario.ativo = True

    db.session.commit()

    flash("Usuário ativado.", "success")

    return redirect("/usuarios")


# ==========================================
# DESATIVAR
# ==========================================

@usuarios.route("/usuarios/desativar/<int:id>")
@perfis_permitidos("Administrador")
def desativar_usuario(id):


    usuario = Usuario.query.get_or_404(id)

    if usuario.id != current_user.id:

        usuario.ativo = False

        db.session.commit()

        flash("Usuário desativado.", "warning")

    return redirect("/usuarios")


# ==========================================
# EXCLUIR
# ==========================================

@usuarios.route("/usuarios/excluir/<int:id>")
@perfis_permitidos("Administrador")
def excluir_usuario(id):



    usuario = Usuario.query.get_or_404(id)

    if usuario.id == current_user.id:

        flash("Você não pode excluir seu próprio usuário.", "danger")

        return redirect("/usuarios")

    db.session.delete(usuario)

    db.session.commit()

    flash("Usuário excluído com sucesso.", "success")

    return redirect("/usuarios")