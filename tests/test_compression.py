import pytest
from fleet_telemetry.compression import StreamCompressor

def test_stream_compression_roundtrip():
    data = b"vehicle_id=V101;speed=85.4;engine_temp=92.1;ts=1720000000\n" * 50
    compressed = StreamCompressor.compress_batch(data)
    assert len(compressed) < len(data)
    decompressed, valid = StreamCompressor.decompress_batch(compressed)
    assert valid is True
    assert decompressed == data
