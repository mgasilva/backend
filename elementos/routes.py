from flask import Blueprint, jsonify, abort
from db import get_db_connection

elementos_bp = Blueprint(
    "elementos",
    __name__,
    url_prefix="/elementos"
)

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
