from typing import Dict, Optional, Tuple
from fleet_telemetry.models import TelemetryRecord
from fleet_telemetry.analytics import SlidingWindowStats

class AnomalyDetector:
    def __init__(self, z_threshold: float = 3.0, window_size: int = 50):
        self.z_threshold = z_threshold
        self.window_size = window_size
        self._windows: Dict[Tuple[str, str], SlidingWindowStats] = {}

    def process_record(self, record: TelemetryRecord) -> Tuple[bool, Optional[float]]:
        key = (record.device_id, record.metric_name)
        if key not in self._windows:
            self._windows[key] = SlidingWindowStats(window_size=self.window_size)

        stats = self._windows[key]
        z = stats.z_score(record.value)
        is_anomaly = False
        if z is not None and abs(z) >= self.z_threshold:
            is_anomaly = True
        stats.add(record.value)
        return is_anomaly, z
