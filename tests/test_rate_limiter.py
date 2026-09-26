from fleet_telemetry.rate_limiter import TokenBucketLimiter

def test_token_bucket_limiter():
    limiter = TokenBucketLimiter(capacity=5.0, refill_rate=2.0)
    for _ in range(5):
        assert limiter.allow("dev-1", 1.0, now=100.0) is True
    assert limiter.allow("dev-1", 1.0, now=100.0) is False
    assert limiter.allow("dev-1", 1.0, now=101.0) is True
