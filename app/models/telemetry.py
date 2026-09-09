from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class AssetType(StrEnum):
    TRANSFORMER = "transformer"
    PUMP = "pump"
    COOLING_FAN = "cooling_fan"
    GENERATOR = "generator"


class TelemetryCreate(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    asset_id: str = Field(min_length=1, max_length=100)
    asset_type: AssetType
    temperature: float = Field(ge=-50, le=300)
    voltage: float = Field(ge=0, le=100000)
    current: float = Field(ge=0, le=10000)
    vibration: float = Field(ge=0, le=100)
    status: str = Field(default="operational", max_length=50)


class TelemetryRead(TelemetryCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TelemetryIngestResponse(BaseModel):
    telemetry: TelemetryRead
    incident_id: int | None = None
    anomalies: list[str] = []
