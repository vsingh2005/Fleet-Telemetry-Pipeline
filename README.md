# Fleet-Telemetry-Pipeline

A modular streaming telemetry pipeline designed for high-throughput IoT vehicle sensor ingestion, real-time statistical anomaly detection, and partitioned columnar storage for analytical SQL querying.

## Overview

Modern fleet operations generate continuous streams of high-frequency sensor readings (speed, engine RPM, battery temperature, GPS coordinates). Processing these streams requires handling bursty ingestion traffic without memory exhaustion, detecting outliers in real time without batch recomputations, and storing records efficiently for low-latency analytical queries.

This repository implements an end-to-end telemetry engine featuring a memory-bounded circular ring buffer, online anomaly detection using Welford's algorithm, kinematic filtering, spatial geofencing, and columnar Parquet archiving queried via embedded DuckDB.

## Architecture

```
[IoT Sensors / CAN Bus]
          |
          v
+-----------------------+     FIFO Eviction
| Circular Ring Buffer  | <------------------ Fixed Memory Cap
+-----------------------+
          |
          v
+-----------------------------------------------+
| Stream Processing & Analytics Engine          |
|  - Welford's Algorithm (Sliding Z-Score)      |
|  - 1D/2D Kalman Trajectory Smoothing          |
|  - Spatial Geofencing & Speed Hysteresis      |
|  - Token Bucket Rate Limiting                 |
+-----------------------------------------------+
          |
          v
+-----------------------+
| Partitioned Parquet   | (Snappy-compressed, run/date partitioned)
+-----------------------+
          |
          v
+-----------------------+
| Embedded DuckDB Engine| (Sub-millisecond analytical SQL queries)
+-----------------------+
```

## Core Modules and Engineering Details

- **Buffered Ingestion (`buffer.py`, `rate_limiter.py`)**: Implements a thread-safe circular ring buffer with fixed capacity and FIFO eviction semantics. Protects against out-of-memory (OOM) failures during network latency spikes while enforcing token-bucket rate limiting on incoming telemetry batches.
- **Online Anomaly Detection (`detector.py`)**: Computes running sample mean, variance, and dynamic z-scores over sliding temporal windows using Welford's algorithm. Achieves O(1) time and O(N) space complexity per observation, avoiding the numerical instability and compute overhead of naive sum-of-squares recomputation.
- **Trajectory Filtering (`kalman.py`)**: Applies discrete Kalman filtering to sensor channels (GPS coordinates and speed) to mitigate high-frequency sensor noise and measurement drift.
- **Spatial Analysis & Compliance (`geofence.py`, `geohash.py`, `speed_compliance.py`)**: Includes ray-casting point-in-polygon verification for polygonal geofences, 32-bit Geohash encoding for spatial locality queries, and speed compliance monitoring with hysteresis thresholds to prevent alert flapping.
- **CAN Bus Frame Parsing (`can_parser.py`)**: Decodes standard automotive CAN bus frames and bitfields into structured telemetry payloads.
- **Columnar Storage & Analytical Querying (`storage.py`, `analytics.py`)**: Batches validated records into Snappy-compressed Apache Parquet files partitioned by device and date. Uses embedded DuckDB for vectorized, zero-copy analytical SQL queries directly over the Parquet datasets.

## Technical Decisions

- **Why Welford's Algorithm over standard rolling windows**: Computing sample variance via standard rolling formulas requires two passes or is prone to catastrophic numerical cancellation. Welford's algorithm updates mean and variance incrementally in a single pass with provable numerical stability.
- **Why Circular Ring Buffer over Unbounded Queues**: In edge and constrained gateway deployments, unbounded queues risk fatal memory exhaustion under burst traffic. A pre-allocated circular buffer guarantees deterministic memory consumption.
- **Why Columnar Parquet over Row-Oriented Storage**: Vehicle telemetry datasets are dominated by aggregations over specific numerical fields (e.g., average fuel rate or peak battery temperature). Columnar layouts reduce disk I/O by over 70% compared to JSON or CSV and allow vectorized SIMD execution in DuckDB.

## Technology Stack

- **Language**: Python 3.11+
- **Data Storage & Format**: Apache Parquet, PyArrow, Snappy Compression
- **Analytics Engine**: DuckDB
- **Validation & Typing**: Pydantic v2
- **Testing**: Pytest, Pytest-Cov

## Project Structure

```
fleet-telemetry-pipeline/
├── src/
│   └── fleet_telemetry/
│       ├── buffer.py           # Thread-safe circular ring buffer
│       ├── detector.py         # Welford sliding-window anomaly detector
│       ├── storage.py          # Partitioned Parquet sink
│       ├── analytics.py        # DuckDB analytical query layer
│       ├── kalman.py           # Kalman filter for GPS/telemetry smoothing
│       ├── geofence.py         # Polygonal geofencing algorithms
│       ├── geohash.py          # Spatial geohash indexing
│       ├── speed_compliance.py # Speed compliance with hysteresis
│       ├── can_parser.py       # CAN bus frame parsing
│       └── rate_limiter.py     # Token bucket rate limiter
├── tests/                      # Automated unit and integration test suite
├── pyproject.toml              # Build metadata and dependency specifications
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

```bash
git clone https://github.com/vsingh2005/Fleet-Telemetry-Pipeline.git
cd Fleet-Telemetry-Pipeline
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
pytest tests/ -v
```