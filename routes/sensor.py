from fastapi import APIRouter, status
from model.sensor_metadata import SensorMetadata
from sensor.manager import (
    create_sensor,
    delete_sensor,
    get_sensor,
    list_sensors,
)


sensor_router = APIRouter(
    prefix="/sensors",
    tags=["sensors"],
)


@sensor_router.post("/", status_code=status.HTTP_201_CREATED)
def add_sensor_route(sensor_metadata: SensorMetadata) -> dict:
    sensor_id = create_sensor(sensor_metadata)

    return {"sensor_id": sensor_id}


@sensor_router.get("/", status_code=status.HTTP_200_OK)
def list_sensors_route() -> list[dict]:
    return list_sensors()


@sensor_router.get("/{sensor_id}", status_code=status.HTTP_200_OK)
def get_sensor_route(sensor_id: int) -> dict:
    return get_sensor(sensor_id)


@sensor_router.delete("/{sensor_id}", status_code=status.HTTP_200_OK)
def delete_sensor_route(sensor_id: int) -> dict:
    deleted = delete_sensor(sensor_id)

    return {"deleted": deleted}