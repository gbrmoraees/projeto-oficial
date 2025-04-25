from flask import Flask

from app.extensoes import db, migrate, bcrypt, jwt
from app.configuracoes.config import Config
from app.rotas.rotas_jogos import jogo_bp
from app.usuarios.rotas import usuario_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializando extensões com a app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Registrando blueprints
    app.register_blueprint(usuario_bp, url_prefix="/usuarios")
    app.register_blueprint(jogo_bp, url_prefix="/jogos")

    return app
