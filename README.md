# Fleet-Telemetry-Pipeline

[![CI](https://github.com/vsingh2005/Fleet-Telemetry-Pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/vsingh2005/Fleet-Telemetry-Pipeline/actions/workflows/ci.yml)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)
![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)

Distributed edge IoT telemetry ingestion, streaming anomaly detection, and Parquet analytical sink.

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
- **Real-Time Anomaly Detection**: Streaming sliding-window Z-score (Welford's algorithm), rolling median absolute deviation (MAD), and threshold violation filters.
- **Columnar Analytics**: Direct export to partition-aware Parquet files with zero-copy DuckDB SQL queries.
- **Resilience**: Exponential backoff reconnection policies and local disk cache fallback for disconnected edge nodes.

## Tech Stack

Python 3.11+, DuckDB, PyArrow, Apache Parquet, Pydantic, Pytest
