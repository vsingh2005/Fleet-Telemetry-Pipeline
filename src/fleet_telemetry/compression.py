"""
Telemetry batch compression wrapper with chunk headers and checksum validation.
"""
import zlib
import struct
from typing import Tuple

MAGIC_HEADER = b"FTC1"

class StreamCompressor:
    @staticmethod
    def compress_batch(data: bytes, level: int = 6) -> bytes:
        compressed = zlib.compress(data, level=level)
        crc = zlib.crc32(data) & 0xFFFFFFFF
        header = struct.pack(">4sII", MAGIC_HEADER, len(data), crc)
        return header + compressed

    @staticmethod
    def decompress_batch(payload: bytes) -> Tuple[bytes, bool]:
        if len(payload) < 12:
            raise ValueError("Payload too short for header")
        magic, raw_len, expected_crc = struct.unpack(">4sII", payload[:12])
        if magic != MAGIC_HEADER:
            raise ValueError(f"Invalid magic header: {magic}")
        decompressed = zlib.decompress(payload[12:])
        if len(decompressed) != raw_len:
            return decompressed, False
        actual_crc = zlib.crc32(decompressed) & 0xFFFFFFFF
        return decompressed, actual_crc == expected_crc
