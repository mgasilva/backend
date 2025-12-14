from flask import Blueprint, jsonify, abort
from db import get_db_connection

elementos_bp = Blueprint(
    "elementos",
    __name__,
    url_prefix="/elementos"
)


#Rota que lista todos os elementos
@elementos_bp.route("", methods=["GET"])
def listar_elementos():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            numero_atomico,
            simbolo,
            nome,
            massa_atomica,
            categoria
        FROM elementos
        ORDER BY numero_atomico
    """)

    rows = cursor.fetchall()
    conn.close()

    elementos = [
        {
            "numero_atomico": row["numero_atomico"],
            "simbolo": row["simbolo"],
            "nome": row["nome"],
            "massa_atomica": row["massa_atomica"],
            "categoria": row["categoria"]
        }
        for row in rows
    ]

    return jsonify(elementos)

#Rota que retorna os detalhes de um elemento
@elementos_bp.route("/<int:numero_atomico>", methods=["GET"])
def detalhe_elemento(numero_atomico):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            numero_atomico,
            simbolo,
            nome,
            massa_atomica,
            categoria
        FROM elementos
        WHERE numero_atomico = ?
    """, (numero_atomico,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        abort(404, description="Elemento não encontrado")

    elemento = {
        "numero_atomico": row["numero_atomico"],
        "simbolo": row["simbolo"],
        "nome": row["nome"],
        "massa_atomica": row["massa_atomica"],
        "categoria": row["categoria"]
    }

    return elemento

#rota que retorna os detalhes adicionais de um elemento
@elementos_bp.route("/<int:numero_atomico>/info_adicional", methods=["GET"])
def info_adicional_elemento(numero_atomico):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            info
        FROM informacoes
        WHERE numero_atomico = ?
        ORDER BY id
    """, (numero_atomico,))

    rows = cursor.fetchall()
    conn.close()

    informacoes = [
        {
            "informacoes": row["info"]
        }
        for row in rows
    ]

    return {
        "numero_atomico": numero_atomico,
        "info_adicional": informacoes
    }

from flask import request

#rota que adiciona informações a um elemento (método POST)
@elementos_bp.route("/<int:numero_atomico>/info_adicional", methods=["POST"])
def post_info_adicional(numero_atomico):
    dados = request.get_json(silent=True)

    if not dados or "info" not in dados:
        return {
            "status": "erro",
            "mensagem": "Campo 'info' é obrigatório"
        }, 400

    info = dados["info"].strip()

    if not info:
        return {
            "status": "erro",
            "mensagem": "Campo 'info' não pode ser vazio"
        }, 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # garante que o elemento existe
    cursor.execute(
        "SELECT 1 FROM elementos WHERE numero_atomico = ?",
        (numero_atomico,)
    )
    if cursor.fetchone() is None:
        conn.close()
        return {
            "status": "erro",
            "mensagem": "Elemento não encontrado"
        }, 404

    cursor.execute("""
        INSERT INTO informacoes (numero_atomico, info)
        VALUES (?, ?)
    """, (numero_atomico, info))

    conn.commit()
    conn.close()

    return {
        "status": "ok",
        "mensagem": "Informação adicional inserida com sucesso"
    }, 201
