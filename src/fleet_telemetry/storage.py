from pathlib import Path
from typing import Any, Dict, List
import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
from fleet_telemetry.models import TelemetryRecord

class ParquetStorageSink:
    def __init__(self, base_directory: str = "data/telemetry"):
        self.base_dir = Path(base_directory)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def write_batch(self, records: List[TelemetryRecord], partition_key: str = "default") -> Path:
        if not records:
            raise ValueError("Cannot write empty batch")
        rows = [r.to_row() for r in records]
        table = pa.Table.from_pylist(rows)
        dest_dir = self.base_dir / f"partition={partition_key}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        first_ts = records[0].timestamp.strftime("%Y%m%d_%H%M%S")
        dest_file = dest_dir / f"telemetry_{first_ts}.parquet"
        pq.write_table(table, dest_file, compression="SNAPPY")
        return dest_file

    def query_sql(self, sql_query: str) -> List[Dict[str, Any]]:
        pattern = str(self.base_dir / "**" / "*.parquet").replace("\\", "/")
        con = duckdb.connect(database=":memory:")
        con.execute(f"CREATE VIEW telemetry_view AS SELECT * FROM read_parquet('{pattern}')")
        result = con.execute(sql_query).df()
        return result.to_dict(orient="records")
