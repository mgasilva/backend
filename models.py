# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Elemento(db.Model):
    __tablename__ = "elementos"

    numero = db.Column(db.Integer, primary_key=True)
    simbolo = db.Column(db.String(5), nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    massa_atomica = db.Column(db.Float, nullable=True)
    categoria = db.Column(db.String(80), nullable=True)

    def to_dict(self):
        return {
            "numero": self.numero,
            "simbolo": self.simbolo,
            "nome": self.nome,
            "massa_atomica": self.massa_atomica,
            "categoria": self.categoria,
        }


class InfoAdicional(db.Model):
    __tablename__ = "infos_adicionais"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numero = db.Column(
        db.Integer,
        db.ForeignKey("elementos.numero"),
        nullable=False
    )
    titulo = db.Column(db.String(150), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    elemento = db.relationship("Elemento", backref="infos_adicionais")

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "titulo": self.titulo,
            "texto": self.texto,
            "criado_em": self.criado_em.isoformat(),
        }


def init_db(app):
    """Inicializa o banco e faz um seed básico de elementos se estiver vazio."""
    db.init_app(app)
    with app.app_context():
        db.create_all()

        # Se não houver elementos, cria alguns de exemplo
        if Elemento.query.count() == 0:
            elementos_seed = [
                {"numero": 1, "simbolo": "H",  "nome": "Hidrogênio", "massa_atomica": 1.008,  "categoria": "não metal"},
                {"numero": 2, "simbolo": "He", "nome": "Hélio",      "massa_atomica": 4.0026, "categoria": "gás nobre"},
                {"numero": 3, "simbolo": "Li", "nome": "Lítio",      "massa_atomica": 6.94,   "categoria": "metal alcalino"},
                {"numero": 6, "simbolo": "C",  "nome": "Carbono",    "massa_atomica": 12.011, "categoria": "não metal"},
                {"numero": 7, "simbolo": "N",  "nome": "Nitrogênio", "massa_atomica": 14.007, "categoria": "não metal"},
                {"numero": 8, "simbolo": "O",  "nome": "Oxigênio",   "massa_atomica": 15.999, "categoria": "não metal"},
                {"numero": 10, "simbolo": "Ne","nome": "Neônio",     "massa_atomica": 20.180, "categoria": "gás nobre"},
            ]
            for e in elementos_seed:
                db.session.add(Elemento(**e))
            db.session.commit()
            print("🌱 Banco inicializado com elementos de exemplo.")
