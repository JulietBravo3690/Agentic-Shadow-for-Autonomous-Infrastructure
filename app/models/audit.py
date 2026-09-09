from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AuditRead(BaseModel):
    id: int
    timestamp: datetime
    event_type: str
    actor: str
    incident_id: int | None
    metadata: dict[str, object]
    model_config = ConfigDict(from_attributes=True)
