"""
Tri-state circuit breaker pattern for network sink resilience.
"""
import time

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.state = "CLOSED"
        self.last_state_change = time.monotonic()

    def allow_request(self) -> bool:
        now = time.monotonic()
        if self.state == "OPEN":
            if now - self.last_state_change >= self.recovery_time:
                self.state = "HALF-OPEN"
                self.last_state_change = now
                return True
            return False
        return True

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_state_change = time.monotonic()
