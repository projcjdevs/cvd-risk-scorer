from app.scorer import compute_risk
from app.mapper import get_guidance
from app.translator import translate_response, SUPPORTED_LANGUAGES


def run_assessment(
    age: int,
    sex: str,
    sbp: int,
    smoking: bool,
    bmi: float = None,
    total_chol: float = None,
    diabetes: bool = None,
    language: str = "en",
) -> dict:

    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    score = compute_risk(
        age=age, sex=sex, sbp=sbp, smoking=smoking,
        bmi=bmi, total_chol=total_chol, diabetes=diabetes,
    )

    guidance = get_guidance(score["category"], score["mode"])

    result = {
        "signal":    guidance["signal"],
        "mode_used": score["mode"],
        "action":    guidance["action"],
        "referral":  guidance["referral"],
        "medicines": guidance["medicines"],
        "follow_up": guidance["follow_up"],
        "lifestyle": guidance["lifestyle"],
        "flag":      guidance["flag"],
    }

    result = translate_response(result, language)

    return result