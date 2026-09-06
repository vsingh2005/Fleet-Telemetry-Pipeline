"""
Circular Ring Buffer for high-throughput sensor telemetry ingestion.
"""
from typing import List, Optional, Generic, TypeVar
from collections import deque
import threading

T = TypeVar('T')

class CircularBuffer(Generic[T]):
    """
    Thread-safe circular ring buffer with fixed capacity and FIFO eviction.
    """
    def __init__(self, capacity: int = 10000):
        if capacity <= 0:
            raise ValueError("Capacity must be strictly positive")
        self.capacity = capacity
        self._buffer: deque = deque(maxlen=capacity)
        self._lock = threading.Lock()

    def push(self, item: T) -> None:
        """Append an item, evicting the oldest element if full."""
        with self._lock:
            self._buffer.append(item)

    def pop_all(self) -> List[T]:
        """Drains and returns all current items in FIFO order."""
        with self._lock:
            items = list(self._buffer)
            self._buffer.clear()
            return items

    def __len__(self) -> int:
        with self._lock:
            return len(self._buffer)

    def is_empty(self) -> bool:
        with self._lock:
            return len(self._buffer) == 0
