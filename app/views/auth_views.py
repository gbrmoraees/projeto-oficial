from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import register_user, login_user, list_all_users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    return register_user(request.get_json())

@auth_bp.route('/login', methods=['POST'])
def login():
    return login_user(request.get_json())

@auth_bp.route('/users', methods=['GET'])
def list_users():
    return list_all_users()