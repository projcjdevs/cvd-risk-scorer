import math

LAB_COEF = {
    "age":     0.0491,   # each additional year increases risk
    "sbp":     0.0107,   # each mmHg of systolic BP increases risk
    "tc":      0.1967,   # total cholesterol in mmol/L
    "smk":     0.7229,   # current smoker (1) vs non-smoker (0)
    "dm":      0.5626,   # diabetes (1) vs no diabetes (0)
    "sex_smk": 0.3430,   # extra risk for MALE smokers 
    "sex_dm":  0.4013,   # extra risk for MALE diabetics 
}

OFFICE_COEF = {
    "age":     0.0491,
    "sbp":     0.0107,
    "bmi":     0.0249,   # BMI replaces cholesterol + diabetes in office mode
    "smk":     0.7229,
    "sex_smk": 0.3430,
}

# --- PH-Specfic Values ---

PH_S0 = {
    "male":   0.9021,
    "female": 0.9612,
}

PH_MEANS = {
    "age":        52.4,
    "sbp":        130.2,
    "tc":         5.10,    
    "bmi":        23.8,
    "smk_male":   0.48,    # 48% of Filipino males smoke
    "smk_female": 0.06,    # 6% of Filipino females smoke
    "dm_male":    0.07,
    "dm_female":  0.08,
}

# --- Risk Categories ---
def get_category(risk: float) -> str:
    if risk < 0.10:
        return "low"
    elif risk < 0.20:
        return "moderate"
    elif risk < 0.30:
        return "high"
    else:
        return "very_high"
    
# --- Scorer ---

def compute_risk(
    age: int,
    sex: str,           
    sbp: int,           
    smoking: bool,
    bmi: float = None,
    total_chol: float = None,
    diabetes: bool = None,
) -> dict:

    is_male = 1 if sex == "male" else 0
    smk = 1 if smoking else 0
    s0 = PH_S0[sex]
    m = PH_MEANS

    use_lab = (total_chol is not None) and (diabetes is not None)

    if use_lab:
        dm = 1 if diabetes else 0
        tc = total_chol

        bX = (
            LAB_COEF["age"] * age
            + LAB_COEF["sbp"] * sbp
            + LAB_COEF["tc"] * tc
            + LAB_COEF["smk"] * smk
            + LAB_COEF["dm"] * dm
            + LAB_COEF["sex_smk"] * is_male * smk
            + LAB_COEF["sex_dm"] * is_male * dm
        )

        mean_smk = m["smk_male"] if is_male else m["smk_female"]
        mean_dm  = m["dm_male"]  if is_male else m["dm_female"]

        bX_bar = (
            LAB_COEF["age"] * m["age"]
            + LAB_COEF["sbp"] * m["sbp"]
            + LAB_COEF["tc"] * m["tc"]
            + LAB_COEF["smk"] * mean_smk
            + LAB_COEF["dm"] * mean_dm
        )
        mode = "lab"

    else:
        bmi_val = bmi if bmi is not None else m["bmi"]  

        bX = (
            OFFICE_COEF["age"] * age
            + OFFICE_COEF["sbp"] * sbp
            + OFFICE_COEF["bmi"] * bmi_val
            + OFFICE_COEF["smk"] * smk
            + OFFICE_COEF["sex_smk"] * is_male * smk
        )

        mean_smk = m["smk_male"] if is_male else m["smk_female"]

        bX_bar = (
            OFFICE_COEF["age"] * m["age"]
            + OFFICE_COEF["sbp"] * m["sbp"]
            + OFFICE_COEF["bmi"] * m["bmi"]
            + OFFICE_COEF["smk"] * mean_smk
        )
        mode = "office"


    risk = 1 - (s0 ** math.exp(bX - bX_bar))
    risk = max(0.0, min(1.0, risk))  

    return {
        "risk_10yr": round(risk, 4),
        "risk_pct":  round(risk * 100, 1),
        "category":  get_category(risk),
        "mode":      mode,
    }