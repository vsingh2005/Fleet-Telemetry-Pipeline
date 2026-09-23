import pytest
from fleet_telemetry.can_parser import CANFrameParser

def test_can_speed_parsing():
    payload = bytes([0x01, 0x0D, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00])
    res = CANFrameParser.parse_payload(payload)
    assert res["metric"] == "vehicle_speed"
    assert res["value"] == 85.0

def test_can_rpm_parsing():
    payload = bytes([0x01, 0x0C, 0x1F, 0x40])
    res = CANFrameParser.parse_payload(payload)
    assert res["metric"] == "engine_rpm"
    assert res["value"] == 2000.0
