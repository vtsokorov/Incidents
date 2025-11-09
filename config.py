import os
from dotenv import load_dotenv
from app.schemas.components import swagger_components


load_dotenv()


class Config:
    DEBUG = os.getenv('DEBUG', True)
    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SWAGGER = {
        'title': 'API для UCAR<>TOPDOER',
        'openapi': '3.0.3',
        'termsOfService': '',
        'description': '',
        'uiversion': 3,
        'specs_route': '/swagger/',
        'headers': [],
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/apispec.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True,
            }
        ],
        **swagger_components  # Добавляем компоненты Swagger
    }