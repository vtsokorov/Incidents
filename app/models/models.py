from app.extensions import db
from datetime import datetime
from enum import Enum


class IncidentStatus(Enum):
    """Перечисление статусов инцидента"""
    
    REPORTED = "reported"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified" 
    RESOLVING = "resolving"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REOPENED = "reopened"


class IncidentSource(Enum):
    """Перечисление источников инцидента"""
    
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"


class Incident(db.Model):
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(IncidentStatus), default=IncidentStatus.REPORTED, nullable=False)
    source = db.Column(db.Enum(IncidentSource), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        db.Index('idx_incident_status', 'status'),
        db.Index('idx_incident_created_at', 'created_at'),  
        db.Index('idx_incident_source', 'source'),           
        db.Index('idx_status_created', 'status', 'created_at')
    )

    def __repr__(self):
        return f'<Incident {self.id}>'