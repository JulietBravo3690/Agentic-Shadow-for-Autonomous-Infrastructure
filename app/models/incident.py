from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, ConfigDict
from app.models.action import ActionRead


class Severity(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class IncidentStatus(StrEnum):
    INVESTIGATING = "INVESTIGATING"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"


class Diagnosis(BaseModel):
    probable_cause: str
    confidence: float
    supporting_evidence: list[str]


class IncidentRead(BaseModel):
    id: int
    created_at: datetime
    asset_id: str
    severity: Severity
    status: IncidentStatus
    anomalies: list[str]
    evidence: dict[str, object]
    diagnosis: dict[str, object] | None
    actions: list[ActionRead] = []
    model_config = ConfigDict(from_attributes=True)
