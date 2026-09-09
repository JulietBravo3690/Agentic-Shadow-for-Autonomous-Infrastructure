from app.models.action import ActionProposal,RiskLevel
from app.safety.policy_engine import PolicyEngine
def proposal(risk): return ActionProposal(action_type="test",risk=risk,rationale="test")
def test_low_risk_is_auto_approved(): assert PolicyEngine().evaluate(proposal(RiskLevel.LOW)).auto_approved
def test_high_risk_needs_human(): assert not PolicyEngine().evaluate(proposal(RiskLevel.HIGH)).auto_approved
def test_human_approval_executes(client):
 from simulator.telemetry_generator import TelemetryGenerator
 from app.models.telemetry import AssetType
 data=TelemetryGenerator().generate(AssetType.TRANSFORMER,"tx","overheating").model_dump(mode="json"); incident_id=client.post("/telemetry",json=data).json()["incident_id"]
 body=client.post(f"/incidents/{incident_id}/approve",json={"actor":"operator@example.test"}).json(); assert body["status"]=="RESOLVED" and all(a["status"]=="EXECUTED" for a in body["actions"])
