from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.incident import IncidentRead
from app.services.incident_service import IncidentService
router = APIRouter(prefix="/incidents", tags=["incidents"])

class DecisionRequest(BaseModel): actor: str = Field(min_length=1, max_length=100)

@router.get("", response_model=list[IncidentRead])
def list_incidents(db: Session = Depends(get_db)): return IncidentService(db).list()

@router.get("/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    item = IncidentService(db).get(incident_id)
    if not item: raise HTTPException(404, "Incident not found")
    return item

def decide(incident_id: int, payload: DecisionRequest, approved: bool, db: Session):
    item = IncidentService(db).decide(incident_id, approved, payload.actor)
    if not item: raise HTTPException(409, "Incident is missing or not awaiting approval")
    return item

@router.post("/{incident_id}/approve", response_model=IncidentRead)
def approve(incident_id: int, payload: DecisionRequest, db: Session = Depends(get_db)): return decide(incident_id, payload, True, db)

@router.post("/{incident_id}/reject", response_model=IncidentRead)
def reject(incident_id: int, payload: DecisionRequest, db: Session = Depends(get_db)): return decide(incident_id, payload, False, db)
