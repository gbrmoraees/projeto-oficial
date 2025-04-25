from flask import jsonify
from flask_jwt_extended import create_access_token

from app import bcrypt, db
from app.modelos import Usuario


class ServicoUsuarios:
    @staticmethod
    def registrar_usuario(dados):
        nome_usuario = dados.get("nome_usuario")
        senha = bcrypt.generate_password_hash(dados.get("senha")).decode("utf-8")
        usuario = Usuario(nome_usuario=nome_usuario, senha=senha)
        db.session.add(usuario)
        db.session.commit()
        return jsonify({"mensagem": "Usuário criado com sucesso"}), 201

    @staticmethod
    def login_usuario(dados):
        usuario = Usuario.query.filter_by(
            nome_usuario=dados.get("nome_usuario")
        ).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, dados.get("senha")):
            token_acesso = create_access_token(identity=usuario.id)
            return jsonify({"token_acesso": token_acesso})
        return jsonify({"mensagem": "Credenciais inválidas"}), 401
