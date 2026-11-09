"""
Diagnostic reporter summarizing ingestion health, packet loss, and latency percentiles.
"""
from typing import List, Dict, Any
import numpy as np

class PipelineDiagnostics:
    @staticmethod
    def generate_report(latencies_ms: List[float], packets_expected: int, packets_received: int) -> Dict[str, Any]:
        loss_pct = 0.0
        if packets_expected > 0:
            loss_pct = max(0.0, (packets_expected - packets_received) / packets_expected * 100.0)

        arr = np.array(latencies_ms) if latencies_ms else np.array([0.0])
        p50 = float(np.percentile(arr, 50))
        p95 = float(np.percentile(arr, 95))
        p99 = float(np.percentile(arr, 99))

        status = "HEALTHY"
        if loss_pct > 5.0 or p95 > 250.0:
            status = "DEGRADED"
        if loss_pct > 20.0 or p95 > 1000.0:
            status = "CRITICAL"

        return {
            "status": status,
            "packets_expected": packets_expected,
            "packets_received": packets_received,
            "packet_loss_pct": round(loss_pct, 2),
            "latency_p50_ms": round(p50, 2),
            "latency_p95_ms": round(p95, 2),
            "latency_p99_ms": round(p99, 2)
        }
