from app.models.action import RiskLevel

AUTO_APPROVABLE_RISKS = frozenset({RiskLevel.LOW})
HUMAN_APPROVAL_RISKS = frozenset({RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL})
