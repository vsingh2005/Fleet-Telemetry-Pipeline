from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Any
from fleet_telemetry.models import TelemetryRecord

class TemporalAggregator:
    def __init__(self, bucket_seconds: int = 60):
        if bucket_seconds <= 0:
            raise ValueError("bucket_seconds must be positive")
        self.bucket_seconds = bucket_seconds

    def _get_bucket_key(self, dt: datetime) -> int:
        epoch = int(dt.replace(tzinfo=timezone.utc).timestamp()) if dt.tzinfo is None else int(dt.timestamp())
        return epoch - (epoch % self.bucket_seconds)

    def aggregate_batch(self, records: List[TelemetryRecord]) -> List[Dict[str, Any]]:
        buckets = defaultdict(list)
        for r in records:
            bkey = self._get_bucket_key(r.timestamp)
            group_key = (r.device_id, r.metric_name, bkey)
            buckets[group_key].append(r.value)

        results = []
        for (dev_id, metric, bkey), vals in sorted(buckets.items(), key=lambda x: x[0][2]):
            results.append({
                "device_id": dev_id,
                "metric_name": metric,
                "bucket_timestamp": datetime.fromtimestamp(bkey, tz=timezone.utc).isoformat(),
                "count": len(vals),
                "min": float(min(vals)),
                "max": float(max(vals)),
                "mean": float(sum(vals) / len(vals))
            })
        return results
