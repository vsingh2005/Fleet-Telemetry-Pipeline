"""
W3C TraceContext distributed traceparent parser and generator.
"""
import secrets

class TraceContext:
    @staticmethod
    def generate_traceparent(sampled: bool = True) -> str:
        trace_id = secrets.token_hex(16)
        span_id = secrets.token_hex(8)
        flags = "01" if sampled else "00"
        return f"00-{trace_id}-{span_id}-{flags}"

    @staticmethod
    def parse_traceparent(header: str) -> dict:
        parts = header.strip().split("-")
        if len(parts) != 4 or parts[0] != "00":
            return {"valid": False}
        return {
            "valid": True,
            "version": parts[0],
            "trace_id": parts[1],
            "parent_id": parts[2],
            "sampled": parts[3] == "01"
        }
