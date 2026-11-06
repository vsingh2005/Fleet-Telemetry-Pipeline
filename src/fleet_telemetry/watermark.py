"""
Bounded out-of-orderness watermark generator for event-time stream processing.
"""
from typing import Tuple

class BoundedWatermarkGenerator:
    def __init__(self, max_out_of_orderness_seconds: float = 5.0):
        self.delay = max_out_of_orderness_seconds
        self.max_timestamp = float("-inf")

    def on_event(self, event_timestamp: float) -> Tuple[float, bool]:
        watermark = self.max_timestamp - self.delay
        is_late = event_timestamp < watermark

        if event_timestamp > self.max_timestamp:
            self.max_timestamp = event_timestamp
            watermark = self.max_timestamp - self.delay

        return watermark, is_late
