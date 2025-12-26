import os
from datetime import timedelta

class Config:
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'd8b8c3f6f7418f0a72c0a19b2f3fb947f8dc3b1c4cce0f7ea9249e7a6372fa21'


    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or '3306'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'efootbool'

    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}'
        f'@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'd8b8c3f6f7418f0a72c0a19b2f3fb947f8dc3b1c4cce0f7ea9249e7a6372fa21'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
