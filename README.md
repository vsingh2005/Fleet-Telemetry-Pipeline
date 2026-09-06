# Fleet-Telemetry-Pipeline

A streaming data pipeline for ingesting IoT sensor data, calculating rolling stats for anomaly detection, and saving records to partitioned Parquet files for fast querying in DuckDB.

## What it does

- **Buffered Ingestion**: Uses a circular ring buffer to handle bursts of incoming sensor packets without spiking memory.
- **Rolling Anomaly Detection**: Calculates dynamic z-scores over sliding windows using Welford's algorithm to catch outliers in real time.
- **Parquet Storage**: Batches records into compressed Parquet files partitioned by timestamp or device.
- **Fast SQL Queries**: Uses embedded DuckDB to run analytical SQL queries directly over the stored Parquet files.

## Stack

Python, DuckDB, PyArrow, Pytest