"""Run the complete workflow locally without an API key or PostgreSQL."""
import os
os.environ.setdefault("DATABASE_URL","sqlite:///./demo.db")
from fastapi.testclient import TestClient
from app.main import app
from app.models.telemetry import AssetType
from simulator.telemetry_generator import TelemetryGenerator
def main():
 with TestClient(app) as client:
  gen=TelemetryGenerator(); healthy=gen.generate(AssetType.TRANSFORMER,"transformer-demo")
  print("1. Healthy telemetry:",client.post("/telemetry",json=healthy.model_dump(mode="json")).json())
  hot=gen.generate(AssetType.TRANSFORMER,"transformer-demo","overheating"); result=client.post("/telemetry",json=hot.model_dump(mode="json")).json(); print("2. Injected anomaly:",result)
  incident=client.get(f"/incidents/{result['incident_id']}").json(); print("3. Agent investigation and policy decision:",incident)
  if incident["status"]=="AWAITING_APPROVAL": print("4. Human-approved simulated execution:",client.post(f"/incidents/{incident['id']}/approve",json={"actor":"demo-human"}).json()["status"])
  print("5. Audit trail:")
  for event in reversed(client.get("/audit").json()): print(f"   {event['event_type']}: {event['metadata']}")
if __name__=="__main__": main()
