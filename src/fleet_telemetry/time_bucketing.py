"""
DuckDB time-bucketed rolling metrics query engine.
"""
import duckdb
import pandas as pd

class DuckDBTimeBucketEngine:
    def __init__(self):
        self.con = duckdb.connect(database=":memory:")
        self.con.execute("""
            CREATE TABLE telemetry (
                vehicle_id VARCHAR,
                ts TIMESTAMP,
                speed DOUBLE,
                rpm DOUBLE
            )
        """)

    def insert_records(self, df: pd.DataFrame):
        self.con.register("temp_df", df)
        self.con.execute("INSERT INTO telemetry SELECT * FROM temp_df")
        self.con.unregister("temp_df")

    def query_bucketed_stats(self, interval: str = "5 minute") -> pd.DataFrame:
        query = f"""
            SELECT 
                time_bucket(INTERVAL '{interval}', ts) as bucket,
                vehicle_id,
                COUNT(*) as point_count,
                AVG(speed) as avg_speed,
                MAX(speed) as max_speed,
                AVG(rpm) as avg_rpm
            FROM telemetry
            GROUP BY 1, 2
            ORDER BY 1 ASC
        """
        return self.con.execute(query).df()
