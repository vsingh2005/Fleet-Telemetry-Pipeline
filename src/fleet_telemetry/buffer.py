from collections import deque
import threading
from typing import Generic, List, TypeVar

T = TypeVar('T')

class CircularBuffer(Generic[T]):
    def __init__(self, capacity: int = 10000):
        if capacity <= 0:
            raise ValueError("Capacity must be strictly positive")
        self.capacity = capacity
        self._buffer: deque = deque(maxlen=capacity)
        self._lock = threading.Lock()

    def push(self, item: T) -> None:
        with self._lock:
            self._buffer.append(item)

    def pop_all(self) -> List[T]:
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
