from datetime import datetime, timezone
from typing import Dict
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/climate",
    tags=["Climate-Health Monitoring"],
)


class ClimateVulnerabilityMetrics(BaseModel):
    province_code: str = Field(..., example="KZN")
    heat_wave_risk_score: float = Field(..., description="0.0 to 1.0 vulnerability index")
    drought_index: float = Field(..., description="SPI Drought index")
    flood_susceptibility: str = Field(..., example="HIGH")
    vulnerable_population_exposure: int = Field(..., description="Estimated population impacted")
    updated_at: str


DEMO_CLIMATE_DATA: Dict[str, dict] = {
    "GP": {"heat_wave_risk_score": 0.45, "drought_index": -0.2, "flood_susceptibility": "MODERATE", "vulnerable_population_exposure": 1200000},
    "KZN": {"heat_wave_risk_score": 0.78, "drought_index": 1.1, "flood_susceptibility": "HIGH", "vulnerable_population_exposure": 850000},
    "WC": {"heat_wave_risk_score": 0.30, "drought_index": -1.5, "flood_susceptibility": "LOW", "vulnerable_population_exposure": 400000},
}


@router.get("/vulnerability/{province_code}", response_model=ClimateVulnerabilityMetrics)
def get_climate_vulnerability(province_code: str):
    code = province_code.upper()
    data = DEMO_CLIMATE_DATA.get(code, {
        "heat_wave_risk_score": 0.25,
        "drought_index": 0.0,
        "flood_susceptibility": "LOW",
        "vulnerable_population_exposure": 250000,
    })
    
    return ClimateVulnerabilityMetrics(
        province_code=code,
        heat_wave_risk_score=data["heat_wave_risk_score"],
        drought_index=data["drought_index"],
        flood_susceptibility=data["flood_susceptibility"],
        vulnerable_population_exposure=data["vulnerable_population_exposure"],
        updated_at=datetime.now(timezone.utc).isoformat(),
