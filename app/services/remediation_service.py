from app.database.models import ActionRecord
from app.models.action import ActionStatus
from app.services.audit_service import AuditService


class SimulatedActionExecutor:
    """Executes only changes to digital-twin state; never controls physical assets."""

    def __init__(self, audit: AuditService): self.audit = audit

    def execute(self, action: ActionRecord) -> None:
        action.pre_state = {"simulation_status": "operational"}
        action.post_state = {"simulation_status": "action_applied", "action": action.action_type}
        action.status = ActionStatus.EXECUTED
        self.audit.record("ACTION_EXECUTED", incident_id=action.incident_id, metadata={"action_id": action.id, "simulation": True})

    def rollback(self, action: ActionRecord) -> None:
        action.post_state = action.pre_state
        action.status = ActionStatus.ROLLED_BACK
        self.audit.record("ROLLBACK_EXECUTED", incident_id=action.incident_id, metadata={"action_id": action.id, "simulation": True})
