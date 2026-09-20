from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional
from fleet_telemetry.models import TelemetryRecord

@dataclass
class Alert:
    rule_name: str
    device_id: str
    metric_name: str
    current_value: float
    threshold: float
    severity: str
    triggered_at: datetime

class AlertEngine:
    def __init__(self):
        self.rules: List[Dict] = []
        self._last_triggered: Dict[str, datetime] = {}

    def register_threshold_rule(self, rule_name: str, metric_name: str, threshold: float, comparator: str = ">", severity: str = "WARNING", cooldown_seconds: int = 300):
        self.rules.append({
            "name": rule_name,
            "metric": metric_name,
            "threshold": threshold,
            "comparator": comparator,
            "severity": severity,
            "cooldown": cooldown_seconds
        })

    def evaluate(self, record: TelemetryRecord) -> Optional[Alert]:
        for r in self.rules:
            if r["metric"] != record.metric_name:
                continue
            is_breached = (record.value > r["threshold"]) if r["comparator"] == ">" else (record.value < r["threshold"])
            if is_breached:
                key = f"{r['name']}:{record.device_id}"
                now = datetime.now(timezone.utc)
                last_time = self._last_triggered.get(key)
                if last_time and (now - last_time).total_seconds() < r["cooldown"]:
                    continue
                self._last_triggered[key] = now
                return Alert(
                    rule_name=r["name"],
                    device_id=record.device_id,
                    metric_name=record.metric_name,
                    current_value=record.value,
                    threshold=r["threshold"],
                    severity=r["severity"],
                    triggered_at=now
                )
        return None
