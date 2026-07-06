from functools import wraps

from flask import flash, redirect
from flask_login import current_user, login_required


def perfis_permitidos(*perfis):

    def decorator(func):

        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):

            if current_user.perfil not in perfis:

                flash(
                    "Você não possui permissão para acessar esta página.",
                    "danger"
                )

                return redirect("/")

            return func(*args, **kwargs)

        return wrapper

    return decorator