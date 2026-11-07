from fleet_telemetry.tracing import TraceContext

def test_tracecontext_generation():
    tp = TraceContext.generate_traceparent(sampled=True)
    assert tp.startswith("00-")
    parsed = TraceContext.parse_traceparent(tp)
    assert parsed["valid"] is True
    assert parsed["sampled"] is True
