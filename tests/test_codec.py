from fleet_telemetry.codec import DeltaEncoder

def test_delta_encode_decode_roundtrip():
    ts = [1000, 1010, 1020, 1030, 1045, 1060, 1075]
    encoded = DeltaEncoder.encode(ts)
    decoded = DeltaEncoder.decode(encoded)
    assert decoded == ts
