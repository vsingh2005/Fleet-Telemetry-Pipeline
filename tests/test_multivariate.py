import numpy as np
from fleet_telemetry.multivariate import MahalanobisDetector

def test_mahalanobis_outlier_detection():
    rng = np.random.RandomState(42)
    normal_data = rng.randn(100, 3)
    det = MahalanobisDetector(threshold=3.5)
    det.fit(normal_data)

    normal_pt = np.array([0.1, -0.2, 0.05])
    assert det.is_anomaly(normal_pt) is False

    extreme_pt = np.array([10.0, -12.0, 15.0])
    assert det.is_anomaly(extreme_pt) is True
