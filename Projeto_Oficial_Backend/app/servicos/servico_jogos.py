from flask import jsonify

from app import db
from app.modelos import Jogo, Usuario


class ServicoJogos:
    @staticmethod
    def listar_jogos():
        jogos = Jogo.query.all()
        return jsonify(
            [
                {
                    "id": j.id,
                    "titulo": j.titulo,
                    "descricao": j.descricao,
                    "downloads": j.downloads,
                }
                for j in jogos
            ]
        )

    @staticmethod
    def adicionar_jogo(dados, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario or not usuario.e_admin:
            return jsonify({"mensagem": "Não autorizado"}), 403
        jogo = Jogo(titulo=dados.get("titulo"), descricao=dados.get("descricao"))
        db.session.add(jogo)
        db.session.commit()
        return jsonify({"mensagem": "Jogo adicionado com sucesso"}), 201

    @staticmethod
    def remover_jogo(jogo_id, usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if not usuario or not usuario.e_admin:
            return jsonify({"mensagem": "Não autorizado"}), 403
        jogo = Jogo.query.get(jogo_id)
        if not jogo:
            return jsonify({"mensagem": "Jogo não encontrado"}), 404
        db.session.delete(jogo)
        db.session.commit()
        return jsonify({"mensagem": "Jogo removido com sucesso"})
