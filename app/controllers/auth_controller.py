from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db

def register_user(data):
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "O email fornecido já está registrado.", "status": "fail"}), 400

    new_user = User(email=email, senha=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso!", "status": "success"}), 201

def login_user(data):
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.senha, password):
        return jsonify({"message": "Login bem-sucedido!", "status": "success"}), 200

    return jsonify({"error": "Email ou senha incorretos.", "status": "fail"}), 401

def list_all_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "email": user.email} for user in users])