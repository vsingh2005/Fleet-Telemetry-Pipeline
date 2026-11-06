from fleet_telemetry.metrics_exporter import MetricsExporter

def test_metrics_exporter():
    exporter = MetricsExporter()
    exporter.inc_counter("fleet_packets_ingested_total", 42)
    exporter.set_gauge("fleet_active_connections", 5)
    out = exporter.export_text()
    assert "fleet_packets_ingested_total 42.0" in out
    assert "fleet_active_connections 5" in out
