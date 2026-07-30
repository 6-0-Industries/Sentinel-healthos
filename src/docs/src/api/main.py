from fastapi import FastAPI

app = FastAPI(
    title="Sentinel HealthOS",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Sentinel HealthOS",
        "status": "Running"
    }

@app.get("/health")
def health():
    return {
        "status": "Healthy"
    }
