from enum import StrEnum
from pydantic import BaseModel, ConfigDict


class RiskLevel(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ActionStatus(StrEnum):
    PROPOSED = "PROPOSED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    EXECUTED = "EXECUTED"
    ROLLED_BACK = "ROLLED_BACK"


class ActionProposal(BaseModel):
    action_type: str
    risk: RiskLevel
    rationale: str
    parameters: dict[str, object] = {}


class ActionRead(ActionProposal):
    id: int
    incident_id: int
    status: ActionStatus
    pre_state: dict[str, object] | None = None
    post_state: dict[str, object] | None = None
    model_config = ConfigDict(from_attributes=True)
