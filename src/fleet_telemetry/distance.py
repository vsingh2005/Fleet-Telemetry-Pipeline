"""
Vectorized Haversine distance computations for vehicle fleet clustering.
"""
import numpy as np

EARTH_RADIUS_KM = 6371.0088

class HaversineMatrix:
    @staticmethod
    def pairwise_distance(coords: np.ndarray) -> np.ndarray:
        if len(coords) == 0:
            return np.empty((0, 0))
            
        rad = np.radians(coords)
        lat = rad[:, 0]
        lon = rad[:, 1]
        
        dlat = lat[:, None] - lat[None, :]
        dlon = lon[:, None] - lon[None, :]
        
        a = np.sin(dlat / 2.0)**2 + np.cos(lat[:, None]) * np.cos(lat[None, :]) * np.sin(dlon / 2.0)**2
        c = 2.0 * np.arcsin(np.sqrt(np.clip(a, 0.0, 1.0)))
        return c * EARTH_RADIUS_KM
