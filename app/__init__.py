from flask import Flask, jsonify
from config import Config
from app.extensions import db, migrate, ma, swagger


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    swagger.init_app(app)
    
    register_blueprints(app)

    register_error_handlers(app)
    
    return app


def register_blueprints(app):
    from app.routes import basic_bp, api_bp
    
    app.register_blueprint(basic_bp)
    app.register_blueprint(api_bp)


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Некорректный запрос',
            'message': 'Сервер не может обработать запрос',
            'status_code': 400
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Ресурс не найден',
            'message': 'Запрашиваемый URL не существует',
            'status_code': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500