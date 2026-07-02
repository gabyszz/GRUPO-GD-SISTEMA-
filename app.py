from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_migrate import Migrate

from database.database import db

# ==========================
# MODELS
# ==========================

from models.cliente import Cliente
from models.projeto import Projeto
from models.planejamento import Planejamento
from models.funcionario import Funcionario
from models.equipe import Equipe
from models.veiculo import Veiculo
from models.equipamento import Equipamento
from models.usuario import Usuario
from models.log import Log

# ==========================
# ROTAS
# ==========================

from routes.auth import auth
from routes.dashboard import dashboard
from routes.clientes import clientes
from routes.projetos import projetos
from routes.planejamento import planejamento
from routes.funcionarios import funcionarios
from routes.equipes import equipes
from routes.veiculos import veiculos
from routes.equipamentos import equipamentos
from routes.usuarios import usuarios

# ==========================
# APP
# ==========================

app = Flask(__name__)

# ==========================
# CONFIGURAÇÕES
# ==========================

app.config.from_object("config.Config")

# ==========================
# BANCO DE DADOS
# ==========================

db.init_app(app)

# ==========================
# MIGRATIONS
# ==========================

migrate = Migrate(app, db)

# ==========================
# CSRF
# ==========================

csrf = CSRFProtect(app)


@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)


# ==========================
# LOGIN
# ==========================

login_manager = LoginManager()

login_manager.login_view = "auth.login"

login_manager.login_message = "Faça login para continuar."

login_manager.login_message_category = "warning"

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):

    return Usuario.query.get(int(user_id))


# ==========================
# BLUEPRINTS
# ==========================

app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(clientes)
app.register_blueprint(projetos)
app.register_blueprint(planejamento)
app.register_blueprint(funcionarios)
app.register_blueprint(equipes)
app.register_blueprint(veiculos)
app.register_blueprint(equipamentos)
app.register_blueprint(usuarios)

# ==========================
# EXECUÇÃO
# ==========================

if __name__ == "__main__":
    app.run(debug=True)