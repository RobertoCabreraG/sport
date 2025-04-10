from flask import Flask
from config import Config
from models import db
from routes.usuarios_routes import usuarios_bp
from routes.marcadores_routes import marcadores_bp
from routes.test_routes import test_bp

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Registramos los blueprints
app.register_blueprint(usuarios_bp)
app.register_blueprint(marcadores_bp)
app.register_blueprint(test_bp)

@app.route('/')
def index():
    return {"mensaje": "API de LiveScore"}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
