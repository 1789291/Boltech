# Claims API (FastAPI)

GenAI-powered claims explanation on top of a trained ML approval model.  
Predict whether a claim is approved (0/1) and, given a final decision, generate a concise, defensible reason using ChatGPT.

---

## ✨ Features

- **Prediction**: Preprocess → encode → align features → `RandomForest` predict.
- **Explanation**: Given a claim record **with** `decision` (`ACCEPT`/`DECLINE`), call ChatGPT to produce a short JSON rationale.
- **FastAPI** with interactive docs at `/docs`.
- **Docker** support.

---

## 🗂️ Project Layout

```
ASSESSMENT/
├─ artifacts/
│  ├─ encoders/
│  ├─ metrics/
│  └─ models/                # random_forest.pkl (+ feature_order.pkl recommended)
├─ config/
│  ├─ config.toml
│  └─ settings.py
├─ data/
│  └─ claim_use_case_dataset.xlsx
├─ docker/
│  └─ Dockerfile
├─ inference/
│  └─ __init__.py            # Infer: drop → fillna → encode → OHE → datetime → align
├─ models/
│  └─ __init__.py            # Pydantic models (ClaimDataRequest)
├─ preprocess/
│  └─ __init__.py
├─ train/
│  └─ __init__.py            # (training logic if present)
├─ app.py                    # FastAPI entrypoint
├─ requirements.txt
└─ .env                      # environment variables (optional)
```

---

## ✅ Requirements

- Python **3.10–3.12**
- `pip` (and optionally `virtualenv`)
- For explanations: an **OpenAI API key**

---

## 🚀 Quickstart (Local)

```bash
# from project root
python -m venv .venv
source .venv/bin/activate                # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file (or export in your shell):

```bash
OPENAI_API_KEY=sk-********************************
```

### Model & encoders

Ensure these files exist (produced by your training workflow):

```
artifacts/models/random_forest.pkl
artifacts/encoders/binary_encoders.pkl
artifacts/encoders/ohe_encoder.pkl
# Recommended: exact training column order
artifacts/models/feature_order.pkl
```

### Run the server

```bash
uvicorn app:app --reload
# Open http://127.0.0.1:8000/docs
```

---

## 🐳 Docker

```bash
# Build
docker build -t claims-api -f docker/Dockerfile .

# Run
docker run --rm -p 8000:8000   -e OPENAI_API_KEY=sk-********************************   claims-api
# Visit http://127.0.0.1:8000/docs
```

---

## 🔌 API

### 1) `POST /predict` — single record

- **Body**: one JSON object matching `ClaimDataRequest`
- **Response**: `{"predictions": [0|1]}`

```bash
curl -X POST http://127.0.0.1:8000/predict   -H "Content-Type: application/json"   -d @data.json
```

**Example body (truncated):**
```json
{
  "excessFee": 139.0,
  "rrp": 1319.0,
  "balanceRRP": 1319.0,
  "oldBalanceRRP": 1319.0,
  "productName": "NL_MANDATORY_ADLD_1Y_UPFRONT_SMARTPHONE_Q5B5",
  "productDesc": "WUAWEI Care+ ...",
  "coverage": "ADLD",
  "productCode": "NLADLD1247",
  "policyStartDate": 1678320000000,
  "policyEndDate": 1709942400000,
  "policyStatus": "Active",
  "deviceType": "SMARTPHONES",
  "make": "WUAWEI",
  "model": "WUAWEI-AAA176",
  "purchaseDate": 1678320000000,
  "deviceCost": 0,
  "relationship": "self",
  "channel": "Online Portal",
  "claimType": "Accidental Damage",
  "country": "NL",
  "turnOnOff": 1.0,
  "touchScreen": 0.0,
  "smashed": 0.0,
  "frontCamera": 0.0,
  "backCamera": 0.0,
  "frontOrBackCamera": 0.0,
  "audio": 1.0,
  "mic": 0.0,
  "buttons": 0.0,
  "connection": 0.0,
  "charging": 0.0,
  "other": "…",
  "issueDesc": "…"
}
```

---

### 2) `POST /batch-predict` — multiple records

- **Body**: JSON array of objects
- **Response**: `{"predictions": [0, 1, ...]}`

```bash
curl -X POST http://127.0.0.1:8000/batch-predict   -H "Content-Type: application/json"   -d '[{...},{...}]'
```

---

### 3) `POST /explain` — GenAI rationale for a decision

- **Body**: a **single** claim **including** `"decision": "ACCEPT"` or `"DECLINE"`
- **Requires**: `OPENAI_API_KEY`
- **Response** (shape):
```json
{
  "decision": "ACCEPT",
  "summary": "…",
  "key_factors": [
    {"field": "coverage", "value": "ADLD", "impact": "+", "rationale": "matches claimType"},
    {"field": "policyStatus", "value": "Active", "impact": "+", "rationale": "policy is active"},
    {"field": "policyStartDate/policyEndDate", "value": "…", "impact": "+", "rationale": "within period"}
  ],
  "policy_checks": {
    "coverage_matches_claim_type": true,
    "policy_active_at_incident": true,
    "within_policy_period": true,
    "device_eligible": true
  },
  "excess_fee_note": "Excess of 139.0 applies.",
  "data_gaps": [],
  "suggested_next_steps": ["Proceed to repair logistics."],
  "confidence": 0.82
}
```

---

## 🧠 Preprocessing (at inference)

1. Drop columns per `config/config.toml`.
2. Fill missing:
   - **Binary flags**: per-column mode.
   - **Categoricals**: mode → fallback `"MISSING"`, cast to string.
   - **Continuous**: median.
3. Encode:
   - **Binary**: `LabelEncoder` (`artifacts/encoders/binary_encoders.pkl`).
   - **Categorical**: `OneHotEncoder(handle_unknown="ignore")` (`artifacts/encoders/ohe_encoder.pkl`).
4. Datetime features: extract year/month/day if applicable.
5. **Align columns** to training order (`model.feature_names_in_` or `artifacts/models/feature_order.pkl`).
6. Predict via `RandomForest`.

---

## 🧾 Field Order (expected by the model)

```
excessFee, rrp, balanceRRP, oldBalanceRRP,
productName, productDesc, coverage, productCode,
policyStartDate, policyEndDate,
policyStatus, retailerName, deviceType, make, model,
purchaseDate, deviceCost,
relationship, channel, claimType, country,
turnOnOff, touchScreen, smashed, frontCamera, backCamera,
frontOrBackCamera, audio, mic, buttons, connection, charging,
other, issueDesc
```

> Dates may be **epoch ms** or `dd/mm/YYYY`. Binary/triage fields should be numeric (0/1).

---

## 🛠️ Troubleshooting

- **FileNotFoundError: artifacts/models/random_forest.pkl**  
  Ensure artifacts exist at the specified paths. Prefer `pathlib` + paths relative to file location.

- **ValueError: Feature names should match those that were passed during fit.**  
  Reindex features before predict:
  ```python
  X = X.reindex(columns=list(model.feature_names_in_), fill_value=0)
  # or load artifacts/models/feature_order.pkl and reindex to that list
  ```

- **OHE transform TypeError / NaNs in categoricals**  
  Fill categoricals with mode then `"MISSING"`, and `astype("string")` before `ohe.transform`.

- **422 Unprocessable Entity**  
  Body shape/type mismatch. `/predict` expects an **object**; `/batch-predict` expects an **array**.

- **OpenAI error**  
  Set `OPENAI_API_KEY`. Ensure network egress is allowed.

---

## 🧪 Testing ideas

- Unit tests for `inference` to verify:
  - No missing columns after alignment
  - Encoders load and transform as expected
- Smoke tests for endpoints (200 status, JSON shape).

---

## 📄 License / Notes

Internal demo for a claims approval prototype with GenAI explanations.  
Do **not** commit secrets (API keys) or personal data to the repo.
