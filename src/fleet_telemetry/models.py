"""
Core data schemas and validation models for telemetry records.
"""
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class TelemetryRecord(BaseModel):
    """
    Structured data model for an incoming sensor telemetry packet.
    """
    device_id: str = Field(..., description="Unique identifier for the edge IoT device")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="UTC timestamp of event")
    metric_name: str = Field(..., description="Telemetry metric identifier (e.g. engine_temp, bus_voltage)")
    value: float = Field(..., description="Numerical sensor observation value")
    unit: str = Field(default="raw", description="Physical unit of measurement")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary peripheral device attributes")

    def to_row(self) -> Dict[str, Any]:
        """Convert record to a flat dictionary suitable for columnar serialization."""
        return {
            "device_id": self.device_id,
            "timestamp": self.timestamp.isoformat(),
            "metric_name": self.metric_name,
            "value": float(self.value),
            "unit": self.unit,
        }
