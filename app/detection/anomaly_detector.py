from dataclasses import dataclass
from app.models.incident import Severity
from app.models.telemetry import AssetType, TelemetryCreate


@dataclass(frozen=True)
class Thresholds:
    max_temperature: float
    min_voltage: float
    max_voltage: float
    max_current: float
    max_vibration: float


DEFAULT_THRESHOLDS = {
    AssetType.TRANSFORMER: Thresholds(95, 210, 250, 120, 4),
    AssetType.PUMP: Thresholds(85, 210, 250, 80, 8),
    AssetType.COOLING_FAN: Thresholds(75, 210, 250, 25, 10),
    AssetType.GENERATOR: Thresholds(105, 380, 440, 180, 7),
}


@dataclass(frozen=True)
class DetectionResult:
    anomalies: list[str]
    severity: Severity | None


class RuleBasedAnomalyDetector:
    """Replaceable detector implementing explicit, inspectable safety rules."""

    def __init__(self, thresholds=DEFAULT_THRESHOLDS):
        self.thresholds = thresholds

    def detect(self, reading: TelemetryCreate) -> DetectionResult:
        t = self.thresholds[reading.asset_type]
        anomalies: list[str] = []
        scores: list[int] = []
        if reading.temperature > t.max_temperature:
            anomalies.append(f"temperature {reading.temperature} exceeds {t.max_temperature}")
            scores.append(4 if reading.temperature > t.max_temperature * 1.25 else 3)
        if not t.min_voltage <= reading.voltage <= t.max_voltage:
            anomalies.append(f"voltage {reading.voltage} outside {t.min_voltage}-{t.max_voltage}")
            scores.append(3)
        if reading.current > t.max_current:
            anomalies.append(f"current {reading.current} exceeds {t.max_current}")
            scores.append(3)
        if reading.vibration > t.max_vibration:
            anomalies.append(f"vibration {reading.vibration} exceeds {t.max_vibration}")
            scores.append(2)
        severity = {1: Severity.LOW, 2: Severity.MEDIUM, 3: Severity.HIGH, 4: Severity.CRITICAL}.get(max(scores, default=0))
        return DetectionResult(anomalies, severity)
