from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from database.database import db
from models.calendario import Calendario
from models.planejamento import Planejamento


calendario = Blueprint(
    "calendario",
    __name__,
    url_prefix="/calendario"
)


# ==========================================
# LISTAR CALENDÁRIO
# ==========================================

@calendario.route("/")
@login_required
def listar_calendario():

    eventos = Calendario.query.order_by(
        Calendario.data_inicio
    ).all()


    eventos_json = []


    for evento in eventos:

        eventos_json.append({

            "id": evento.id,

            "title": evento.titulo,

            "start": (
                str(evento.data_inicio)
                + (
                    f"T{evento.hora_inicio}"
                    if evento.hora_inicio
                    else ""
                )
            ),

            "end": (
                str(evento.data_fim)
                + (
                    f"T{evento.hora_fim}"
                    if evento.hora_fim
                    else ""
                )
                if evento.data_fim
                else None
            ),

            "color": evento.cor or "#198754",

            "url": url_for(
                "calendario.editar_compromisso",
                id=evento.id
            )

        })


    return render_template(
        "calendario.html",
        eventos=eventos_json
    )



# ==========================================
# NOVO COMPROMISSO
# ==========================================

@calendario.route("/novo", methods=["GET", "POST"])
@login_required
def novo_compromisso():


    planejamentos = Planejamento.query.order_by(
        Planejamento.id.desc()
    ).all()



    if request.method == "POST":


        evento = Calendario(

            titulo=request.form["titulo"],

            descricao=request.form.get("descricao"),

            data_inicio=request.form["data_inicio"],

            data_fim=request.form.get("data_fim") or None,

            hora_inicio=request.form.get("hora_inicio") or None,

            hora_fim=request.form.get("hora_fim") or None,

            status=request.form.get("status"),

            cor=request.form.get("cor"),


            planejamento_id=request.form.get("planejamento_id")
            or None

        )


        db.session.add(evento)

        db.session.commit()


        flash(
            "Compromisso cadastrado com sucesso!",
            "success"
        )


        return redirect(
            url_for("calendario.listar_calendario")
        )


    return render_template(
        "novo_compromisso.html",
        planejamentos=planejamentos
    )





# ==========================================
# EDITAR COMPROMISSO
# ==========================================

@calendario.route(
    "/editar/<int:id>",
    methods=["GET","POST"]
)
@login_required
def editar_compromisso(id):


    evento = Calendario.query.get_or_404(id)



    planejamentos = Planejamento.query.order_by(
        Planejamento.id.desc()
    ).all()



    if request.method == "POST":


        evento.titulo = request.form["titulo"]

        evento.descricao = request.form.get("descricao")


        evento.data_inicio = request.form["data_inicio"]

        evento.data_fim = request.form.get("data_fim") or None


        evento.hora_inicio = request.form.get("hora_inicio") or None

        evento.hora_fim = request.form.get("hora_fim") or None


        evento.status = request.form.get("status")


        evento.cor = request.form.get("cor")


        evento.planejamento_id = (
            request.form.get("planejamento_id")
            or None
        )



        db.session.commit()



        flash(
            "Compromisso atualizado!",
            "success"
        )



        return redirect(
            url_for("calendario.listar_calendario")
        )




    return render_template(
        "editar_compromisso.html",
        evento=evento,
        planejamentos=planejamentos
    )





# ==========================================
# EXCLUIR COMPROMISSO
# ==========================================

@calendario.route("/excluir/<int:id>")
@login_required
def excluir_compromisso(id):


    evento = Calendario.query.get_or_404(id)



    db.session.delete(evento)

    db.session.commit()



    flash(
        "Compromisso excluído!",
        "success"
    )



    return redirect(
        url_for("calendario.listar_calendario")
    )