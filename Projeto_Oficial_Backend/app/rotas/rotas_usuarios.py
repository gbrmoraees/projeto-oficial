from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from app.modelos import Usuario, db
from app.servicos import servico_usuarios

usuarios_bp = Blueprint("usuarios_bp", __name__)


@usuarios_bp.route("/registrar", methods=["POST"])
def registrar():
    dados = request.get_json()
    return servico_usuarios.ServicoUsuarios.registrar_usuario(dados)


@usuarios_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json()
    return servico_usuarios.ServicoUsuarios.login_usuario(dados)
