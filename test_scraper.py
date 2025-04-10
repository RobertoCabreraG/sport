# test_scraper.py
import sys
import os

# Añadir el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper.livescore_scraper import obtener_marcadores
from config import Config

# Ejecutar el scraper
print("Iniciando prueba del scraper...")
marcadores = obtener_marcadores(limite=5)

# Imprimir resultados para verificar
print(f"Número de marcadores obtenidos: {len(marcadores)}")
for idx, marcador in enumerate(marcadores, 1):
    print(f"\nMarcador {idx}:")
    print(f"Región: {marcador['region']}")
    print(f"Competición: {marcador['competition']}")
    print(f"Equipos: {marcador['team_home']} vs {marcador['team_away']}")
    print(f"Resultado: {marcador['score_home']} - {marcador['score_away']}")
    print(f"Estado: {marcador['status']}")
    print(f"Hora: {marcador['match_time']}")