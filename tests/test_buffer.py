from fleet_telemetry.buffer import CircularBuffer

def test_circular_buffer_capacity_eviction():
    buf = CircularBuffer(capacity=3)
    buf.push(1)
    buf.push(2)
    buf.push(3)
    assert len(buf) == 3
    buf.push(4)
    assert len(buf) == 3
    assert buf.pop_all() == [2, 3, 4]
    assert len(buf) == 0
    assert buf.is_empty()
