from fastapi import APIRouter, status

from analytics.statistics import (
    summarize_sensor,
    summarize,
)
from analytics.anomaly import (
    detect_sensor_anomalies,
    detect_anomalies,
)


analytics_router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
)


@analytics_router.get(
    "/stats/{sensor_id}",
    status_code=status.HTTP_200_OK,
)
def get_sensor_stats_route(
    sensor_id: int,
    start_timestamp: str | None = None,
    end_timestamp: str | None = None,
) -> dict:
    return summarize_sensor(
        sensor_id,
        start_timestamp,
        end_timestamp,
    )


@analytics_router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
)
def get_all_stats_route(
    start_timestamp: str | None = None,
    end_timestamp: str | None = None,
) -> list[dict]:
    return summarize(
        start_timestamp,
        end_timestamp,
    )


@analytics_router.get(
    "/anomalies/{sensor_id}",
    status_code=status.HTTP_200_OK,
)
def get_sensor_anomalies_route(
    sensor_id: int,
    start_timestamp: str | None = None,
    end_timestamp: str | None = None,
) -> list[dict]:
    return detect_sensor_anomalies(
        sensor_id,
        start_timestamp,
        end_timestamp,
    )


@analytics_router.get(
    "/anomalies",
    status_code=status.HTTP_200_OK,
)
def get_all_anomalies_route(
    start_timestamp: str | None = None,
    end_timestamp: str | None = None,
) -> dict[int, list[dict]]:
    return detect_anomalies(
        start_timestamp,
        end_timestamp,
    )