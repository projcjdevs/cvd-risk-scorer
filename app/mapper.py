GUIDANCE = {
    "low": {
        "signal": "LOW RISK",
        "action": (
            "No immediate medical intervention needed. "
            "Provide lifestyle counseling on diet, physical activity, and smoking cessation."
        ),
        "referral": "No referral needed. Continue routine barangay health monitoring.",
        "medicines": "No maintenance medicines indicated at this time.",
        "follow_up": "Re-screen in 12 months, or sooner if new symptoms appear.",
        "lifestyle": [
            "Encourage at least 30 minutes of physical activity most days of the week.",
            "Advise reducing salt intake — avoid patis, bagoong, and processed foods.",
            "Promote a diet rich in vegetables, fish, and fruits available locally (malunggay, ampalaya, bangus).",
            "If smoker: counsel on smoking cessation. Refer to local quit-smoking program.",
            "Maintain healthy weight. Target BMI below 25.",
        ],
        "flag": None,
    },

    "moderate": {
        "signal": "MODERATE RISK",
        "action": (
            "Intensive lifestyle counseling required. "
            "Monitor blood pressure at every visit. "
            "If SBP remains above 140 mmHg on two separate visits, consider antihypertensive treatment."
        ),
        "referral": (
            "Refer to Rural Health Unit (RHU) physician within 1 month "
            "for full NCD assessment under PhilPEN protocol."
        ),
        "medicines": (
            "If BP uncontrolled after lifestyle changes: "
            "Amlodipine 5mg or Losartan 50mg available free under DOH ComPack program at the RHU."
        ),
        "follow_up": "Re-screen in 3 to 6 months. Document BP at every barangay visit.",
        "lifestyle": [
            "Strict salt restriction — target less than 5g per day (about 1 teaspoon).",
            "Daily physical activity: brisk walking, cycling, or any moderate exercise for 30 minutes.",
            "Advise weight loss if BMI is above 25. Even 3-5kg reduction lowers BP meaningfully.",
            "If smoker: strong cessation counseling. Smoking at this risk level significantly raises event probability.",
            "Limit alcohol. For men: no more than 2 drinks per day. For women: 1 drink per day.",
            "Teach patient to recognize warning signs: chest pain, sudden headache, numbness, vision changes.",
        ],
        "flag": None,
    },

    "high": {
        "signal": "HIGH RISK",
        "action": (
            "Immediate referral to RHU physician required. "
            "Do not wait for a second visit. "
            "Begin antihypertensive therapy and statin as per PhilPEN Step 3 protocol."
        ),
        "referral": (
            "Refer to RHU physician TODAY or at next available schedule within this week. "
            "If patient has chest pain, dizziness, or shortness of breath — refer to emergency immediately."
        ),
        "medicines": (
            "Antihypertensive: Amlodipine 5-10mg or Losartan 50-100mg (free under DOH ComPack). "
            "Statin: Atorvastatin 40mg for cholesterol management. "
            "Aspirin 80mg if no contraindications — discuss with physician."
        ),
        "follow_up": "Re-assess in 1 month after physician visit. Monthly BP monitoring at barangay.",
        "lifestyle": [
            "Strict dietary changes are now medically necessary, not optional.",
            "Eliminate high-sodium foods: canned goods, instant noodles, processed meats.",
            "Prioritize potassium-rich foods: bananas, kamote, sayote — help lower blood pressure.",
            "Moderate aerobic exercise as tolerated. If patient feels chest discomfort during activity, stop and refer.",
            "Complete smoking cessation. Each cigarette at this risk level is a direct cardiac threat.",
            "Stress reduction: encourage rest, social support, and community activities.",
        ],
        "flag": (
            "CLINICAL NOTE: If cholesterol or blood glucose were not measured, "
            "strongly recommend lab tests at RHU. Lab mode scoring would be more precise."
        ),
    },

    "very_high": {
        "signal": "VERY HIGH RISK",
        "action": (
            "URGENT. This patient requires immediate physician evaluation. "
            "Do not defer. Combination antihypertensive therapy and high-intensity statin are indicated."
        ),
        "referral": (
            "Refer to RHU or nearest hospital TODAY. "
            "If patient has any of the following — refer to emergency NOW: "
            "chest pain, jaw or arm pain, sudden severe headache, vision loss, weakness on one side of body, "
            "difficulty speaking, or loss of consciousness."
        ),
        "medicines": (
            "Dual antihypertensive therapy (e.g. Amlodipine + Losartan) — available free under DOH ComPack. "
            "High-intensity statin: Atorvastatin 40-80mg. "
            "Aspirin 80mg daily if no bleeding risk — confirm with physician. "
            "PhilHealth Z-benefit package may apply for cardiovascular cases — check eligibility at RHU."
        ),
        "follow_up": "Weekly BP monitoring until stable. Monthly physician follow-up minimum.",
        "lifestyle": [
            "All lifestyle modifications are now urgent and medically necessary.",
            "Complete rest from strenuous activity until cleared by physician.",
            "Strict low-sodium, low-fat diet. Avoid all fried, processed, and preserved foods.",
            "Absolute smoking cessation — immediate.",
            "Family support is critical. Involve household members in patient monitoring.",
            "Patient and family should know emergency warning signs by heart.",
        ],
        "flag": (
            "CRITICAL NOTE: This score indicates very high cardiovascular event risk. "
            "If only office mode was used, lab confirmation (cholesterol, blood glucose) is strongly recommended "
            "to rule out underestimation. Physician must be involved in all treatment decisions."
        ),
    },
}


def get_guidance(category: str, mode: str) -> dict:
    """
    Takes the risk category from scorer.py and the mode used,
    returns the full structured guidance object for the health worker.

    We pass 'mode' in so we can add a flag when office mode was used —
    reminding the BHW that lab results would sharpen the picture.
    """

    # Safety check — if an unexpected category comes in, default to very_high
    # Better to over-caution than under-caution in a clinical context
    guidance = GUIDANCE.get(category, GUIDANCE["very_high"]).copy()

    # If office mode was used and no flag already exists, add a gentle note
    if mode == "office" and guidance["flag"] is None:
        guidance["flag"] = (
            "Office mode used (no cholesterol or diabetes data provided). "
            "Result is a reliable screening estimate. "
            "For greater accuracy, obtain lipid panel and fasting blood glucose at RHU."
        )

    return guidance