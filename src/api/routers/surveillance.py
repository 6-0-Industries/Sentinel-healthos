from datetime import datetime, timezone
from typing import Dict, List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/api/surveillance",
    tags=["Disease Surveillance & Outbreak Prediction"],
)


class OutbreakRisk(BaseModel):
    disease: str = Field(..., example="Malaria")
    risk_score: float = Field(..., description="Calculated risk index (0.0 to 1.0)")
    risk_level: str = Field(..., example="HIGH")
    primary_driver: str = Field(..., example="Heavy precipitation and high LST anomaly")


class OutbreakPredictionResponse(BaseModel):
    province_code: str = Field(..., example="KZN")
    overall_outbreak_risk: str = Field(..., example="HIGH")
    monitored_diseases: List[OutbreakRisk]
    generated_at: str


DEMO_SURVEILLANCE_DATA: Dict[str, dict] = {
    "GP": {
        "overall": "MODERATE",
        "diseases": [
            {"disease": "Respiratory Infections (AQI Driven)", "risk_score": 0.65, "risk_level": "MODERATE", "primary_driver": "Elevated PM2.5 & population density"},
            {"disease": "Enteric/Waterborne Illness", "risk_score": 0.30, "risk_level": "LOW", "primary_driver": "Stable water supply infrastructure"}
        ]
    },
    "KZN": {
        "overall": "HIGH",
        "diseases": [
            {"disease": "Malaria / Vector-Borne", "risk_score": 0.88, "risk_level": "HIGH", "primary_driver": "High humidity & 68.4mm rainfall anomaly"},
            {"disease": "Cholera Vector Signal", "risk_score": 0.55, "risk_level": "MODERATE", "primary_driver": "Flood runoff near coastal rivers"}
        ]
    },
    "WC": {
        "overall": "LOW",
        "diseases": [
            {"disease": "Viral Influenza", "risk_score": 0.40, "risk_level": "LOW", "primary_driver": "Seasonal temperature variance"},
            {"disease": "Vector-Borne Disease", "risk_score": 0.15, "risk_level": "LOW", "primary_driver": "Cool surface temperatures"}
        ]
    }
}


@router.get("/predictions/{province_code}", response_model=OutbreakPredictionResponse)
def get_outbreak_predictions(province_code: str):
    code = province_code.upper()
    
    # Default fallback for unlisted provinces in demo model
    data = DEMO_SURVEILLANCE_DATA.get(code, {
        "overall": "LOW",
        "diseases": [
            {"disease": "General Pathogen Outbreak Signal", "risk_score": 0.20, "risk_level": "LOW", "primary_driver": "Baseline climate metrics"}
        ]
