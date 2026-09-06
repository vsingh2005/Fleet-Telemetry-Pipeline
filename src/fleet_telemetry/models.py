from datetime import datetime, timezone
from pydantic import BaseModel, Field

class TelemetryRecord(BaseModel):
    device_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metric_name: str
    value: float
    unit: str = "raw"
    metadata: dict = Field(default_factory=dict)

    def to_row(self) -> dict:
        return {
            "device_id": self.device_id,
            "timestamp": self.timestamp.isoformat(),
            "metric_name": self.metric_name,
            "value": float(self.value),
            "unit": self.unit,
        }
