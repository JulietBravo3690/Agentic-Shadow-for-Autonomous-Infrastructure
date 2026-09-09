from simulator.telemetry_generator import TelemetryGenerator
from app.models.telemetry import AssetType
def test_validation(client): assert client.post("/telemetry",json={}).status_code==422
def test_normal_does_not_trigger_incident(client):
 body=client.post("/telemetry",json=TelemetryGenerator().generate(AssetType.PUMP,"pump-1").model_dump(mode="json")).json(); assert body["incident_id"] is None
def test_abnormal_creates_incident_and_audit(client):
 reading=TelemetryGenerator().generate(AssetType.TRANSFORMER,"tx-1","overheating"); response=client.post("/telemetry",json=reading.model_dump(mode="json")); assert response.status_code==201
 incident=client.get(f"/incidents/{response.json()['incident_id']}").json(); assert incident["severity"]=="CRITICAL" and incident["status"]=="AWAITING_APPROVAL"
 events={x["event_type"] for x in client.get("/audit").json()}; assert {"TELEMETRY_RECEIVED","ANOMALY_DETECTED","ACTION_EXECUTED","APPROVAL_REQUESTED"}<=events
