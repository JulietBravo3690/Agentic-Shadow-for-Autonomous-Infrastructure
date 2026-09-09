from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.audit import AuditRead
from app.services.audit_service import AuditService
router = APIRouter(tags=["audit"])

@router.get("/audit", response_model=list[AuditRead])
def audit(db: Session = Depends(get_db)):
    return [AuditRead(id=x.id, timestamp=x.timestamp, event_type=x.event_type, actor=x.actor, incident_id=x.incident_id, metadata=x.event_metadata) for x in AuditService(db).list()]
