import os
from storage.sensor import SensorStorage
from model.sensor_metadata import SensorMetadata


db_path = os.getenv("DB_PATH", "data/monitoring.db")


def create_sensor(sensor_metadata: SensorMetadata) -> int:
    sensor_storage = SensorStorage(db_path)

    metadata = sensor_metadata.model_dump()
    sensor_id = sensor_storage.add_sensor(metadata)

    return sensor_id


def get_sensor(sensor_id: int) -> dict:
    sensor_storage = SensorStorage(db_path)

    return sensor_storage.fetch_sensor(sensor_id)


def list_sensors() -> list[dict]:
    sensor_storage = SensorStorage(db_path)

    return sensor_storage.fetch_all_sensors()


def delete_sensor(sensor_id: int) -> bool:
    sensor_storage = SensorStorage(db_path)

    return sensor_storage.delete_sensor(sensor_id)