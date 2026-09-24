import pytest
from fleet_telemetry.kalman import GPSKalmanFilter

def test_kalman_filter_smoothing():
    kf = GPSKalmanFilter(process_variance=1e-4, measurement_variance=1e-2)
    kf.initialize(42.3601, -71.0589)
    for _ in range(5):
        kf.predict(dt=1.0)
        smoothed_lat, smoothed_lon = kf.update(42.3602, -71.0590)
    assert abs(smoothed_lat - 42.3602) < 0.001
    assert abs(smoothed_lon - (-71.0590)) < 0.001
