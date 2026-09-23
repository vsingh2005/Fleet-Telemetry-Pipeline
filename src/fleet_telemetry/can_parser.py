"""
CAN-bus and OBD-II standard PID frame parser.
"""
from typing import Dict, Any, Optional

PID_DEFINITIONS = {
    0x0C: ("engine_rpm", lambda data: ((data[0] * 256) + data[1]) / 4.0),
    0x0D: ("vehicle_speed", lambda data: float(data[0])),
    0x05: ("coolant_temp", lambda data: float(data[0] - 40)),
    0x11: ("throttle_position", lambda data: (data[0] * 100.0) / 255.0),
    0x2F: ("fuel_level", lambda data: (data[0] * 100.0) / 255.0),
}

class CANFrameParser:
    """Parses raw 8-byte CAN payload frames into telemetry fields."""
    
    @staticmethod
    def parse_payload(payload_bytes: bytes) -> Dict[str, Any]:
        if len(payload_bytes) < 3:
            return {}
        
        mode = payload_bytes[0]
        pid = payload_bytes[1]
        data = payload_bytes[2:]
        
        if mode != 0x01:
            return {"mode": mode, "unsupported": True}
            
        if pid in PID_DEFINITIONS:
            name, formula = PID_DEFINITIONS[pid]
            try:
                val = formula(data)
                return {"pid": hex(pid), "metric": name, "value": round(val, 2)}
            except (IndexError, ZeroDivisionError):
                return {"error": "malformed_frame"}
                
        return {"pid": hex(pid), "raw_bytes": data.hex()}
