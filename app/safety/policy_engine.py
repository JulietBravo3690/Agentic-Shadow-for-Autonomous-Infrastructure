from dataclasses import dataclass
from app.models.action import ActionProposal
from app.safety.permissions import AUTO_APPROVABLE_RISKS


@dataclass(frozen=True)
class PolicyDecision:
    auto_approved: bool
    reason: str


class PolicyEngine:
    def evaluate(self, action: ActionProposal) -> PolicyDecision:
        allowed = action.risk in AUTO_APPROVABLE_RISKS
        return PolicyDecision(allowed, "Low-risk simulated action" if allowed else f"{action.risk} action requires explicit human approval")
