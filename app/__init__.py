from flask import Flask

from .config import Config
from .extensions import db, login_manager, csrf, migrate, limiter
from .models import User

from .auth import auth_bp
from .dashboard import dashboard_bp
from .turmas import turmas_bp
from .analises import analises_bp
from .reports import reports_bp
from .uploads import uploads_bp

# Importa as rotas de upload.
# Isso registra a função upload() no Blueprint.
from .uploads import routes as uploads_routes


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    # Inicialização das extensões
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)

    # Configuração do Flask-Login
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Entre na sua conta para continuar."

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Registro dos Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(turmas_bp, url_prefix="/turmas")
    app.register_blueprint(analises_bp, url_prefix="/analises")
    app.register_blueprint(reports_bp, url_prefix="/relatorios")
    app.register_blueprint(uploads_bp, url_prefix="/uploads")

    # Rota de verificação
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app