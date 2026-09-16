from fleet_telemetry.analytics import SlidingWindowStats

def test_sliding_window_mean_and_std():
    stats = SlidingWindowStats(window_size=5)
    for val in [10.0, 10.0, 10.0, 10.0, 10.0]:
        stats.add(val)
    assert stats.mean == 10.0
    assert stats.std_dev == 0.0

def test_sliding_window_z_score():
    stats = SlidingWindowStats(window_size=10)
    for val in [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]:
        stats.add(val)
    z = stats.z_score(15.0)
    assert z is not None and z > 2.0
