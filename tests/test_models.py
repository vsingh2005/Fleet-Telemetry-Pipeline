"""
Unit tests for telemetry data models.
"""
from datetime import datetime, timezone
from fleet_telemetry.models import TelemetryRecord

def test_telemetry_record_creation():
    record = TelemetryRecord(
        device_id="edge-node-01",
        metric_name="battery_voltage",
        value=12.6,
        unit="V"
    )
    assert record.device_id == "edge-node-01"
    assert record.metric_name == "battery_voltage"
    assert record.value == 12.6
    assert record.unit == "V"
    assert isinstance(record.timestamp, datetime)

def test_telemetry_to_row():
    record = TelemetryRecord(
        device_id="sensor-42",
        metric_name="core_temperature",
        value=68.5,
        unit="C"
    )
    row = record.to_row()
    assert row["device_id"] == "sensor-42"
    assert row["value"] == 68.5
    assert "timestamp" in row
