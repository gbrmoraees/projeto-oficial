import unittest

from app import app, db
from app.modelos import Usuario


class TestUsuarios(unittest.TestCase):
    """Classe de testes para funcionalidades relacionadas a usuários"""

    def setUp(self):
        """Configuração inicial antes de cada teste"""
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Limpeza do banco de dados após cada teste"""
        db.session.remove()
        db.drop_all()

    def test_registro_usuario(self):
        """Testa o registro de um novo usuário"""
        resposta = self.app.post(
            "/usuarios/registrar", json={"nome_usuario": "teste", "senha": "1234"}
        )
        self.assertEqual(
            resposta.status_code, 201
        )  # Verifica se o status HTTP é 201 (Criado)
        self.assertIn(
            "Usuário criado com sucesso", resposta.get_json()["mensagem"]
        )  # Confirma a mensagem de sucesso

    def test_login_usuario(self):
        """Testa o login de um usuário existente"""
        # Primeiro, registra um usuário
        self.app.post(
            "/usuarios/registrar", json={"nome_usuario": "teste", "senha": "1234"}
        )

        # Agora, tenta fazer login
        resposta = self.app.post(
            "/usuarios/login", json={"nome_usuario": "teste", "senha": "1234"}
        )
        self.assertEqual(
            resposta.status_code, 200
        )  # Verifica se o login foi bem-sucedido
        self.assertIn(
            "token_acesso", resposta.get_json()
        )  # Confirma que um token de acesso foi gerado

    def test_login_falha(self):
        """Testa login com credenciais incorretas"""
        resposta = self.app.post(
            "/usuarios/login", json={"nome_usuario": "invalido", "senha": "errada"}
        )
        self.assertEqual(resposta.status_code, 401)  # Espera um erro de autorização
        self.assertIn(
            "Credenciais inválidas", resposta.get_json()["mensagem"]
        )  # Verifica a mensagem de erro
