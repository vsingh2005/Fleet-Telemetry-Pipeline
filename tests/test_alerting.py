from fleet_telemetry.models import TelemetryRecord
from fleet_telemetry.alerting import AlertEngine

def test_alert_engine_trigger_and_cooldown():
    engine = AlertEngine()
    engine.register_threshold_rule(
        rule_name="high_engine_temp",
        metric_name="coolant_temp_c",
        threshold=105.0,
        comparator=">",
        cooldown_seconds=60
    )
    rec_normal = TelemetryRecord(device_id="truck-1", metric_name="coolant_temp_c", value=90.0)
    assert engine.evaluate(rec_normal) is None

    rec_hot = TelemetryRecord(device_id="truck-1", metric_name="coolant_temp_c", value=112.0)
    alert = engine.evaluate(rec_hot)
    assert alert is not None
    assert alert.severity == "WARNING"

    alert2 = engine.evaluate(rec_hot)
    assert alert2 is None
