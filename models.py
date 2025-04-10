from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Region(db.Model):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    competitions = db.relationship('Competition', backref='region', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Competition(db.Model):
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)
    
    matches = db.relationship('Match', backref='competition', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "region_id": self.region_id,
            "region_name": self.region.name if self.region else None
        }

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    home_matches = db.relationship('Match', foreign_keys='Match.team_home_id', backref='home_team', lazy=True)
    away_matches = db.relationship('Match', foreign_keys='Match.team_away_id', backref='away_team', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)
    team_home_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    team_away_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    score_home = db.Column(db.Integer, nullable=True)
    score_away = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), nullable=False)
    match_time = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "competition": self.competition.name if self.competition else None,
            "region": self.competition.region.name if self.competition and self.competition.region else None,
            "team_home": self.home_team.name if self.home_team else None,
            "team_away": self.away_team.name if self.away_team else None,
            "score_home": self.score_home,
            "score_away": self.score_away,
            "status": self.status,
            "match_time": self.match_time,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Mantener la clase Usuario por compatibilidad
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo
        }