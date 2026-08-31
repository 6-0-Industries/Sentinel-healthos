from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/surveillance", tags=["Outbreak Surveillance"])

class SurveillancePredictionResponse(BaseModel):
    province_code: str
    outbreak_risk_score: float
    primary_driver: str
    predicted_outbreak_index: str

# Mock data mapping for provincial surveillance predictions
SURVEILLANCE_DATA = {
    "GP": {"outbreak_risk_score": 0.72, "primary_driver": "Respiratory Pathogens", "predicted_outbreak_index": "High Alert"},
    "KZN": {"outbreak_risk_score": 0.85, "primary_driver": "Waterborne Microbes", "predicted_outbreak_index": "Critical"},
    "WC": {"outbreak_risk_score": 0.41, "primary_driver": "Seasonal Influenza", "predicted_outbreak_index": "Moderate"},
    "EC": {"outbreak_risk_score": 0.63, "primary_driver": "Vector-borne Pathogens", "predicted_outbreak_index": "Elevated"},
    "FS": {"outbreak_risk_score": 0.38, "primary_driver": "Airborne Pathogens", "predicted_outbreak_index": "Low"},
    "LP": {"outbreak_risk_score": 0.78, "primary_driver": "Malaria / Vector-borne", "predicted_outbreak_index": "High Alert"},
    "MP": {"outbreak_risk_score": 0.69, "primary_driver": "Waterborne Microbes", "predicted_outbreak_index": "Elevated"},
    "NC": {"outbreak_risk_score": 0.25, "primary_driver": "Heat Strain / Enteric", "predicted_outbreak_index": "Low"},
    "NW": {"outbreak_risk_score": 0.52, "primary_driver": "Dust / Respiratory", "predicted_outbreak_index": "Moderate"},
}

@router.get("/predictions/{province_code}", response_model=SurveillancePredictionResponse)
def get_surveillance_predictions(province_code: str):
    code = province_code.upper()
    data = SURVEILLANCE_DATA.get(code, {
        "outbreak_risk_score": 0.50,
        "primary_driver": "General Environmental Exposure",
        "predicted_outbreak_index": "Moderate"
    })
    return SurveillancePredictionResponse(
        province_code=code,
        outbreak_risk_score=data["outbreak_risk_score"],
        primary_driver=data["primary_driver"],
        predicted_outbreak_index=data["predicted_outbreak_index"]
    )
