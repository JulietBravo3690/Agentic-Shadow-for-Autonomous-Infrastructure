from app.agents.diagnostic import DiagnosticAgent
from app.agents.remediation import RemediationAgent
from app.models.action import ActionProposal
from app.models.incident import Diagnosis


class SupervisorAgent:
    def __init__(self, diagnostic: DiagnosticAgent | None = None, remediation: RemediationAgent | None = None):
        self.diagnostic = diagnostic or DiagnosticAgent()
        self.remediation = remediation or RemediationAgent()

    def investigate(self, incident: dict[str, object]) -> tuple[Diagnosis, list[ActionProposal]]:
        diagnosis = self.diagnostic.run(incident)
        return diagnosis, self.remediation.run(diagnosis)
