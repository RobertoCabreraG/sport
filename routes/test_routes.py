from flask import Blueprint, jsonify
from models import db
from sqlalchemy import text

# Creamos un Blueprint para las rutas de prueba
test_bp = Blueprint('test', __name__, url_prefix='/test')

@test_bp.route('/db', methods=['GET'])
def test_db():
    try:
        resultado = db.session.execute(text('SELECT 1')).scalar()
        return jsonify({"conexion": "exitosa", "resultado": resultado})
    except Exception as e:
        return jsonify({"conexion": "fallida", "error": str(e)}), 500