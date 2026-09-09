from app.agents.base import BaseAgent
from app.models.incident import Diagnosis


class DiagnosticAgent(BaseAgent[dict[str, object], Diagnosis]):
    def run(self, incident: dict[str, object]) -> Diagnosis:
        anomalies = [str(item) for item in incident["anomalies"]]  # type: ignore[index]
        cause = "thermal management failure" if any("temperature" in a for a in anomalies) else "operating parameter outside safe envelope"
        return Diagnosis(probable_cause=cause, confidence=min(0.95, 0.72 + 0.06 * len(anomalies)), supporting_evidence=anomalies)
