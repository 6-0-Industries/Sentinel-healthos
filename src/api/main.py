from fastapi import FastAPI
from src.api.routers import provinces

app = FastAPI(
    title="Sentinel HealthOS 6.0",
    description="Provincial Public Health Risk & Surveillance API",
    version="6.0.0",
)

# Mount the provincial endpoints
app.include_router(provinces.router)


@app.get("/")
def read_root():
    return {"status": "online", "system": "Sentinel HealthOS 6.0"}
