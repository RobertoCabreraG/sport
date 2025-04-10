import requests
from bs4 import BeautifulSoup
import re
from config import Config

def obtener_marcadores(limite=5):
    """
    Función para scrapear los marcadores de fútbol de livescore.football-data.co.uk
    
    Args:
        limite (int): Número máximo de partidos a obtener
    
    Returns:
        list: Lista de diccionarios con los marcadores obtenidos
    """
    url = Config.SCRAPER_TARGET_URL
    headers = {
        'User-Agent': Config.SCRAPER_USER_AGENT
    }
    
    try:
        # Realizamos la petición a la página
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parseamos el contenido HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Lista para almacenar los resultados
        matches = []
        
        # Intentamos todas las estrategias de scraping, pero si no funciona, 
        # usamos los datos de ejemplo
        matches = parse_live_data(soup, limite)
        
        # Si no se encontraron partidos con los métodos anteriores, usamos el ejemplo
        if not matches:
            matches = parse_example_data(limite)
        
        return matches[:limite]  # Aseguramos que solo devolvemos el número especificado
    
    except Exception as e:
        print(f"Error al obtener marcadores: {e}")
        # Si hay algún error, usamos los datos de ejemplo
        return parse_example_data(limite)

def parse_live_data(soup, limite):
    """Intenta parsear los datos directamente del sitio web"""
    matches = []
    contador_partidos = 0
    current_region = None
    current_competition = None
    
    # Intenta encontrar los bloques de partidos (ajustar según la estructura real del sitio)
    blocks = soup.find_all('div', class_='match-block')
    
    if blocks:
        for block in blocks:
            if contador_partidos >= limite:
                break
            
            # Extraemos información de la región y competencia
            header = block.find_previous('h2', class_='competition-header')
            if header:
                header_text = header.text.strip()
                parts = header_text.rsplit(' ', 1)
                if len(parts) == 2:
                    current_region, current_competition = parts
            
            # Extraemos información del partido
            teams = block.find_all('div', class_='team-name')
            scores = block.find_all('div', class_='score')
            status_elem = block.find('div', class_='match-status')
            
            if len(teams) >= 2 and len(scores) >= 2 and status_elem:
                team_home = teams[0].text.strip()
                team_away = teams[1].text.strip()
                score_home = int(scores[0].text.strip())
                score_away = int(scores[1].text.strip())
                status = status_elem.text.strip()
                
                match_time_elem = block.find('div', class_='match-time')
                match_time = match_time_elem.text.strip() if match_time_elem else "00:00"
                
                match_data = {
                    'region': current_region,
                    'competition': current_competition,
                    'team_home': team_home,
                    'team_away': team_away,
                    'score_home': score_home,
                    'score_away': score_away,
                    'status': status,
                    'match_time': match_time
                }
                
                matches.append(match_data)
                contador_partidos += 1
    
    return matches

def parse_example_data(limite):
    
    return "Fail scraper"