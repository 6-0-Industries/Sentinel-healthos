from datetime import datetime, timezone
from typing import Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/earth-obs",
    tags=["Earth Observation & Climate Data"],
)


class EnvironmentalMetrics(BaseModel):
    province_code: str = Field(..., example="GP")
    ndvi_index: float = Field(..., description="Normalized Difference Vegetation Index (-1 to 1)")
    land_surface_temp_celsius: float = Field(..., description="Average LST in Celsius")
    precipitation_mm: float = Field(..., description="Recent 7-day cumulative rainfall")
    cloud_cover_percentage: float = Field(..., description="Satellite coverage noise metric")
    data_source: str = Field(default="Copernicus Sentinel-2 & NASA MODIS")
    last_updated: str


DEMO_EO_DATA: Dict[str, dict] = {
    "GP": {"ndvi_index": 0.35, "land_surface_temp_celsius": 24.5, "precipitation_mm": 12.0, "cloud_cover_percentage": 5.2},
    "WC": {"ndvi_index": 0.52, "land_surface_temp_celsius": 19.8, "precipitation_mm": 45.1, "cloud_cover_percentage": 14.8},
    "KZN": {"ndvi_index": 0.68, "land_surface_temp_celsius": 26.2, "precipitation_mm": 68.4, "cloud_cover_percentage": 22.1},
    "EC": {"ndvi_index": 0.48, "land_surface_temp_celsius": 21.0, "precipitation_mm": 28.3, "cloud_cover_percentage": 8.0},
    "FS": {"ndvi_index": 0.28, "land_surface_temp_celsius": 23.1, "precipitation_mm": 5.0, "cloud_cover_percentage": 2.1},
    "MP": {"ndvi_index": 0.61, "land_surface_temp_celsius": 25.0, "precipitation_mm": 34.0, "cloud_cover_percentage": 10.5},
    "LP": {"ndvi_index": 0.42, "land_surface_temp_celsius": 28.7, "precipitation_mm": 8.2, "cloud_cover_percentage": 3.0},
    "NW": {"ndvi_index": 0.22, "land_surface_temp_celsius": 27.4, "precipitation_mm": 2.1, "cloud_cover_percentage": 1.5},
    "NC": {"ndvi_index": 0.12, "land_surface_temp_celsius": 31.0, "precipitation_mm": 0.0, "cloud_cover_percentage": 0.5},
}


@router.get("/metrics/{province_code}", response_model=EnvironmentalMetrics)
def get_provincial_eo_metrics(province_code: str):
    code = province_code.upper()
    if code not in DEMO_EO_DATA:
        raise HTTPException(status_code=404, detail=f"Province code '{province_code}' not found.")
    
    data = DEMO_EO_DATA[code]
    return EnvironmentalMetrics(
        province_code=code,
        ndvi_index=data["ndvi_index"],
        land_surface_temp_celsius=data["land_surface_temp_celsius"],
        precipitation_mm=data["precipitation_mm"],
        cloud_cover_percentage=data["cloud_cover_percentage"],
        last_updated=datetime.now(timezone.utc).isoformat(),
    )
