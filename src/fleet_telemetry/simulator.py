"""
Deterministic CAN bus trip drive-cycle replay simulator.
"""
import math
from typing import Generator, Dict, Any

class TripSimulator:
    @staticmethod
    def generate_trip(duration_steps: int = 100, seed_speed: float = 40.0) -> Generator[Dict[str, Any], None, None]:
        speed = seed_speed
        for step in range(duration_steps):
            delta = math.sin(step / 10.0) * 2.5
            speed = max(0.0, min(120.0, speed + delta))
            rpm = speed * 35.0 + 800.0
            temp = 85.0 + (speed / 10.0)
            yield {
                "step": step,
                "speed": round(speed, 2),
                "rpm": round(rpm, 1),
                "coolant_temp": round(temp, 1)
            }
