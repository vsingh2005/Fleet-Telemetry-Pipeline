"""
Partition batching compactor for merging micro-batches before disk flush.
"""
from typing import Dict, List, Any
import pandas as pd

class PartitionCompactor:
    def __init__(self, batch_size_threshold: int = 100):
        self.threshold = batch_size_threshold
        self.partitions: Dict[str, List[Dict[str, Any]]] = {}

    def add_record(self, partition_key: str, record: Dict[str, Any]) -> bool:
        if partition_key not in self.partitions:
            self.partitions[partition_key] = []
        self.partitions[partition_key].append(record)
        return len(self.partitions[partition_key]) >= self.threshold

    def drain_partition(self, partition_key: str) -> pd.DataFrame:
        records = self.partitions.pop(partition_key, [])
        return pd.DataFrame(records)

    def drain_all(self) -> Dict[str, pd.DataFrame]:
        results = {}
        for key in list(self.partitions.keys()):
            results[key] = self.drain_partition(key)
        return results
