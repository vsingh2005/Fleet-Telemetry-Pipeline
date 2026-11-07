from fleet_telemetry.circuit_breaker import CircuitBreaker

def test_circuit_breaker():
    cb = CircuitBreaker(failure_threshold=2, recovery_time=0.1)
    assert cb.allow_request() is True
    cb.record_failure()
    assert cb.allow_request() is True
    cb.record_failure()
    assert cb.state == "OPEN"
    assert cb.allow_request() is False
