import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://roob:roob1128@localhost:5432/dataDB'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
