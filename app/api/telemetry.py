from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.telemetry import TelemetryCreate, TelemetryIngestResponse, TelemetryRead
from app.services.telemetry_service import TelemetryService
router = APIRouter(prefix="/telemetry", tags=["telemetry"])

@router.post("", response_model=TelemetryIngestResponse, status_code=201)
def ingest(payload: TelemetryCreate, db: Session = Depends(get_db)):
    record, incident, result = TelemetryService(db).ingest(payload)
    return TelemetryIngestResponse(telemetry=TelemetryRead.model_validate(record), incident_id=incident.id if incident else None, anomalies=result.anomalies)

@router.get("/recent", response_model=list[TelemetryRead])
def recent(limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db)): return TelemetryService(db).recent(limit)
