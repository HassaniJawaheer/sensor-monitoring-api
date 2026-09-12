from measure.manager import get_measurements
from sensor.manager import get_sensor
from storage.sensor import SensorStorage
import os

db_path = os.getenv("DB_PATH", "data/monitoring.db")

def detect_sensor_anomalies(
    sensor_id: int,
    start_timestamp: str | None = None,
    end_timestamp: str | None = None
) -> list[dict]:
    """Return out-of-range measurements for a sensor."""

    sensor = get_sensor(sensor_id)

    measures = get_measurements(
        sensor_id,
        start_timestamp,
        end_timestamp
    )

    return [
        measure
        for measure in measures
        if measure["value"] < sensor["min_valid_value"]
        or measure["value"] > sensor["max_valid_value"]
    ]

def detect_anomalies(
    start_timestamp: str | None = None,
    end_timestamp: str | None = None
) -> dict[int, list[dict]]:

    sensor_storage = SensorStorage(db_path)
    sensor_ids = sensor_storage.fetch_sensors_id()

    result = {}
    for sensor_id in sensor_ids:
        result[sensor_id] = detect_sensor_anomalies(
            sensor_id,
            start_timestamp,
            end_timestamp
        )
    return result