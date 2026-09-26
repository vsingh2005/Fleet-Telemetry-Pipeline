"""
Per-device token bucket rate limiter for ingest throttling.
"""
import time
from typing import Dict

class TokenBucketLimiter:
    def __init__(self, capacity: float = 100.0, refill_rate: float = 20.0):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self._buckets: Dict[str, float] = {}
        self._last_time: Dict[str, float] = {}

    def allow(self, device_id: str, tokens_requested: float = 1.0, now: float = None) -> bool:
        current_time = time.monotonic() if now is None else now
        if device_id not in self._buckets:
            self._buckets[device_id] = self.capacity
            self._last_time[device_id] = current_time

        elapsed = current_time - self._last_time[device_id]
        self._last_time[device_id] = current_time
        self._buckets[device_id] = min(self.capacity, self._buckets[device_id] + elapsed * self.refill_rate)

        if self._buckets[device_id] >= tokens_requested:
            self._buckets[device_id] -= tokens_requested
            return True
        return False
