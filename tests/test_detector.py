from fleet_telemetry.models import TelemetryRecord
from fleet_telemetry.detector import AnomalyDetector

def test_anomaly_detection_trigger():
    detector = AnomalyDetector(z_threshold=2.5, window_size=20)
    for _ in range(15):
        detector.process_record(TelemetryRecord(device_id="dev1", metric_name="temp", value=20.0))
        detector.process_record(TelemetryRecord(device_id="dev1", metric_name="temp", value=21.0))
    spike = TelemetryRecord(device_id="dev1", metric_name="temp", value=95.0)
    is_anomaly, z = detector.process_record(spike)
    assert is_anomaly is True and z is not None and z > 2.5
