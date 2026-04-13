from app.scorer import compute_risk
from app.mapper import get_guidance


def run_assessment(
    age: int,
    sex: str,
    sbp: int,
    smoking: bool,
    bmi: float = None,
    total_chol: float = None,
    diabetes: bool = None,
) -> dict:


    score = compute_risk(
        age=age,
        sex=sex,
        sbp=sbp,
        smoking=smoking,
        bmi=bmi,
        total_chol=total_chol,
        diabetes=diabetes,
    )

    guidance = get_guidance(score["category"], score["mode"])

    return {
        "signal":    guidance["signal"],
        "mode_used": score["mode"],
        "action":    guidance["action"],
        "referral":  guidance["referral"],
        "medicines": guidance["medicines"],
        "follow_up": guidance["follow_up"],
        "lifestyle": guidance["lifestyle"],
        "flag":      guidance["flag"],
    }