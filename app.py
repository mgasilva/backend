from flask import Flask, jsonify
from elementos import elementos_bp
from flask_cors import CORS
from flask_restx import Api
import json

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(elementos_bp)
    return app

app = create_app()

api = Api(
    app,
    title="API da Tabela Periódica",
    version="1.0",
    description="API REST para consulta e inclusão de dados da Tabela Periódica",
    doc="/swagger"
)

@app.route("/openapi.json")
def swagger():
    with open("swagger.json", "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(debug=True)
