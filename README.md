# Sensor Monitoring API

A REST API for storing, querying, and analyzing sensor measurements.

## Features

* **Sensor management**: Create, retrieve, list, and delete sensors.
* **Measurement storage**: Store and retrieve sensor measurements.
* **Statistics**: Compute basic statistics such as count, min, max, mean, and median.
* **Anomaly detection**: Detect measurements outside the valid range of a sensor.
* **Time filtering**: Filter measurements and analytics by time period.

## Tech Stack

Python, FastAPI, SQLite, Pydantic

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

Optional `start_timestamp` and `end_timestamp` query parameters can be used to filter measurements and analytics by time period.
