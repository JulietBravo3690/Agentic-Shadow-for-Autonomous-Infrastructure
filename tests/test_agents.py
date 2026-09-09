from app.agents.supervisor import SupervisorAgent
def test_structured_agent_outputs():
 diagnosis,actions=SupervisorAgent().investigate({"anomalies":["temperature 125 exceeds 95"]}); assert diagnosis.confidence>.7 and diagnosis.supporting_evidence; assert any(a.action_type=="shutdown_simulated_equipment" for a in actions)
