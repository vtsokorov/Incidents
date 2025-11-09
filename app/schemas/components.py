swagger_components = {
    'components': {
        'schemas': {
            'Incident': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'readOnly': True},
                    'description': {'type': 'string'},
                    'status': {
                        'type': 'string',
                        'enum': ['reported', 'investigating', 'identified', 'resolving', 'resolved', 'closed', 'reopened'],
                    },
                    'source': {
                        'type': 'string',
                        'enum': ['operator', 'monitoring', 'partner']
                    },
                    'created_at': {'type': 'string', 'format': 'date-time', 'readOnly': True},
                }
            },
            'IncidentCreate': {
                'type': 'object',
                'required': ['description', 'source'],
                'properties': {
                    'description': {'type': 'string'},
                    'source': {
                        'type': 'string',
                        'example': 'operator',
                        'enum': ['operator', 'monitoring', 'partner']
                    }
                }
            },
            'IncidentUpdate': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'example': 'reported',
                        'enum': ['reported', 'investigating', 'identified', 'resolving', 'resolved', 'closed', 'reopened'],
                    }
                }
            },
            'Pagination': {
                'type': 'object',
                'properties': {
                    'page': {
                        'type': 'integer',
                        'example': 1
                    },
                    'has_next': {
                        'type': 'boolean',
                        'example': True      
                    },
                    'has_prev': {
                        'type': 'boolean',
                        'example': True 
                    },
                    'fact_length': {
                        'type': 'integer',
                        'example': 10
                    },
                    'length': {
                        'type': 'integer',
                        'example': 10
                    },
                    'total': {
                        'type': 'integer',
                        'example': 5000
                    }
                }
            }
        },
        'parameters': {
            'page': {
                'name': 'page',
                'in': 'query',
                'description': 'Текущая страница',
                'example': 1,
                'required': False,
                'schema': {
                    'type': 'integer',
                    'minimum': 1
                }
            },
            'length': {
                'name': 'length',
                'in': 'query',
                'description': 'Количество записей на странице',
                'example': 10,
                'required': False,
                'schema': {
                    'type': 'integer',
                    'minimum': 1,
                    'maximum': 500
                }
            },
            'status': {
                'name': 'status',
                'in': 'query',
                'required': False,
                'schema': {
                    'type': 'string',
                    'enum': ['reported', 'investigating', 'identified', 'resolving', 'resolved', 'closed', 'reopened']
                },
                'description': 'Фильтр по статусу'
            }
        }
    }
}
