from models import db, Region, Competition, Team, Match
from datetime import datetime

def guardar_partido(partido_data):
    """
    Guarda un partido en la base de datos, creando o recuperando las entidades relacionadas
    
    Args:
        partido_data (dict): Diccionario con los datos del partido
        
    Returns:
        Match: Objeto Match guardado
    """
    try:
        # 1. Obtener o crear la región
        region = Region.query.filter_by(name=partido_data['region']).first()
        if not region:
            region = Region(name=partido_data['region'])
            db.session.add(region)
            db.session.flush()
        
        # 2. Obtener o crear la competencia
        competition = Competition.query.filter_by(name=partido_data['competition'], region_id=region.id).first()
        if not competition:
            competition = Competition(name=partido_data['competition'], region_id=region.id)
            db.session.add(competition)
            db.session.flush()
        
        # 3. Obtener o crear el equipo local
        team_home = Team.query.filter_by(name=partido_data['team_home']).first()
        if not team_home:
            team_home = Team(name=partido_data['team_home'])
            db.session.add(team_home)
            db.session.flush()
        
        # 4. Obtener o crear el equipo visitante
        team_away = Team.query.filter_by(name=partido_data['team_away']).first()
        if not team_away:
            team_away = Team(name=partido_data['team_away'])
            db.session.add(team_away)
            db.session.flush()
        
        # 5. Crear el partido
        match = Match(
            competition_id=competition.id,
            team_home_id=team_home.id,
            team_away_id=team_away.id,
            score_home=partido_data['score_home'],
            score_away=partido_data['score_away'],
            status=partido_data['status'],
            match_time=partido_data['match_time']
        )
        
        db.session.add(match)
        db.session.flush()
        
        return match
    
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar partido: {e}")
        raise e

def guardar_marcadores(marcadores):
    """
    Guarda una lista de marcadores en la base de datos
    
    Args:
        marcadores (list): Lista de diccionarios con datos de marcadores
        
    Returns:
        int: Número de marcadores guardados
    """
    contador = 0
    
    try:
        for marcador in marcadores:
            guardar_partido(marcador)
            contador += 1
        
        db.session.commit()
        return contador
    
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar marcadores: {e}")
        return 0

def obtener_ultimos_partidos(limite=10):
    """
    Obtiene los últimos partidos de la base de datos
    
    Args:
        limite (int): Cantidad máxima de partidos a obtener
        
    Returns:
        list: Lista de objetos Match
    """
    return Match.query.order_by(Match.created_at.desc()).limit(limite).all()

def verificar_actualizacion_necesaria(horas=1):
    """
    Verifica si es necesario actualizar los marcadores
    
    Args:
        horas (int): Horas desde la última actualización para considerar necesaria una nueva
        
    Returns:
        bool: True si se necesita actualización, False en caso contrario
    """
    ultimo_partido = Match.query.order_by(Match.created_at.desc()).first()
    
    if not ultimo_partido:
        return True
    
    tiempo_transcurrido = datetime.now() - ultimo_partido.created_at
    return tiempo_transcurrido.total_seconds() > (horas * 3600)