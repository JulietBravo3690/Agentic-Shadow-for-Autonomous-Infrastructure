from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.models import AuditRecord


class AuditService:
    def __init__(self, db: Session): self.db = db

    def record(self, event_type: str, *, actor: str = "system", incident_id: int | None = None, metadata: dict | None = None) -> AuditRecord:
        event = AuditRecord(event_type=event_type, actor=actor, incident_id=incident_id, event_metadata=metadata or {})
        self.db.add(event)
        self.db.flush()
        return event

    def list(self) -> list[AuditRecord]:
        return list(self.db.scalars(select(AuditRecord).order_by(AuditRecord.id.desc())))
