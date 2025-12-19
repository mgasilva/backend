from flask import Flask, jsonify, render_template
from elementos import elementos_bp
from flask_cors import CORS
from flask_restx import Api
from flask_swagger_ui import get_swaggerui_blueprint
import json

SWAGGER_URL = "/swagger"
API_URL = "/openapi.json"

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

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "API da Tabela Periódica"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/docs")
def docs():
    return render_template("swagger.html")

@app.route("/openapi.json")
def swagger():
    with open("swagger.json", "r", encoding="utf-8") as f:
        return jsonify(json.load(f))

if __name__ == "__main__":
    app.run(debug=True)
