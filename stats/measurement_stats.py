from measure.manager import get_measurements
from storage.sensor import SensorStorage
from statistics import mean, median
import os

db_path = os.getenv("DB_PATH", "data/monitoring.db")

def summarize_sensor(
    sensor_id: int, 
    start_timestamp: str | None = None,
    end_timestamp: str | None = None,
) -> dict:
    # Get the measures
    measures = get_measurements(
        sensor_id,
        start_timestamp,
        end_timestamp
    )

    if measures == []:
        {
            "period": (start_timestamp, end_timestamp),
            "count": 0,
            "min": None,
            "max": None,
            "mean": None,
            "median": None
        }

    # Aggregate
    ## Get values
    values = [d["value"] for d in measures]

    return {
        "period": (start_timestamp, end_timestamp),
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": mean(values),
        "median": median(values)
    }

def summarize(
    start_timestamp: str | None = None,
    end_timestamp: str | None = None
) -> list[dict]:
    
    sensor_storage = SensorStorage(db_path)
    sensor_ids = sensor_storage.fetch_sensors_id()

    summary = []

    for sensor_id in sensor_ids:
        summary.append(
            summarize_sensor(
                sensor_id,
                start_timestamp,
                end_timestamp
            )
        )

    return summary
