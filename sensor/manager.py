import os
from storage.sensor import SensorStorage
from model.sensor_metadata import SensorMetadata

db_path = os.getenv("DB_PATH", "data/monitoring")

def create_sensor(sensor_metadata: SensorMetadata):
    sensor_storage = SensorStorage(db_path)
    metadata = sensor_metadata.model_dump()
    sensor_id = sensor_storage.add_sensor(metadata)
    return sensor_id

def get_sensor(sensor_id: str) -> dict[str, str]:
    sensor_storage = SensorStorage(db_path)