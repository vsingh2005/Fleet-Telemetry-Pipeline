from fleet_telemetry.compactor import PartitionCompactor

def test_partition_compactor():
    compactor = PartitionCompactor(batch_size_threshold=3)
    assert compactor.add_record("date=2026-09-23", {"val": 1}) is False
    assert compactor.add_record("date=2026-09-23", {"val": 2}) is False
    assert compactor.add_record("date=2026-09-23", {"val": 3}) is True

    df = compactor.drain_partition("date=2026-09-23")
    assert len(df) == 3
    assert compactor.drain_partition("date=2026-09-23").empty
