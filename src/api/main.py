from fastapi import FastAPI
from src.api.routers import climate, earth_obs, provinces, surveillance

app = FastAPI(
    title="Sentinel HealthOS 6.0",
    description="Provincial Public Health Risk, Earth Observation, Surveillance & Climate API",
    version="6.0.0",
)

# Register endpoints
app.include_router(provinces.router)
app.include_router(earth_obs.router)
app.include_router(surveillance.router)
app.include_router(climate.router)


@app.get("/")
def read_root():
    return {"status": "online", "system": "Sentinel HealthOS 6.0"}
