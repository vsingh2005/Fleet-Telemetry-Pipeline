"""
Apache Arrow IPC stream serialization for telemetry record batches.
"""
import io
import pyarrow as pa
from typing import List, Dict, Any

TELEMETRY_SCHEMA = pa.schema([
    ("vehicle_id", pa.string()),
    ("timestamp", pa.float64()),
    ("speed", pa.float64()),
    ("rpm", pa.float64()),
    ("fuel_pct", pa.float64())
])

class ArrowStreamSerializer:
    @staticmethod
    def serialize_records(records: List[Dict[str, Any]]) -> bytes:
        if not records:
            table = pa.Table.from_batches([], schema=TELEMETRY_SCHEMA)
        else:
            pydict = {
                "vehicle_id": [r["vehicle_id"] for r in records],
                "timestamp": [float(r["timestamp"]) for r in records],
                "speed": [float(r.get("speed", 0.0)) for r in records],
                "rpm": [float(r.get("rpm", 0.0)) for r in records],
                "fuel_pct": [float(r.get("fuel_pct", 0.0)) for r in records],
            }
            table = pa.Table.from_pydict(pydict, schema=TELEMETRY_SCHEMA)
            
        sink = io.BytesIO()
        with pa.ipc.new_stream(sink, TELEMETRY_SCHEMA) as writer:
            writer.write_table(table)
        return sink.getvalue()

    @staticmethod
    def deserialize_records(stream_bytes: bytes) -> pa.Table:
        reader = pa.ipc.open_stream(stream_bytes)
        return reader.read_all()
