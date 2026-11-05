from fleet_telemetry.state_store import StreamStateStore

def test_stream_state_store():
    store = StreamStateStore()
    store.set("offset_veh_1", 1052)
    assert store.get("offset_veh_1") == 1052
    assert store.get("nonexistent", -1) == -1
    snap = store.snapshot()
    assert snap == {"offset_veh_1": 1052}
