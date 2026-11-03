"""
Sequence-ordered packet jitter buffer for reassembling out-of-order packets.
"""
from typing import Dict, List, Any

class PacketJitterBuffer:
    def __init__(self, max_buffer_size: int = 50):
        self.max_buffer_size = max_buffer_size
        self.expected_seq = 0
        self.buffer: Dict[int, Any] = {}

    def insert(self, seq_num: int, payload: Any) -> List[Any]:
        if seq_num < self.expected_seq:
            return []
            
        self.buffer[seq_num] = payload
        ready: List[Any] = []
        while self.expected_seq in self.buffer:
            ready.append(self.buffer.pop(self.expected_seq))
            self.expected_seq += 1
            
        if len(self.buffer) > self.max_buffer_size:
            min_seq = min(self.buffer.keys())
            del self.buffer[min_seq]
            self.expected_seq = min_seq + 1
            
        return ready
