from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

from app.engine import run_assessment
from app.translator import SUPPORTED_LANGUAGES

app = FastAPI(
    title="CVD Risk Scorer API",
    description=(
        "A Philippines-calibrated cardiovascular risk screening API "
        "for barangay health workers. Built on the WHO HEARTS framework "
        "and Globorisk PH-calibrated equation. Outputs PhilPEN-aligned "
        "clinical guidance — not a diagnosis."
    ),
    version="1.0.0",
)

class PatientInput(BaseModel):
    age: int = Field(
        ...,                        
        ge=40,                       
        le=80,                       
        description="Patient age in years. Valid range: 40–80 (Globorisk model bounds)."
    )
    sex: str = Field(
        ...,
        pattern="^(male|female)$",  
        description="Biological sex: 'male' or 'female'."
    )
    systolic_bp: int = Field(
        ...,
        ge=80,
        le=250,
        description="Systolic blood pressure in mmHg."
    )
    smoking: bool = Field(
        ...,
        description="True if current smoker, False if non-smoker or ex-smoker."
    )
    bmi: Optional[float] = Field(
        default=None,
        ge=10.0,
        le=60.0,
        description="Body Mass Index in kg/m². Used in office mode when cholesterol is unavailable."
    )
    total_cholesterol: Optional[float] = Field(
        default=None,
        ge=1.0,
        le=15.0,
        description="Total cholesterol in mmol/L. If provided along with diabetes, enables lab mode."
    )
    diabetes: Optional[bool] = Field(
        default=None,
        description="True if diagnosed diabetic or fasting glucose ≥ 126 mg/dL. Required for lab mode."
    )

    language: str = Field(
    default="en",
    description=(
        "Response language. Supported codes: "
        "en (English), fil (Filipino), "
        "ceb (Cebuano), hil (Hiligaynon), ilo (Ilocano)"
    )
)

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 58,
                "sex": "male",
                "systolic_bp": 155,
                "smoking": True,
                "bmi": 26.5,
                "total_cholesterol": None,
                "diabetes": None,
            }
        }
    }


@app.get("/")
def root():
    return {
        "service": "PulsoRisk",
        "status": "running",
        "note": "POST to /score with patient vitals to receive CVD risk guidance.",
    }


@app.post("/score")
def score(patient: PatientInput):
    result = run_assessment(
        age=patient.age,
        sex=patient.sex,
        sbp=patient.systolic_bp,
        smoking=patient.smoking,
        bmi=patient.bmi,
        total_chol=patient.total_cholesterol,
        diabetes=patient.diabetes,
        language=patient.language,
    )
    return result

@app.get("/languages")
def get_languages():
    """Returns all supported language codes and their names."""
    return {
        "supported": [
            {"code": code, "name": config["name"]}
            for code, config in SUPPORTED_LANGUAGES.items()
        ]
    }
