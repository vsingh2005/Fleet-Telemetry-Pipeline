from fleet_telemetry.speed_compliance import SpeedComplianceMonitor

def test_speed_compliance_evaluation():
    monitor = SpeedComplianceMonitor(hysteresis_kmh=2.0)
    res_ok = monitor.evaluate("Depot", 28.0, 30.0)
    assert res_ok["violation"] is False

    res_viol = monitor.evaluate("School_Zone", 52.0, 30.0)
    assert res_viol["violation"] is True
    assert res_viol["severity"] == "moderate"
