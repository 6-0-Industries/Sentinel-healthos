from datetime import datetime, timezone
from typing import Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/air-quality",
    tags=["Air Quality Monitoring"],
)


class AirQualityMetrics(BaseModel):
    province_code: str = Field(..., example="GP")
    aqi_index: int = Field(..., description="Air Quality Index (0-500)")
    pm2_5_ug_m3: float = Field(..., description="Fine Particulate Matter Concentration")
    pm10_ug_m3: float = Field(..., description="Coarse Particulate Matter Concentration")
    no2_ppb: float = Field(..., description="Nitrogen Dioxide level")
    category: str = Field(..., example="Moderate")
    updated_at: str


DEMO_AQI_DATA: Dict[str, dict] = {
    "GP": {"aqi_index": 115, "pm2_5_ug_m3": 41.2, "pm10_ug_m3": 78.5, "no2_ppb": 24.1, "category": "Unhealthy for Sensitive Groups"},
    "KZN": {"aqi_index": 55, "pm2_5_ug_m3": 14.8, "pm10_ug_m3": 28.0, "no2_ppb": 10.2, "category": "Moderate"},
    "WC": {"aqi_index": 32, "pm2_5_ug_m3": 7.5, "pm10_ug_m3": 15.1, "no2_ppb": 5.4, "category": "Good"},
}


@router.get("/metrics/{province_code}", response_model=AirQualityMetrics)
def get_air_quality_metrics(province_code: str):
    code = province_code.upper()
    data = DEMO_AQI_DATA.get(code, {
        "aqi_index": 45,
        "pm2_5_ug_m3": 10.0,
        "pm10_ug_m3": 20.0,
        "no2_ppb": 8.0,
        "category": "Good",
    })
    
    return AirQualityMetrics(
        province_code=code,
        aqi_index=data["aqi_index"],
        pm2_5_ug_m3=data["pm2_5_ug_m3"],
        pm10_ug_m3=data["pm10_ug_m3"],
        no2_ppb=data["no2_ppb"],
        category=data["category"],
        updated_at=datetime.now(timezone.utc).isoformat(),
    )
