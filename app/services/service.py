from typing import Tuple, Optional, List
from app.extensions import db
from app.models.models import Incident
from app.schemas.schemas import incident_create_schema, \
    incident_update_schema, params_schema


class IncidentService:
    @staticmethod
    def get_page_incident(params) -> Tuple[List[Incident], dict, dict]:
        errors = params_schema.validate(params)

        if errors:
            return [], {}, errors

        query_params = params_schema.load(params)
        query = db.session.query(
            Incident
        )

        if query_params.get('status'):
            query = query.filter(
                Incident.status == query_params.get('status')
            )
               
        query = query.order_by(
            Incident.id.desc()
        )
        
        current_page = query_params.get('page')
        page_length = query_params.get('length')
        
        incidents = query.paginate(
            page=current_page, per_page=page_length, error_out=False
        )
        
        pagination = {
            'pagination': {
                'total': incidents.total,
                'has_next': incidents.has_next,
                'has_prev': incidents.has_prev,
                'page': incidents.page,
                'length': page_length,
                'fact_length': len(incidents.items)
            }
        }

        return incidents.items, pagination, {}
    
    @staticmethod
    def get_incident_by_id(incident_id: int) -> Optional[Incident]:
        return Incident.query.filter_by(id=incident_id).first()
    
    @staticmethod
    def create_incident(incident_data: dict) -> Tuple[Optional[Incident], dict]:
        errors = incident_create_schema.validate(incident_data)

        if errors:
            return None, errors
        
        try:
            incident = incident_create_schema.load(
                incident_data
            )
            db.session.add(incident)
            db.session.commit()
            return incident, {}
        except Exception as e:
            db.session.rollback()
            return None, {'database': [str(e)]}
    
    @staticmethod
    def update_incident(incident_id: int, update_data: dict) -> Tuple[Optional[Incident], dict]:
        incident = IncidentService.get_incident_by_id(incident_id)
        
        if not incident:
            return None, {'error': 'Инцидент не найден'}
        
        errors = incident_update_schema.validate(update_data)
        if errors:
            return None, errors
        
        try:
            incident = incident_update_schema.load(
                update_data, 
                instance=incident,
                partial=True        
            )
            
            db.session.commit()
            
            return incident, {}
        except Exception as e:
            db.session.rollback()
            return None, {'database': [str(e)]}