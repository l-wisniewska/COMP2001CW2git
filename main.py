from flask import Flask
from flasgger import Swagger
from app.routes import app_routes  # Import the routes blueprint
from extensions import db  # Assuming you have a db extension

def create_app():
    app = Flask(__name__)

    # Configure your app (e.g., secret key, database URI, etc.)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://LWisniewska:ZofM708*@dist-6-505.uopnet.plymouth.ac.uk/COMP2001_LWisniewska?driver=ODBC+Driver+17+for+SQL+Server'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secretKEY'  # Set a secret key for JWT

    # Initialize your database
    db.init_app(app)

    # Set up Swagger UI (assuming you have the swagger.json file)
    Swagger(app, template_file='static/swagger.json')

    # Register the blueprint with a prefix (e.g., '/api')
    app.register_blueprint(app_routes, url_prefix='/api')

    # Swagger configuration
    app.config['SWAGGER'] = {
        'title': 'Trail API',
        'uiversion': 3,
        'openapi': '3.0.0',
        'specs': [
            {
                'endpoint': 'api_docs',
                'route': '/api/docs.json',
                'rule_filter': lambda rule: True,  # All endpoints included
                'model_filter': lambda tag: True,  # All models included
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/apidocs',  # Swagger UI route
    }

    Swagger(app)
    
    return app