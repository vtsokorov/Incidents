from app.extensions import ma, db
from marshmallow import validate, ValidationError, EXCLUDE, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.models import Incident, IncidentSource, IncidentStatus


class IncidentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incident
        sqla_session = db.session
        include_fk = True
        load_instance = True
        unknown = EXCLUDE 
        datetimeformat = 'iso'
    
    id = ma.Int(dump_only=True)
    
    description = ma.Str(
        required=True, validate=validate.Length(min=1, max=1000)
    )
    status = ma.Method("get_status_value", deserialize="load_status")
    source = ma.Method("get_source_value", deserialize="load_source")
    
    created_at = ma.DateTime(dump_only=True)
    
    def get_status_value(self, obj):
        if isinstance(obj.status, IncidentStatus):
            return obj.status.value
        
        return obj.status
    
    def get_source_value(self, obj):
        if isinstance(obj.source, IncidentSource):
            return obj.source.value
        
        return obj.source
    
    def load_status(self, value):
        if isinstance(value, IncidentStatus):
            return value
        
        if isinstance(value, str):
            for status in IncidentStatus:
                if status.value.lower() == value.lower():
                    return status
        
        raise ValidationError(f"Invalid status: {value}")
    
    def load_source(self, value):
        if isinstance(value, IncidentSource):
            return value
        
        if isinstance(value, str):
            for source in IncidentSource:
                if source.value.lower() == value.lower():
                    return source
        
        raise ValidationError(f"Invalid source: {value}")
    
    
class PaginationSchema(ma.Schema):
    total = ma.Integer()
    page = ma.Integer()
    length = ma.Integer()
    has_next = ma.Boolean()
    has_prev = ma.Boolean()
    fact_length = ma.Integer()
    
    
class IncidentPaginationSchema(ma.Schema):
    pagination = ma.Nested(lambda: PaginationSchema())
    incidents = ma.List(ma.Nested(lambda: IncidentSchema()))
    
    
class ParamsSchema(ma.Schema):
    status = ma.Str(validate=validate.OneOf([status.value for status in IncidentStatus]))
    page = ma.Int(validate=validate.Range(min=1), load_default=1)
    length = ma.Int(validate=validate.Range(min=1, max=100), load_default=10)
    
    @post_load
    def uppercase_fields(self, data, **kwargs):
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = data['status'].upper()
            
        return data
    

incident_schema = IncidentSchema()
incidents_schema = IncidentPaginationSchema()
incident_create_schema = IncidentSchema(only=['description', 'source'])
incident_update_schema = IncidentSchema(only=['status'], partial=True)
params_schema = ParamsSchema()
