import math
from collections import deque
from typing import Optional

class SlidingWindowStats:
    def __init__(self, window_size: int = 100):
        if window_size < 2:
            raise ValueError("Window size must be at least 2")
        self.window_size = window_size
        self.values = deque(maxlen=window_size)

    def add(self, value: float) -> None:
        self.values.append(float(value))

    @property
    def count(self) -> int:
        return len(self.values)

    @property
    def mean(self) -> Optional[float]:
        if not self.values:
            return None
        return sum(self.values) / len(self.values)

    @property
    def std_dev(self) -> Optional[float]:
        if len(self.values) < 2:
            return None
        avg = self.mean
        variance = sum((x - avg) ** 2 for x in self.values) / (len(self.values) - 1)
        return math.sqrt(variance)

    def z_score(self, value: float) -> Optional[float]:
        avg = self.mean
        std = self.std_dev
        if avg is None or std is None or std == 0.0:
            return None
        return (value - avg) / std
