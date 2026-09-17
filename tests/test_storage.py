import tempfile
from fleet_telemetry.models import TelemetryRecord
from fleet_telemetry.storage import ParquetStorageSink

def test_parquet_write_and_query():
    with tempfile.TemporaryDirectory() as tmpdir:
        sink = ParquetStorageSink(base_directory=tmpdir)
        records = [
            TelemetryRecord(device_id="car-1", metric_name="speed_kmh", value=100.0),
            TelemetryRecord(device_id="car-1", metric_name="speed_kmh", value=110.0),
            TelemetryRecord(device_id="car-2", metric_name="speed_kmh", value=85.0),
        ]
        file_path = sink.write_batch(records, partition_key="run1")
        assert file_path.exists()
        query = "SELECT device_id, AVG(value) as avg_speed FROM telemetry_view GROUP BY device_id ORDER BY device_id"
        results = sink.query_sql(query)
        assert len(results) == 2
        assert results[0]["device_id"] == "car-1"
