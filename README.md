# Sensor Monitoring API

A REST API for storing, querying, and analyzing sensor measurements.

## Features

* **Sensor management**: Create, retrieve, list, and delete sensors.
* **Measurement storage**: Store and retrieve sensor measurements.
* **Statistics**: Compute basic statistics such as count, min, max, mean, and median.
* **Anomaly detection**: Detect measurements outside the valid range of a sensor.
* **Time filtering**: Filter measurements and analytics by time period.

## Tech Stack

Python, FastAPI, SQLite, Pydantic, Requests, Uvicorn

## Project Structure

```text
sensor-monitoring-api/
├── main.py
├── model/
├── storage/
├── sensor/
├── measure/
├── analytics/
├── routes/
└── data/
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Run

```bash
uvicorn main:app --reload
```

The API documentation is available at `/docs`.

## Quick Start

Create at least two sensors before loading the sample measurements.

Example:

```bash
curl http://127.0.0.1:8000/sensors/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"reactor_temp_01","type":"temperature","unit":"°C","min_valid_value":10.0,"max_valid_value":80.0}'
```

```bash
curl http://127.0.0.1:8000/sensors/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"pressure_sensor_01","type":"pressure","unit":"bar","min_valid_value":1.0,"max_valid_value":5.0}'
```

The sample data expects these sensors to have IDs `1` and `2`.

Populate the database:

```bash
python3 scripts/populate_data.py
```

You can then test the API, for example:

```bash
curl http://127.0.0.1:8000/measures/1
```

```bash
curl http://127.0.0.1:8000/analytics/stats/1
```

```bash
curl "http://127.0.0.1:8000/analytics/stats/1?start_timestamp=2026-09-12T15:30:00&end_timestamp=2026-09-12T15:40:00"
```

The API documentation is available at `/docs`.

## API Endpoints

| Method | Endpoint                           | Description                    |
| ------ | ---------------------------------- | ------------------------------ |
| POST   | `/sensors/`                        | Create a sensor                |
| GET    | `/sensors/`                        | List sensors                   |
| GET    | `/sensors/{sensor_id}`             | Get a sensor                   |
| DELETE | `/sensors/{sensor_id}`             | Delete a sensor                |
| POST   | `/measures/`                       | Store a measurement            |
| GET    | `/measures/{sensor_id}`            | Get sensor measurements        |
| GET    | `/analytics/stats/{sensor_id}`     | Get sensor statistics          |
| GET    | `/analytics/stats`                 | Get statistics for all sensors |
| GET    | `/analytics/anomalies/{sensor_id}` | Get sensor anomalies           |
| GET    | `/analytics/anomalies`             | Get anomalies for all sensors  |
