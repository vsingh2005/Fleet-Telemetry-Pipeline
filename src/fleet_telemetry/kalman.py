"""
2D constant-velocity Kalman filter for GPS trajectory smoothing and dead reckoning.
"""
import numpy as np

class GPSKalmanFilter:
    def __init__(self, process_variance: float = 1e-4, measurement_variance: float = 1e-2):
        self.state = np.zeros(4, dtype=np.float64)  # [lat, lon, v_lat, v_lon]
        self.P = np.eye(4, dtype=np.float64) * 1.0
        self.q = process_variance
        self.r = measurement_variance
        self.initialized = False

    def initialize(self, lat: float, lon: float):
        self.state = np.array([lat, lon, 0.0, 0.0], dtype=np.float64)
        self.P = np.eye(4, dtype=np.float64) * self.r
        self.initialized = True

    def predict(self, dt: float):
        if not self.initialized:
            return
        F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float64)
        Q = np.eye(4, dtype=np.float64) * (self.q * dt)
        self.state = F @ self.state
        self.P = F @ self.P @ F.T + Q

    def update(self, lat: float, lon: float):
        if not self.initialized:
            self.initialize(lat, lon)
            return float(self.state[0]), float(self.state[1])
        H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=np.float64)
        R = np.eye(2, dtype=np.float64) * self.r
        z = np.array([lat, lon], dtype=np.float64)
        y = z - (H @ self.state)
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.state = self.state + (K @ y)
        self.P = (np.eye(4) - K @ H) @ self.P
        return float(self.state[0]), float(self.state[1])
