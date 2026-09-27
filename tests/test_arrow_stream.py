from fleet_telemetry.arrow_stream import ArrowStreamSerializer

def test_arrow_ipc_serialization():
    data = [
        {"vehicle_id": "truck-01", "timestamp": 1720000001.0, "speed": 62.5, "rpm": 1850.0, "fuel_pct": 74.0},
        {"vehicle_id": "truck-02", "timestamp": 1720000002.0, "speed": 45.0, "rpm": 1400.0, "fuel_pct": 52.3},
    ]
    raw_ipc = ArrowStreamSerializer.serialize_records(data)
    assert len(raw_ipc) > 0
    table = ArrowStreamSerializer.deserialize_records(raw_ipc)
    assert table.num_rows == 2
    assert table.column("vehicle_id").to_pylist() == ["truck-01", "truck-02"]
