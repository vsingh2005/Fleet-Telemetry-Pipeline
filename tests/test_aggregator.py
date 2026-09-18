from datetime import datetime, timezone
from fleet_telemetry.models import TelemetryRecord
from fleet_telemetry.aggregator import TemporalAggregator

def test_temporal_aggregator_bucketing():
    agg = TemporalAggregator(bucket_seconds=60)
    t0 = datetime(2026, 1, 1, 12, 0, 10, tzinfo=timezone.utc)
    t1 = datetime(2026, 1, 1, 12, 0, 50, tzinfo=timezone.utc)
    t2 = datetime(2026, 1, 1, 12, 1, 15, tzinfo=timezone.utc)
    records = [
        TelemetryRecord(device_id="v1", metric_name="speed", value=50.0, timestamp=t0),
        TelemetryRecord(device_id="v1", metric_name="speed", value=70.0, timestamp=t1),
        TelemetryRecord(device_id="v1", metric_name="speed", value=80.0, timestamp=t2),
    ]
    summary = agg.aggregate_batch(records)
    assert len(summary) == 2
    assert summary[0]["count"] == 2
    assert summary[0]["mean"] == 60.0
    assert summary[1]["count"] == 1
    assert summary[1]["mean"] == 80.0
