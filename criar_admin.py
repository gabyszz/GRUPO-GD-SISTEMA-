from app import app
from database.database import db
from models.usuario import Usuario

with app.app_context():
    # Verifica se já existe um usuário com esse e-mail
    usuario = Usuario.query.filter_by(email="admin@gd.com").first()

    if usuario:
        print("Usuário já existe.")
    else:
        usuario = Usuario(
            nome="Administrador",
            email="admin@gd.com",
            perfil="Administrador",
            ativo=True
        )

        usuario.definir_senha("123456")

        db.session.add(usuario)
        db.session.commit()

        print("Usuário administrador criado com sucesso!")