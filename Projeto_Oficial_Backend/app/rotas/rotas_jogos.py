from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.servicos import servico_jogos

jogos_bp = Blueprint("jogos_bp", __name__)


@jogos_bp.route("/", methods=["GET"])
def listar_jogos():
    return servico_jogos.ServicoJogos.listar_jogos()


@jogos_bp.route("/adicionar", methods=["POST"])
@jwt_required()
def adicionar_jogo():
    usuario_atual = get_jwt_identity()
    return servico_jogos.ServicoJogos.adicionar_jogo(request.get_json(), usuario_atual)


@jogos_bp.route("/remover/<int:jogo_id>", methods=["DELETE"])
@jwt_required()
def remover_jogo(jogo_id):
    usuario_atual = get_jwt_identity()
    return servico_jogos.ServicoJogos.remover_jogo(jogo_id, usuario_atual)
