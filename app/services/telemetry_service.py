from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.models import TelemetryRecord
from app.detection.anomaly_detector import RuleBasedAnomalyDetector
from app.models.telemetry import TelemetryCreate
from app.services.audit_service import AuditService
from app.services.incident_service import IncidentService


class TelemetryService:
    def __init__(self, db: Session): self.db = db

    def ingest(self, reading: TelemetryCreate):
        record = TelemetryRecord(
            timestamp=reading.timestamp,
            asset_id=reading.asset_id,
            asset_type=reading.asset_type.value,
            temperature=reading.temperature,
            voltage=reading.voltage,
            current=reading.current,
            vibration=reading.vibration,
            status=reading.status,
        )
        self.db.add(record); self.db.flush()
        audit = AuditService(self.db)
        audit.record("TELEMETRY_RECEIVED", metadata={"telemetry_id": record.id, "asset_id": record.asset_id})
        result = RuleBasedAnomalyDetector().detect(reading)
        incident = None
        if result.anomalies:
            audit.record("ANOMALY_DETECTED", metadata={"telemetry_id": record.id, "anomalies": result.anomalies})
            incident = IncidentService(self.db).create_and_investigate(record.asset_id, result.severity, result.anomalies, reading.model_dump(mode="json"))
        else: self.db.commit()
        return record, incident, result

    def recent(self, limit: int = 50):
        return list(self.db.scalars(select(TelemetryRecord).order_by(TelemetryRecord.timestamp.desc()).limit(limit)))
