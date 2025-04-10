# test_scraper_db.py
import sys
import os

# Ensure the root directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.livescore_scraper import obtener_marcadores
from database.db_utils import guardar_marcadores
from app import app  # Importamos la app Flask para usar su contexto
from models import db

print("Iniciando prueba del scraper con guardado en base de datos...")

# Número de partidos a obtener
LIMITE = 5

# Obtenemos los marcadores
marcadores = obtener_marcadores(limite=LIMITE)

print(f"Número de marcadores obtenidos: {len(marcadores)}")
for idx, marcador in enumerate(marcadores, 1):
    print(f"\nMarcador {idx}:")
    print(f"Región: {marcador['region']}")
    print(f"Competición: {marcador['competition']}")
    print(f"Equipos: {marcador['team_home']} vs {marcador['team_away']}")
    print(f"Resultado: {marcador['score_home']} - {marcador['score_away']}")
    print(f"Estado: {marcador['status']}")
    print(f"Hora: {marcador['match_time']}")

# Guardamos los marcadores en la base de datos usando el contexto de la aplicación
with app.app_context():
    try:
        # Creamos las tablas si no existen
        db.create_all()
        
        # Guardamos los marcadores
        num_guardados = guardar_marcadores(marcadores)
        
        print(f"\nSe guardaron {num_guardados} marcadores en la base de datos.")
        print("Proceso completado con éxito.")
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")