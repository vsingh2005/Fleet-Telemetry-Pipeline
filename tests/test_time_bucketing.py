import pandas as pd
from fleet_telemetry.time_bucketing import DuckDBTimeBucketEngine

def test_time_bucketing():
    engine = DuckDBTimeBucketEngine()
    df = pd.DataFrame({
        "vehicle_id": ["v1", "v1", "v2"],
        "ts": pd.to_datetime(["2026-09-23 10:01:00", "2026-09-23 10:02:00", "2026-09-23 10:03:00"]),
        "speed": [50.0, 60.0, 70.0],
        "rpm": [2000.0, 2200.0, 2500.0]
    })
    engine.insert_records(df)
    res = engine.query_bucketed_stats("5 minute")
    assert len(res) == 2
