from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from models.usuario import Usuario
from services.log_service import registrar_log

auth = Blueprint("auth", __name__)


# ==========================
# LOGIN
# ==========================

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        senha = request.form["senha"]

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:

            if not usuario.ativo:

                flash(
                    "Este usuário está desativado.",
                    "warning"
                )

                return render_template("login.html")

            if usuario.verificar_senha(senha):

                login_user(usuario)

                registrar_log("Entrou no sistema")

                return redirect(url_for("dashboard.inicio"))

        flash(
            "Usuário ou senha inválidos.",
            "danger"
        )

    return render_template("login.html")


# ==========================
# LOGOUT
# ==========================

@auth.route("/logout")
@login_required
def logout():

    registrar_log("Saiu do sistema")

    logout_user()

    flash(
        "Logout realizado com sucesso.",
        "success"
    )

    return redirect(url_for("auth.login"))