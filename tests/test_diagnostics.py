from fleet_telemetry.diagnostics import PipelineDiagnostics

def test_pipeline_diagnostics():
    rep = PipelineDiagnostics.generate_report([12.0, 15.0, 18.0, 22.0, 45.0], 100, 98)
    assert rep["status"] == "HEALTHY"
    assert rep["packet_loss_pct"] == 2.0
    assert rep["latency_p95_ms"] > 0
