from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.views.auth_views import auth_bp  # Importa o Blueprint antes, mas ainda não o registra

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)  # A variável "app" é criada aqui
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Kenay/OneDrive/Área de Trabalho/Projeto final/migrations/meu_banco.db'    
    app.config['SECRET_KEY'] = 'uma_chave_secreta_super_segura'
    db.init_app(app)

    # Agora que "app" já foi definido, o Blueprint pode ser registrado
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app