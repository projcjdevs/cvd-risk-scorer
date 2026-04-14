# PH-based CVD Risk Scorer

A FastAPI API for cardiovascular disease (CVD) risk screening, calibrated for the Philippines using the Globorisk equation and PhilPEN clinical guidance. Multilingual output for barangay health workers and clinicians.

---

## Features

- Automatic risk scoring (Globorisk PH-calibrated)
- PhilPEN-aligned clinical guidance
- Multilingual output: Filipino, Cebuano, Hiligaynon, Ilocano, English
- Simple API: one POST endpoint, auto-selects mode (office/lab)

---

## Setup & Installation

**Prerequisites:** Python 3.9+, pip, Git, internet connection (for translation)

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOURUSERNAME/pulsorisk.git
   cd pulsorisk
   ```
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac / Linux
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Core: fastapi, uvicorn, pydantic, deep-translator

---

## Running the API

```bash
uvicorn app.api:app --reload
```

Visit: http://localhost:8000

Docs: http://localhost:8000/docs

---

## Running Tests

```bash
python tests/test_scorer.py
```

You should see three test patients with correct risk levels:

- Pablo (58yo male smoker, high BP) → HIGH RISK, office mode
- Lorna (42yo female, normal BP, non-smoker) → LOW RISK, office mode
- Ernesto (72yo male, very high BP, diabetic, smoker) → VERY HIGH RISK, lab mode

---

## Example API Usage

**Health check:**

```bash
curl http://localhost:8000/
```

**Supported languages:**

```bash
curl http://localhost:8000/languages
```

**Score (office mode):**

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 58,
    "sex": "male",
    "systolic_bp": 155,
    "smoking": true,
    "bmi": 26.5
  }'
```

**Score (lab mode):**

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 58,
    "sex": "male",
    "systolic_bp": 155,
    "smoking": true,
    "bmi": 26.5,
    "total_cholesterol": 5.8,
    "diabetes": false
  }'
```

**Score (Filipino output):**

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 58,
    "sex": "male",
    "systolic_bp": 155,
    "smoking": true,
    "bmi": 26.5,
    "language": "fil"
  }'
```

**Score (low risk):**

```bash
curl -X POST "http://localhost:8000/score" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 42,
    "sex": "female",
    "systolic_bp": 118,
    "smoking": false,
    "bmi": 22.0
  }'
```

---

## Input Validation Rules

| Field             | Rule/Range                                |
| ----------------- | ----------------------------------------- |
| age               | 40–80 (Globorisk bounds)                  |
| sex               | "male" or "female"                        |
| systolic_bp       | 80–250                                    |
| bmi               | 10.0–60.0 (if provided)                   |
| total_cholesterol | 1.0–15.0 mmol/L (if provided)             |
| language          | Falls back to English if unsupported code |

_For patients outside 40–80: model is not validated. Under-40: give lifestyle advice. Over-80: refer to physician._

---

## Mode Selection Logic

- If both `total_cholesterol` and `diabetes` are provided: **lab mode** (more accurate)
- Otherwise: **office mode** (uses BMI)
- If neither BMI nor lab values: office mode uses PH mean BMI (23.6) as fallback (flagged in response)

---

## Project Structure

```
pulsorisk/
├── app/
│   ├── scorer.py      # Risk equation + PH calibration
│   ├── mapper.py      # PhilPEN guidance by risk tier
│   ├── translator.py  # Multilingual support
│   ├── engine.py      # Pipeline logic
│   └── api.py         # FastAPI routes
├── tests/
│   └── test_scorer.py # End-to-end tests
├── requirements.txt
├── README.md
```

**Debugging tips:**

- Wrong risk score → scorer.py
- Wrong clinical guidance → mapper.py
- Translation issues → translator.py
- API field errors → engine.py or api.py

---

## Common Errors

- **ModuleNotFoundError: No module named 'app'**
  Run from project root, not inside app/.
- **Address already in use**
  Port 8000 busy. Use another port: `uvicorn app.api:app --reload --port 8001`
- **Translation failed**
  No internet or Google endpoint down. English output is returned as fallback.
- **422 Unprocessable Entity**
  Input failed validation. See the `detail` field in the response.
- **uvicorn: command not found**
  Virtual environment not active or dependencies missing. Activate venv and reinstall requirements.
- **Stopping the server**
  Press CTRL+C in the terminal. To deactivate venv: `deactivate`

---

## References

- [Globorisk CVD Risk Score](https://www.globorisk.org/)
- [PhilPEN Protocol (DOH)](https://doh.gov.ph/sites/default/files/publications/PhilPEN%20Protocol.pdf)
- [WHO HEARTS Technical Package](https://www.who.int/teams/noncommunicable-diseases/cardiovascular-diseases/management/tools/hearts)
