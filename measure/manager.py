import os
from model.measure import Measure
from storage.sensor import SensorStorage

db_path = os.getenv("DB_PATH", "data/monitoring.db")


def add_measurement(measure: Measure) -> None:
    storage = SensorStorage(db_path)

    storage.store_measurement(measure.model_dump())

def get_measurements(
    sensor_id: int,
    start_timestamp: str | None = None,
    end_timestamp: str | None = None
) -> list[dict]:
    storage = SensorStorage(db_path)

    return storage.fetch_measurements(
        sensor_id,
        start_timestamp,
        end_timestamp
    )