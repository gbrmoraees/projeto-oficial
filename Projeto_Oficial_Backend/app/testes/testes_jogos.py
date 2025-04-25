import unittest

from app import app, db
from app.modelos import Jogo, Usuario


class TestJogos(unittest.TestCase):
    """Classe de testes para funcionalidades relacionadas a jogos"""

    def setUp(self):
        """Configuração inicial antes de cada teste"""
        self.app = app.test_client()
        db.create_all()

        # Usuário administrador para realizar testes
        usuario_admin = Usuario(nome_usuario="admin", senha="1234", e_admin=True)
        db.session.add(usuario_admin)
        db.session.commit()
        self.admin_id = usuario_admin.id

    def tearDown(self):
        """Limpeza do banco de dados após cada teste"""
        db.session.remove()
        db.drop_all()

    def test_listar_jogos(self):
        """Testa se a listagem de jogos retorna status 200"""
        resposta = self.app.get("/jogos/")
        self.assertEqual(resposta.status_code, 200)

    def test_adicionar_jogo(self):
        """Testa a adição de um novo jogo por um administrador"""
        # Simulação de login para obter token de administrador
        resposta_login = self.app.post(
            "/usuarios/login", json={"nome_usuario": "admin", "senha": "1234"}
        )
        token = resposta_login.get_json().get("token_acesso")

        # Enviar requisição para adicionar jogo com autenticação
        resposta = self.app.post(
            "/jogos/adicionar",
            json={"titulo": "Novo Jogo", "descricao": "Descrição do jogo"},
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(
            resposta.status_code, 201
        )  # Verifica se o jogo foi criado com sucesso
        self.assertIn("Jogo adicionado com sucesso", resposta.get_json()["mensagem"])

    def test_adicionar_jogo_nao_autorizado(self):
        """Testa tentativa de adicionar jogo sem permissão"""
        resposta = self.app.post(
            "/jogos/adicionar",
            json={"titulo": "Jogo Não Autorizado", "descricao": "Tentativa de adição"},
            headers={"Authorization": "Bearer token_invalido"},
        )
        self.assertEqual(resposta.status_code, 401)  # Espera erro de autenticação

    def test_remover_jogo(self):
        """Testa a remoção de um jogo por um administrador"""
        # Simulação de login para obter token de administrador
        resposta_login = self.app.post(
            "/usuarios/login", json={"nome_usuario": "admin", "senha": "1234"}
        )
        token = resposta_login.get_json().get("token_acesso")

        # Criar um jogo no banco para testar remoção
        novo_jogo = Jogo(titulo="Jogo Teste", descricao="Teste")
        db.session.add(novo_jogo)
        db.session.commit()

        # Enviar requisição para remover o jogo
        resposta = self.app.delete(
            f"/jogos/remover/{novo_jogo.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(resposta.status_code, 200)  # Espera sucesso na remoção
        self.assertIn("Jogo removido com sucesso", resposta.get_json()["mensagem"])

    def test_remover_jogo_nao_autorizado(self):
        """Testa tentativa de remover jogo sem permissão"""
        # Criar um jogo no banco para testar remoção sem autorização
        novo_jogo = Jogo(titulo="Jogo Sem Permissão", descricao="Teste de falha")
        db.session.add(novo_jogo)
        db.session.commit()

        # Enviar requisição para remover o jogo sem autenticação
        resposta = self.app.delete(f"/jogos/remover/{novo_jogo.id}")
        self.assertEqual(resposta.status_code, 401)  # Espera erro de autenticação
