from datetime import datetime

from app.extensoes import db


class Jogo(db.Model):
    __tablename__ = "jogos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "url": self.url,
            "criado_em": self.criado_em.strftime("%Y-%m-%d %H:%M:%S"),
        }
