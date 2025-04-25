from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.rotas.rotas_jogos import jogos_bp
from app.rotas.rotas_usuarios import usuarios_bp

app = Flask(__name__)
app.config.from_object("configuracao.Config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(jogos_bp, url_prefix="/jogos")
