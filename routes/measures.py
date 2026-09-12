from fastapi import APIRouter, status
from model.measure import Measure
from measure.manager import (
    add_measurement,
    get_measurements,
)


measure_router = APIRouter(
    prefix="/measures",
    tags=["measures"],
)


@measure_router.post("/", status_code=status.HTTP_201_CREATED)
def add_measurement_route(measure: Measure) -> None:
    add_measurement(measure)


@measure_router.get("/{sensor_id}", status_code=status.HTTP_200_OK)
def get_measurements_route(
    sensor_id: int,
    start_timestamp: str | None = None,
    end_timestamp: str | None = None,
) -> list[dict]:
    return get_measurements(
        sensor_id,
        start_timestamp,
        end_timestamp,
    )
