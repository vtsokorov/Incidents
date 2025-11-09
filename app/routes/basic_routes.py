from flask import Blueprint, jsonify, request, render_template_string
from datetime import datetime
from app.extensions import db
from sqlalchemy import text


bp = Blueprint('basic', __name__)


@bp.route('/')
def index():
    return jsonify({
        'message': 'Добро пожаловать в Flask API!',
        'version': '1.0.0',
        'endpoints': {
            'documentation': '/swagger',
            'api_base': '/api/v1',
            'health': '/health'
        }
    })


@bp.route('/health')
def health_check():
    try:
        db.session.execute(text('SELECT 1'))
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'version': '1.0.0'
    })


@bp.route('/info')
def info():
    import platform
    return jsonify({
        'flask_version': '3.1.2',
        'python_version': platform.python_version(),
        'environment': 'development'
    })