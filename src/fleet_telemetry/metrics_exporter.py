"""
Prometheus OpenMetrics text format exporter for edge telemetry ingestion metrics.
"""
from typing import Dict

class MetricsExporter:
    def __init__(self):
        self._counters: Dict[str, float] = {}
        self._gauges: Dict[str, float] = {}

    def inc_counter(self, name: str, value: float = 1.0):
        self._counters[name] = self._counters.get(name, 0.0) + value

    def set_gauge(self, name: str, value: float):
        self._gauges[name] = value

    def export_text(self) -> str:
        lines = []
        for name, val in sorted(self._counters.items()):
            lines.append(f"# TYPE {name} counter")
            lines.append(f"{name} {val}")
        for name, val in sorted(self._gauges.items()):
            lines.append(f"# TYPE {name} gauge")
            lines.append(f"{name} {val}")
        return "\n".join(lines) + "\n"
