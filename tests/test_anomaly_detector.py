from app.detection.anomaly_detector import RuleBasedAnomalyDetector
from app.models.incident import Severity
from app.models.telemetry import AssetType
from simulator.telemetry_generator import TelemetryGenerator
def test_severity_is_deterministic(): assert RuleBasedAnomalyDetector().detect(TelemetryGenerator().generate(AssetType.TRANSFORMER,"tx","overheating")).severity is Severity.CRITICAL
