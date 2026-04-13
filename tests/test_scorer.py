from app.scorer import compute_risk

# Test 1: Mang Pablo — 58yo male smoker, high BP, no cholesterol available
pablo = compute_risk(age=58, sex="male", sbp=155, smoking=True, bmi=26.5)
print("PABLO (office mode):", pablo)

# Test 2: Same patient but WITH cholesterol — should switch to lab mode
pablo_lab = compute_risk(
    age=58, sex="male", sbp=155, smoking=True,
    bmi=26.5, total_chol=5.8, diabetes=False
)
print("PABLO (lab mode):", pablo_lab)

# Test 3: Low-risk patient — young female, non-smoker, normal BP
lorna = compute_risk(age=42, sex="female", sbp=118, smoking=False, bmi=22.0)
print("LORNA (low risk):", lorna)

# Test 4: Very high risk — older male, very high BP, smoker, diabetic
ernesto = compute_risk(
    age=72, sex="male", sbp=175, smoking=True,
    total_chol=6.5, diabetes=True
)
print("ERNESTO (very high):", ernesto)