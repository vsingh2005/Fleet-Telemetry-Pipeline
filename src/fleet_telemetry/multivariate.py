"""
Multivariate outlier detection via Mahalanobis distance.
"""
import numpy as np

class MahalanobisDetector:
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.mean = None
        self.inv_cov = None

    def fit(self, baseline_data: np.ndarray):
        self.mean = np.mean(baseline_data, axis=0)
        cov = np.cov(baseline_data, rowvar=False)
        cov += np.eye(cov.shape[0]) * 1e-6
        self.inv_cov = np.linalg.inv(cov)

    def score(self, point: np.ndarray) -> float:
        if self.mean is None or self.inv_cov is None:
            raise ValueError("Detector must be fitted first")
        diff = point - self.mean
        dist = np.sqrt(np.dot(np.dot(diff, self.inv_cov), diff.T))
        return float(dist)

    def is_anomaly(self, point: np.ndarray) -> bool:
        return self.score(point) > self.threshold
