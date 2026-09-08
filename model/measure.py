from pydantic import BaseModel

class Measure(BaseModel):
    sensor_id: int
    timestamp: str
    value: str