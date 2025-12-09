# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Elemento, InfoAdicional, init_db
import requests


def create_app():
    app = Flask(__name__)

    # Banco SQLite local
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///elementos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)  # libera acesso do front-end em outra porta (ex: 5173, 5500, etc.)
    init_db(app)

    # 1) Ver informações de um elemento + infos adicionais
    @app.route("/api/info/<int:numero>", methods=["GET"])
    def get_info(numero):
        elemento = Elemento.query.get(numero)
        if not elemento:
            return jsonify({"error": "Elemento não encontrado"}), 404

        infos = (
            InfoAdicional.query
            .filter_by(numero=numero)
            .order_by(InfoAdicional.criado_em.desc())
            .all()
        )

        return jsonify({
            "elemento": elemento.to_dict(),
            "infos": [info.to_dict() for info in infos],
        })

    # 2) Acrescentar informações (POST)
    @app.route("/api/add_info", methods=["POST"])
    def add_info():
        data = request.get_json() or {}

        for campo in ("numero", "titulo", "texto"):
            if campo not in data:
                return jsonify({"error": f"Campo obrigatório ausente: {campo}"}), 400

        numero = data["numero"]
        elemento = Elemento.query.get(numero)
        if not elemento:
            return jsonify({"error": "Elemento não existe no banco"}), 404

        info = InfoAdicional(
            numero=numero,
            titulo=data["titulo"],
            texto=data["texto"]
        )
        db.session.add(info)
        db.session.commit()

        return jsonify(info.to_dict()), 201

    # 3) Busca texto na web (Wikipedia se possível, senão simulado)
    @app.route("/api/search/web", methods=["GET"])
    def search_web():
        termo = request.args.get("q")
        if not termo:
            return jsonify({"error": "Parâmetro 'q' é obrigatório"}), 400

        # Tenta buscar na Wikipedia (em inglês, só pra ter algo real)
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{termo}"
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                data = r.json()
                resumo = data.get("extract") or ""
                titulo = data.get("title") or termo
                page_url = data.get("content_urls", {}).get("desktop", {}).get("page")

                return jsonify({
                    "source": "wikipedia",
                    "title": titulo,
                    "summary": resumo,
                    "url": page_url,
                })
        except Exception as e:
            print("Falha ao consultar Wikipedia:", e)

        # Fallback: resposta simulada, nunca quebra o MVP
        return jsonify({
            "source": "simulado",
            "title": termo,
            "summary": f"Resumo simulado para '{termo}'. Aqui você pode integrar outra API depois.",
            "url": None,
        })

    # 4) Busca imagens na web (simulada com uma URL genérica)
    @app.route("/api/search/images", methods=["GET"])
    def search_images():
        termo = request.args.get("q")
        if not termo:
            return jsonify({"error": "Parâmetro 'q' é obrigatório"}), 400

        # Aqui você pode plugar Unsplash, Bing, etc. Por enquanto, simulação:
        exemplo_url = "https://images.pexels.com/photos/5860305/pexels-photo-5860305.jpeg"

        return jsonify({
            "query": termo,
            "urls": [exemplo_url],
        })

    # 5) Rota de teste simples
    @app.route("/api/ping")
    def ping():
        return jsonify({"status": "ok"})

    return app


app = create_app()

if __name__ == "__main__":
    # debug=True só para desenvolvimento
    app.run(debug=True)
