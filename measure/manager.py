from model.measure import Measure
from storage.sensor import SensorStorage
import os

db_path = os.getenv("DB_PATH", "data/monitoring.db")

def add_measuremnts(measure: Measure) -> None
    storage = SensorStorage(db_path)
    storage.store_measurement(measure)
    return None

def get_measurements(session_id: int | None) -> dict | list[dict]:
    