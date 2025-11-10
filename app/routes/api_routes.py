from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.service import IncidentService
from app.schemas.schemas import incident_schema, incidents_schema


bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/incidents', methods=['GET'])
@swag_from({
    'tags': ['Incidents'],
    'parameters': [
        {'$ref': '#/components/parameters/page'},
        {'$ref': '#/components/parameters/length'},
        {'$ref': '#/components/parameters/status'},
    ],
    'operationId': 'get_incidents',
    'summary': 'Получить список инцидентов',
    'responses': {
        200: {
            'description': 'Список инцидентов',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'incidents': {
                                'type': 'array',
                                'items': {'$ref': '#/components/schemas/Incident'}
                            },
                            'pagination': {
                                '$ref': '#/components/schemas/Pagination'
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_incidents():
    incidents, pagination, errors = IncidentService.get_page_incident(
        request.args.to_dict()
    )
    
    if errors:
        return jsonify({'errors': errors}), 400

    return jsonify(incidents_schema.dump({**pagination, 'incidents': incidents}))


@bp.route('/incident/<int:incident_id>', methods=['GET'])
@swag_from({
    'tags': ['Incidents'],
    'operationId': 'get_incident',
    'summary': 'Получить инцидент по ID',
    'parameters': [{
        'name': 'incident_id',
        'in': 'path',
        'required': True,
        'schema': {'type': 'integer'}
    }],
    'responses': {
        200: {
            'description': 'Данные о инциденте',
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/Incident'}
                }
            }
        },
        404: {'description': 'Инцидент не найден'}
    }
})
def get_incident(incident_id):
    incident = IncidentService.get_incident_by_id(incident_id)
    if not incident:
        return jsonify({'error': 'Инцидент не найден'}), 404
    
    return jsonify(incident_schema.dump(incident))


@bp.route('/incident', methods=['POST'])
@swag_from({
    'tags': ['Incidents'],
    'operationId': 'create_incident',
    'summary': 'Создать нового инцидента',
    'requestBody': {
        'required': True,
        'content': {
            'application/json': {
                'schema': {'$ref': '#/components/schemas/IncidentCreate'}
            }
        }
    },
    'responses': {
        201: {
            'description': 'Инцидент создан',
            'requestBody': {
                'content': {
                    'application/json': {
                        'schema': {'$ref': '#/components/schemas/Incident'}
                    }
                }
            },
        },
        400: {
            'description': 'Ошибка валидации'
        }
    }
})
def create_incident():
    data = request.get_json()
    inciden, errors = IncidentService.create_incident(data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    return jsonify(incident_schema.dump(inciden)), 201


@bp.route('/incident/<int:incident_id>', methods=['PATCH'])
@swag_from({
    'tags': ['Incidents'],
    'operationId': 'update_incident',
    'summary': 'Обновить статус инцидента',
    'parameters': [{
        'name': 'incident_id',
        'in': 'path',
        'required': True,
        'schema': {'type': 'integer'}
    }],
    'requestBody': {
        'content': {
            'application/json': {
                'schema': {'$ref': '#/components/schemas/IncidentUpdate'}
            }
        }
    },
    'responses': {
        200: {
            'description': 'Инцидент обновлен',
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/Incident'}
                }
            }
        },
        400: {'description': 'Ошибка валидации'},
        404: {'description': 'Инцидент не найден'}
    }
})
def update_incident(incident_id):
    data = request.get_json()
    
    user, errors = IncidentService.update_incident(incident_id, data)
    
    if errors:
        return jsonify({'errors': errors}), 400
    
    if not user:
        return jsonify({'error': 'Инцидент не найден'}), 404
    
    return jsonify(incident_schema.dump(user))