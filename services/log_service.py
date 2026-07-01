from flask import request
from flask_login import current_user

from database.database import db
from models.log import Log


def registrar_log(acao):

    """
    Registra uma ação realizada no sistema.
    """

    if current_user.is_authenticated:
        usuario = current_user.nome
    else:
        usuario = "Sistema"

    log = Log(

        usuario=usuario,

        acao=acao,

        ip=request.remote_addr

    )

    db.session.add(log)

    db.session.commit()


def registrar_log_personalizado(usuario, acao, ip=None):

    """
    Permite registrar logs informando o usuário manualmente.
    """

    log = Log(

        usuario=usuario,

        acao=acao,

        ip=ip

    )

    db.session.add(log)

    db.session.commit()