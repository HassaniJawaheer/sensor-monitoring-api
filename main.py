from fastapi import FastAPI
from routes.sensor import sensor_router


app = FastAPI(title="Sensor Monitoring API")

@app.get("/")
def get():
    return {"message": "Sensor Monitoring API"}


app.include_router(sensor_router)
 