from flask import Blueprint, jsonify
from database.db_utils import guardar_marcadores, obtener_ultimos_partidos, verificar_actualizacion_necesaria
from scraper.livescore_scraper import obtener_marcadores

# Creamos un Blueprint para las rutas de marcadores
marcadores_bp = Blueprint('marcadores', __name__, url_prefix='/marcadores')

@marcadores_bp.route('/', methods=['GET'])
def get_marcadores():
    """Endpoint para obtener los marcadores más recientes"""
    try:
        # Verificamos si necesitamos actualizar los marcadores
        if verificar_actualizacion_necesaria():
            # Obtenemos nuevos marcadores (limitados a 5)
            marcadores_nuevos = obtener_marcadores(limite=5)
            
            # Guardamos los nuevos marcadores en la base de datos
            guardar_marcadores(marcadores_nuevos)
        
        # Obtenemos los marcadores actualizados
        partidos = obtener_ultimos_partidos(limite=10)
        
        return jsonify([p.to_dict() for p in partidos])
    
    except Exception as e:
        return jsonify({"error": f"Error al obtener marcadores: {str(e)}"}), 500

@marcadores_bp.route('/actualizar', methods=['GET'])
def actualizar_marcadores():
    """Endpoint para forzar la actualización de marcadores"""
    try:
        # Obtenemos nuevos marcadores (limitados a 5)
        marcadores_nuevos = obtener_marcadores(limite=5)
        
        # Guardamos los nuevos marcadores en la base de datos
        contador = guardar_marcadores(marcadores_nuevos)
        
        return jsonify({
            "mensaje": f"Marcadores actualizados correctamente",
            "total": contador
        })
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar marcadores: {str(e)}"}), 500
