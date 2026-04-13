from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from app.engine import run_assessment

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


