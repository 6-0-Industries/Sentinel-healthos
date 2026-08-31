"""
Province health-risk endpoints.

Sentinel HealthOS 6.0
---------------------

Serves South Africa's 9 provinces with:
    1. Composite public-health risk score
    2. Contributing risk factors
    3. 14-day risk trend
    4. AI/rule-based public-health recommendations
    5. Responsible health function
    6. Priority and escalation guidance

IMPORTANT
---------
The current figures are DEMO DATA for MVP/dashboard development.

The recommendation engine is intentionally deterministic and explainable.
Once live EO/climate, air-quality and disease-surveillance feeds are
connected, the same recommendation layer can operate on live data.

The response schemas are designed to remain stable when the data source
changes.
"""

from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


router = APIRouter(
    prefix="/api/provinces",
    tags=["provinces"],
)


# ---------------------------------------------------------------------
# ENUMS
# ---------------------------------------------------------------------

class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class AdvicePriority(str, Enum):
    routine = "routine"
    monitor = "monitor"
    urgent = "urgent"
    critical = "critical"


class HealthFunction(str, Enum):
    disease_surveillance = "Disease Surveillance"
    environmental_health = "Environmental Health"
    emergency_preparedness = "Emergency Preparedness"
    primary_healthcare = "Primary Healthcare"
    outbreak_response = "Outbreak Response"
    health_promotion = "Health Promotion"
    maternal_child_health = "Maternal and Child Health"
    clinical_services = "Clinical Services"
    public_health_intelligence = "Public Health Intelligence"


# ---------------------------------------------------------------------
# RISK HELPERS
# ---------------------------------------------------------------------

def _risk_level(score: float) -> RiskLevel:
    if score >= 66:
        return RiskLevel.high
    if score >= 33:
        return RiskLevel.medium
    return RiskLevel.low


def _priority_from_score(score: float) -> AdvicePriority:
    if score >= 80:
        return AdvicePriority.critical
    if score >= 66:
        return AdvicePriority.urgent
    if score >= 33:
        return AdvicePriority.monitor
    return AdvicePriority.routine


# ---------------------------------------------------------------------
# PYDANTIC MODELS
# ---------------------------------------------------------------------

class RiskFactor(BaseModel):
    label: str
    value: float
    unit: str
    weight: float = Field(
        description="Relative contribution to the composite risk score, 0-1"
    )


class TrendPoint(BaseModel):
    date: str
    risk_score: float


class HealthRecommendation(BaseModel):
    priority: AdvicePriority
    health_function: HealthFunction
    recommendation: str
    rationale: str
    suggested_timeframe: str
    escalation_required: bool = False


class ProvinceRisk(BaseModel):
    code: str
    name: str
    capital: str
    risk_score: float = Field(ge=0, le=100)
    risk_level: RiskLevel
    population: int
    active_alerts: int


class ProvinceDetail(ProvinceRisk):
    factors: List[RiskFactor]
    trend: List[TrendPoint]
    recommendations: List[HealthRecommendation]
    last_updated: str


# ---------------------------------------------------------------------
# DEMO DATASET
# ---------------------------------------------------------------------

_RAW_PROVINCES = [
    {
        "code": "GP",
        "name": "Gauteng",
        "capital": "Johannesburg",
        "population": 16_000_000,
        "risk_score": 58,
        "active_alerts": 2,
        "factors": [
            ("Air Quality Index", 142, "AQI", 0.30),
            ("Population Density Exposure", 71, "score", 0.25),
            ("Rainfall Anomaly", -12, "% vs. norm", 0.15),
            ("Disease Surveillance Signal", 44, "score", 0.30),
        ],
    },
    {
        "code": "WC",
        "name": "Western Cape",
        "capital": "Cape Town",
        "population": 7_200_000,
        "risk_score": 27,
        "active_alerts": 0,
        "factors": [
            ("Air Quality Index", 48, "AQI", 0.30),
            ("Population Density Exposure", 39, "score", 0.25),
            ("Rainfall Anomaly", 6, "% vs. norm", 0.15),
            ("Disease Surveillance Signal", 18, "score", 0.30),
        ],
    },
    {
        "code": "KZN",
        "name": "KwaZulu-Natal",
        "capital": "Pietermaritzburg",
        "population": 11_500_000,
        "risk_score": 71,
        "active_alerts": 3,
        "factors": [
            ("Air Quality Index", 88, "AQI", 0.30),
            ("Population Density Exposure", 62, "score", 0.25),
            ("Rainfall Anomaly", 34, "% vs. norm", 0.15),
            ("Disease Surveillance Signal", 79, "score", 0.30),
        ],
    },
    {
        "code": "EC",
        "name": "Eastern Cape",
        "capital": "Bhisho",
        "population": 6_700_000,
        "risk_score": 63,
        "active_alerts": 2,
        "factors": [
            ("Air Quality Index", 55, "AQI", 0.30),
            ("Population Density Exposure", 48, "score", 0.25),
            ("Rainfall Anomaly", -28, "% vs. norm", 0.15),
            ("Disease Surveillance Signal", 74, "score", 0.30),
        ],
    },
    {
        "code": "LP",
        "name": "Limpopo",
        "capital": "Polokwane",
        "population": 5_900_000,
        "risk_score": 69,
        "active_alerts": 2,
        "factors": [
            ("Air Quality Index", 61, "AQI", 0.30),
            ("Population Density Exposure", 41, "score", 0.25),
            ("Rainfall Anomaly", 21, "% vs. norm", 0.15),
            ("Disease Surveillance Signal", 82, "score", 0.30),
        ],
    },
    {
        "code": "MP",
        "name": "Mpumalanga",
        "capital": "Mbombela",
        "population": 4_700_000,
        "risk_score": 52,
        "active_alerts": 1,
        "factors": [
            ("Air Quality Index", 76, "AQI", 0.30),
            ("Population Density Exposure", 37, "score", 0.25),
            ("Rainfall Anomaly", 15, "% vs. norm", 0.15),
            ("Disease Surveillance Signal", 51, "score", 0.30),
        ],
    },
    {
        "code": "NW",
        "name": "North West",
        "capital": "Mahikeng",
        "population": 4_100_000,
        "risk_score": 41,
        "active_alerts": 1,
        "factors": [
            ("Air Quality Index", 58, "AQI", 0.30),
            ("Population Density Exposure", 29, "score", 0.25),
            ("Rainfall Anomaly", -19, "% vs. norm", 0.15),
            ("Disease Surveillance Signal", 39, "score", 0.30),
        ],
    },
    {
        "code": "FS",
        "name": "Free State",
        "capital": "Bloemfontein",
        "population": 2_900_000,
        "risk_score": 33,
        "active_alerts": 0,
        "factors": [
            ("Air Quality Index", 41, "AQI", 0.30),
            ("Population Density Exposure", 22, "score", 0.25),
            ("Rainfall Anomaly", -8, "% vs. norm", 0.15),
            ("Disease Surveillance Signal", 29, "score", 0.30),
        ],
    },
    {
        "code": "NC",
        "name": "Northern Cape",
        "capital": "Kimberley",
        "population": 1_300_000,
        "risk_score": 19,
        "active_alerts": 0,
        "factors": [
            ("Air Quality Index", 22, "AQI", 0.30),
            ("Population Density Exposure", 9, "score", 0.25),
            ("Rainfall Anomaly", -4, "% vs. norm", 0.15),
            ("Disease Surveillance Signal", 14, "score", 0.30),
        ],
    },
]


# ---------------------------------------------------------------------
# TREND GENERATOR
# ---------------------------------------------------------------------

def _demo_trend(seed_score: float) -> List[TrendPoint]:
    """Generate a deterministic 14-day synthetic risk trend."""

    today = datetime.now(timezone.utc).date()

    points = []

    for i in range(13, -1, -1):
        day = today - timedelta(days=i)

        wobble = ((i * 37) % 11) - 5

        score = max(
            0,
            min(
                100,
                seed_score + wobble - (i * 0.4)
            )
        )

        points.append(
            TrendPoint(
                date=day.isoformat(),
                risk_score=round(score, 1),
            )
        )

    return points


# ---------------------------------------------------------------------
# RECOMMENDATION ENGINE
# ---------------------------------------------------------------------

def _get_factor(factors: List[RiskFactor], label: str) -> float:
    """
    Retrieve a factor value safely.
    """

    for factor in factors:
        if factor.label == label:
            return factor.value

    return 0


def generate_recommendations(
    province_name: str,
    risk_score: float,
    active_alerts: int,
    factors: List[RiskFactor],
) -> List[HealthRecommendation]:
    """
    Generate explainable public-health recommendations.

    This is currently a rules engine rather than a machine-learning model.
    This makes the recommendations auditable and easier for a provincial
    health authority to validate before deployment.
    """

    recommendations = []

    aqi = _get_factor(
        factors,
        "Air Quality Index"
    )

    population_exposure = _get_factor(
        factors,
        "Population Density Exposure"
    )

    rainfall = _get_factor(
        factors,
        "Rainfall Anomaly"
    )

    disease_signal = _get_factor(
        factors,
        "Disease Surveillance Signal"
    )

    # -------------------------------------------------------------
    # 1. HIGH OVERALL RISK
    # -------------------------------------------------------------

    if risk_score >= 66:

        recommendations.append(
            HealthRecommendation(
                priority=AdvicePriority.urgent,
                health_function=HealthFunction.public_health_intelligence,
                recommendation=(
                    f"Activate enhanced public-health surveillance "
                    f"for {province_name} and review the provincial "
                    f"risk situation at least daily."
                ),
                rationale=(
                    f"The composite provincial risk score is "
                    f"{risk_score}/100, placing the province in the "
                    f"high-risk category."
                ),
                suggested_timeframe="Within 24 hours",
                escalation_required=True,
            )
        )

    elif risk_score >= 33:

        recommendations.append(
            HealthRecommendation(
                priority=AdvicePriority.monitor,
                health_function=HealthFunction.public_health_intelligence,
                recommendation=(
                    f"Maintain enhanced monitoring of public-health "
                    f"indicators in {province_name} and review "
                    f"risk trends regularly."
                ),
                rationale=(
                    f"The composite risk score is "
                    f"{risk_score}/100, indicating moderate risk."
                ),
                suggested_timeframe="Within 72 hours",
                escalation_required=False,
            )
        )

    # -------------------------------------------------------------
    # 2. AIR QUALITY
    # -------------------------------------------------------------

    if aqi >= 100:

        recommendations.append(
            HealthRecommendation(
                priority=(
                    AdvicePriority.urgent
                    if aqi >= 150
                    else AdvicePriority.monitor
                ),
                health_function=HealthFunction.environmental_health,
                recommendation=(
                    "Coordinate with environmental-health and "
                    "air-quality authorities to investigate elevated "
                    "air pollution and strengthen public-health "
                    "risk communication."
                ),
                rationale=(
                    f"The air-quality factor is {aqi} AQI, indicating "
                    "an elevated environmental exposure signal."
                ),
                suggested_timeframe="Within 24–48 hours",
                escalation_required=aqi >= 150,
            )
        )

    # -------------------------------------------------------------
    # 3. POPULATION EXPOSURE
    # -------------------------------------------------------------

    if population_exposure >= 60:

        recommendations.append(
            HealthRecommendation(
                priority=AdvicePriority.urgent,
                health_function=HealthFunction.primary_healthcare,
                recommendation=(
                    "Review primary healthcare capacity, facility "
                    "readiness and medicine availability in high-density "
                    "communities. Prioritise areas with the greatest "
                    "population exposure."
                ),
                rationale=(
                    f"Population exposure score is "
                    f"{population_exposure}/100."
                ),
                suggested_timeframe="Within 72 hours",
                escalation_required=False,
            )
        )

    # -------------------------------------------------------------
    # 4. RAINFALL / CLIMATE ANOMALY
    # -------------------------------------------------------------

    if rainfall >= 20:

        recommendations.append(
            HealthRecommendation(
                priority=AdvicePriority.urgent,
                health_function=HealthFunction.emergency_preparedness,
                recommendation=(
                    "Review preparedness for rainfall-related "
                    "health risks, including flooding, waterborne "
                    "disease, disruption of healthcare services and "
                    "population displacement."
                ),
                rationale=(
                    f"Rainfall is {rainfall}% above the historical "
                    "norm, representing an elevated climate-related "
                    "exposure signal."
                ),
                suggested_timeframe="Within 24–72 hours",
                escalation_required=True,
            )
        )

    elif rainfall <= -20:

        recommendations.append(
            HealthRecommendation(
                priority=AdvicePriority.urgent,
                health_function=HealthFunction.emergency_preparedness,
                recommendation=(
                    "Assess drought-related health risks, including "
                    "water availability, food insecurity, sanitation "
                    "conditions and increased vulnerability among "
                    "high-risk communities."
                ),
                rationale=(
                    f"Rainfall is {abs(rainfall)}% below the historical "
                    "norm."
                ),
                suggested_timeframe="Within 72 hours",
                escalation_required=True,
            )
        )

    # -------------------------------------------------------------
    # 5. DISEASE SURVEILLANCE
    # -------------------------------------------------------------

    if disease_signal >= 70:

        recommendations.append(
            HealthRecommendation(
                priority=AdvicePriority.critical,
                health_function=HealthFunction.outbreak_response,
                recommendation=(
                    "Initiate enhanced disease surveillance and "
                    "epidemiological investigation. Review case trends, "
                    "geographic clustering and healthcare facility "
                    "capacity, and consider activating an outbreak "
                    "response structure where warranted."
                ),
                rationale=(
                    f"Disease surveillance signal is "
                    f"{disease_signal}/100."
                ),
                suggested_timeframe="Immediate",
                escalation_required=True,
            )
        )

    elif disease_signal >= 50:

        recommendations.append(
            HealthRecommendation(
                priority=AdvicePriority.urgent,
                health_function=HealthFunction.disease_surveillance,
                recommendation=(
                    "Increase disease surveillance frequency and "
                    "validate emerging signals with district and "
                    "facility-level data."
                ),
                rationale=(
                    f"Disease surveillance signal is "
                    f"{disease_signal}/100."
                ),
                suggested_timeframe="Within 48 hours",
                escalation_required=False,
            )
        )

    # -------------------------------------------------------------
    # 6. ACTIVE ALERTS
    # -------------------------------------------------------------

    if active_alerts >= 3:

        recommendations.append(
            HealthRecommendation(
                priority=AdvicePriority.urgent,
                health_function=HealthFunction.emergency_preparedness,
                recommendation=(
                    "Review all active public-health alerts and "
                    "coordinate an interdepartmental response "
                    "between surveillance, clinical services and "
                    "emergency preparedness teams."
                ),
                rationale=(
                    f"{active_alerts} active public-health alerts "
                    "are currently associated with the province."
                ),
                suggested_timeframe="Immediate",
                escalation_required=True,
            )
        )

    # -------------------------------------------------------------
    # 7. LOW-RISK DEFAULT
    # -------------------------------------------------------------

    if not recommendations:

        recommendations.append(
            HealthRecommendation(
                priority=AdvicePriority.routine,
                health_function=HealthFunction.public_health_intelligence,
                recommendation=(
                    f"Continue routine surveillance in {province_name} "
                    "and monitor for deterioration in environmental, "
                    "climate or disease indicators."
                ),
                rationale=(
                    f"Current composite risk score is "
                    f"{risk_score}/100 with no major threshold "
                    "breaches detected."
                ),
                suggested_timeframe="Routine monitoring",
                escalation_required=False,
            )
        )

    return recommendations


# ---------------------------------------------------------------------
# DEMO OBJECT FACTORY
# ---------------------------------------------------------------------

def _get_demo_provinces() -> List[ProvinceDetail]:
    """
    Constructs province objects dynamically per request to ensure real-time timestamps
    and up-to-date relative trend dates.
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    provinces = []

    for p in _RAW_PROVINCES:
        factors = [
            RiskFactor(
                label=label,
                value=value,
                unit=unit,
                weight=weight,
            )
            for label, value, unit, weight in p["factors"]
        ]

        recommendations = generate_recommendations(
            province_name=p["name"],
            risk_score=p["risk_score"],
            active_alerts=p["active_alerts"],
            factors=factors,
        )

        provinces.append(
            ProvinceDetail(
                code=p["code"],
                name=p["name"],
                capital=p["capital"],
                risk_score=p["risk_score"],
                risk_level=_risk_level(p["risk_score"]),
                population=p["population"],
                active_alerts=p["active_alerts"],
                factors=factors,
                trend=_demo_trend(p["risk_score"]),
                recommendations=recommendations,
                last_updated=now_iso,
            )
        )

    return provinces


# ---------------------------------------------------------------------
# API ENDPOINTS
# ---------------------------------------------------------------------

@router.get(
    "",
    response_model=List[ProvinceRisk]
)
def list_provinces():
    """
    Summary risk data for all 9 provinces.
    """
    demo_data = _get_demo_provinces()
    return [
        ProvinceRisk(
            code=p.code,
            name=p.name,
            capital=p.capital,
            risk_score=p.risk_score,
            risk_level=p.risk_level,
            population=p.population,
            active_alerts=p.active_alerts,
        )
        for p in demo_data
    ]


@router.get(
    "/summary/national"
)
def national_summary():
    """
    National roll-up used by the dashboard.
    """
    demo_data = _get_demo_provinces()

    scores = [
        p.risk_score
        for p in demo_data
    ]

    high_risk = [
        p
        for p in demo_data
        if p.risk_level == RiskLevel.high
    ]

    urgent_provinces = [
        p
        for p in demo_data
        if any(
            r.priority in [
                AdvicePriority.urgent,
                AdvicePriority.critical,
            ]
            for r in p.recommendations
        )
    ]

    return {
        "national_risk_index": round(
            sum(scores) / len(scores),
            1
        ),

        "provinces_at_high_risk": len(high_risk),

        "total_active_alerts": sum(
            p.active_alerts
            for p in demo_data
        ),

        "provinces_requiring_action": [
            {
                "code": p.code,
                "province": p.name,
                "risk_score": p.risk_score,
                "risk_level": p.risk_level,
                "top_action": p.recommendations[0].recommendation,
            }
            for p in urgent_provinces
        ],

        "last_updated": datetime.now(
            timezone.utc
        ).isoformat(),
    }


@router.get(
    "/{code}",
    response_model=ProvinceDetail
)
def get_province(code: str):
    """
    Full province detail including:
        - risk score
        - contributing factors
        - 14-day trend
        - health department recommendations
    """
    demo_data = _get_demo_provinces()
    by_code: Dict[str, ProvinceDetail] = {p.code: p for p in demo_data}

    province = by_code.get(code.upper())

    if not province:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown province code '{code}'",
        )

    return province
