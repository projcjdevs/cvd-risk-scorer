from app.engine import run_assessment

print("=" * 60)
print("TEST 1: PABLO — 58yo male smoker, high BP, office mode")
print("=" * 60)
pablo = run_assessment(age=58, sex="male", sbp=155, smoking=True, bmi=26.5)
for key, value in pablo.items():
    print(f"{key}: {value}")

print()
print("=" * 60)
print("TEST 2: LORNA — 42yo female, non-smoker, normal BP")
print("=" * 60)
lorna = run_assessment(age=42, sex="female", sbp=118, smoking=False, bmi=22.0)
for key, value in lorna.items():
    print(f"{key}: {value}")

print()
print("=" * 60)
print("TEST 3: ERNESTO — 72yo male, very high risk, lab mode")
print("=" * 60)
ernesto = run_assessment(
    age=72, sex="male", sbp=175, smoking=True,
    total_chol=6.5, diabetes=True
)
for key, value in ernesto.items():
    print(f"{key}: {value}")