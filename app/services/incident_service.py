from sqlalchemy import select
from sqlalchemy.orm import Session
from app.agents.supervisor import SupervisorAgent
from app.database.models import ActionRecord, IncidentRecord
from app.models.action import ActionStatus
from app.models.incident import IncidentStatus, Severity
from app.safety.policy_engine import PolicyEngine
from app.services.audit_service import AuditService
from app.services.remediation_service import SimulatedActionExecutor


class IncidentService:
    def __init__(self, db: Session):
        self.db, self.audit = db, AuditService(db)
        self.executor = SimulatedActionExecutor(self.audit)

    def create_and_investigate(self, asset_id: str, severity: Severity, anomalies: list[str], evidence: dict) -> IncidentRecord:
        incident = IncidentRecord(asset_id=asset_id, severity=severity, status=IncidentStatus.INVESTIGATING, anomalies=anomalies, evidence=evidence)
        self.db.add(incident); self.db.flush()
        self.audit.record("INCIDENT_CREATED", incident_id=incident.id, metadata={"severity": severity})
        diagnosis, proposals = SupervisorAgent().investigate({"anomalies": anomalies, "evidence": evidence})
        incident.diagnosis = diagnosis.model_dump()
        self.audit.record("DIAGNOSIS_COMPLETED", incident_id=incident.id, metadata={"confidence": diagnosis.confidence})
        needs_human = False
        for proposal in proposals:
            decision = PolicyEngine().evaluate(proposal)
            action = ActionRecord(incident_id=incident.id, **proposal.model_dump(), status=ActionStatus.APPROVED if decision.auto_approved else ActionStatus.AWAITING_APPROVAL)
            self.db.add(action); self.db.flush()
            self.audit.record("REMEDIATION_PROPOSED", incident_id=incident.id, metadata={"action_id": action.id, "risk": proposal.risk})
            if decision.auto_approved:
                self.executor.execute(action)
            else:
                needs_human = True
                self.audit.record("APPROVAL_REQUESTED", incident_id=incident.id, metadata={"action_id": action.id})
        incident.status = IncidentStatus.AWAITING_APPROVAL if needs_human else IncidentStatus.RESOLVED
        self.db.commit()
        return incident

    def list(self): return list(self.db.scalars(select(IncidentRecord).order_by(IncidentRecord.id.desc())))
    def get(self, incident_id: int): return self.db.get(IncidentRecord, incident_id)

    def decide(self, incident_id: int, approved: bool, actor: str) -> IncidentRecord | None:
        incident = self.get(incident_id)
        if not incident or incident.status != IncidentStatus.AWAITING_APPROVAL: return None
        for action in incident.actions:
            if action.status == ActionStatus.AWAITING_APPROVAL:
                action.status = ActionStatus.APPROVED if approved else ActionStatus.REJECTED
                self.audit.record("ACTION_APPROVED" if approved else "ACTION_REJECTED", actor=actor, incident_id=incident.id, metadata={"action_id": action.id})
                if approved: self.executor.execute(action)
        incident.status = IncidentStatus.RESOLVED if approved else IncidentStatus.REJECTED
        self.db.commit()
        return incident
