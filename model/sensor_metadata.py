from pydantic import BaseModel

class SensorMetadata(BaseModel):
    unit: str
    name: str
    type: str
    min_valid_value: float
    max_valid_value: float