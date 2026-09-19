import math
from typing import List, Tuple

class GeofenceValidator:
    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlam = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2.0)**2
        return 2.0 * R * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    @staticmethod
    def is_inside_circle(lat: float, lon: float, center_lat: float, center_lon: float, radius_km: float) -> bool:
        dist = GeofenceValidator.haversine_distance_km(lat, lon, center_lat, center_lon)
        return dist <= radius_km

    @staticmethod
    def is_inside_polygon(lat: float, lon: float, polygon: List[Tuple[float, float]]) -> bool:
        n = len(polygon)
        if n < 3:
            return False
        inside = False
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if lat > min(p1x, p2x):
                if lat <= max(p1x, p2x):
                    if lon <= max(p1y, p2y):
                        if p1x != p2x:
                            xinters = (lat - p1x) * (p2y - p1y) / (p2x - p1x) + p1y
                        if p1y == p2y or lon <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
