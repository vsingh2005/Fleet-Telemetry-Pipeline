# Fleet Telemetry Pipeline

High-throughput distributed edge IoT telemetry ingestion, streaming window statistics, and columnar Parquet archival engine designed for resource-constrained automotive and industrial sensor networks.

## Architecture & Overview

```
[ Edge Sensor Nodes ] ────► [ Ingestion Broker ] ────► [ Sliding Window Anomaly Engine ]
 (CAN-Bus / MQTT / BLE)        (Async Ring Buffer)          (Z-Score / IQR / Quantiles)
                                                                       │
                                                                       ▼
                                                          [ Columnar Storage & Analytics ]
                                                             (DuckDB / Apache Parquet)
```

## Features
- **Asynchronous Ingestion**: Lock-free circular ring buffer handling high-frequency multi-channel sensor events.
- **Real-Time Anomaly Detection**: Streaming sliding-window Z-score, rolling median absolute deviation (MAD), and threshold violation filters.
- **Columnar Analytics**: Direct export to partition-aware Parquet files with zero-copy DuckDB SQL queries.
- **Resilience**: Exponential backoff reconnection policies and local disk cache fallback for disconnected edge nodes.

## Tech Stack
- **Language**: Python 3.11+ / Typing
- **Storage & Query**: DuckDB, PyArrow, Apache Parquet
- **Testing & Quality**: Pytest, Ruff, Mypy

## Quickstart

```bash
# Install dependencies
pip install -e .

# Run test suite
pytest tests/ -v
```
