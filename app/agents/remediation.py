from app.agents.base import BaseAgent
from app.models.action import ActionProposal, RiskLevel
from app.models.incident import Diagnosis


class RemediationAgent(BaseAgent[Diagnosis, list[ActionProposal]]):
    def run(self, diagnosis: Diagnosis) -> list[ActionProposal]:
        actions = [ActionProposal(action_type="increase_monitoring", risk=RiskLevel.LOW, rationale="Collect a denser evidence window before intervention")]
        if "thermal" in diagnosis.probable_cause:
            actions.append(ActionProposal(action_type="shutdown_simulated_equipment", risk=RiskLevel.HIGH, rationale="Prevent simulated thermal damage"))
        else:
            actions.append(ActionProposal(action_type="restart_simulated_service", risk=RiskLevel.MEDIUM, rationale="Restore the simulated controller to a known state"))
        return actions
