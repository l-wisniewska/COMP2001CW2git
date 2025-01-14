# app/__init__.py
from flask import Flask
from app.config import DevelopmentConfig
from extensions import db, jwt
from app.routes import app_routes

def create_app(config_class=DevelopmentConfig):

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register routes
    app_routes(app)

    return app

