from fastapi import FastAPI
from routes.sensor import sensor_router
from routes.measures import measure_router
from routes.analytics import analytics_router


app = FastAPI(title="Sensor Monitoring API")

@app.get("/")
def get():
    return {"message": "Sensor Monitoring API"}


app.include_router(sensor_router)
app.include_router(measure_router)
app.include_router(analytics_router)
 