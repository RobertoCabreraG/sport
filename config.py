import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://roob:roob1128@localhost:5432/dataDB'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración para el scraper
    SCRAPER_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    SCRAPER_TARGET_URL = 'https://livescore.football-data.co.uk/'
    SCRAPER_CACHE_TIMEOUT = 3600  # Tiempo en segundos antes de actualizar el caché (1 hora)
