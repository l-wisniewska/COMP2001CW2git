import os
from datetime import timedelta

class Config:
    """Base config class."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secretKey')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development config."""
    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://LWisniewska:ZofM708*@dist-6-505.uopnet.plymouth.ac.uk/COMP2001_LWisniewska?driver=ODBC+Driver+17+for+SQL+Server'
    )
    DEBUG = True


class ProductionConfig(Config):
    """Production config."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///production.db')  
    DEBUG = False





