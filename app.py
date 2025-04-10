from flask import Flask, jsonify
from config import Config
from models import db, Usuario
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return jsonify({"mensaje": "API viva y coleando"})

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])

@app.route('/test-db')  # 👈 ¡Movido aquí!
def test_db():
    try:
        resultado = db.session.execute(text('SELECT 1')).scalar()
        return jsonify({"conexion": "exitosa", "resultado": resultado})
    except Exception as e:
        return jsonify({"conexion": "fallida", "error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
