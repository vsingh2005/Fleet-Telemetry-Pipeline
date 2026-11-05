"""
Lightweight checkpoint state store with write-ahead log semantics for stream offsets.
"""
from typing import Dict, Any

class StreamStateStore:
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._wal: list = []

    def set(self, key: str, value: Any):
        self._wal.append(("SET", key, value))
        self._state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._state.get(key, default)

    def snapshot(self) -> Dict[str, Any]:
        return dict(self._state)

    def replay_wal(self, log_entries: list):
        for op, k, v in log_entries:
            if op == "SET":
                self._state[k] = v
        self._wal = list(log_entries)
