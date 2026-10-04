"""
Speed compliance monitor checking vehicle speeds against zone limits.
"""
from typing import Dict, Any

class SpeedComplianceMonitor:
    def __init__(self, hysteresis_kmh: float = 3.0):
        self.hysteresis = hysteresis_kmh

    def evaluate(self, zone_name: str, speed_kmh: float, speed_limit_kmh: float) -> Dict[str, Any]:
        delta = speed_kmh - speed_limit_kmh
        is_violation = delta > self.hysteresis
        severity = "none"
        if delta > 25.0:
            severity = "critical"
        elif delta > 10.0:
            severity = "moderate"
        elif delta > self.hysteresis:
            severity = "minor"

        return {
            "zone": zone_name,
            "speed": speed_kmh,
            "limit": speed_limit_kmh,
            "excess": max(0.0, round(delta, 1)),
            "violation": is_violation,
            "severity": severity
        }
