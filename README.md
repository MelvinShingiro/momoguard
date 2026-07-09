# MomoGuard — Full Project Specification

> Real-time mobile money fraud detection for East Africa.
> Inspired by Stripe Radar's ML-powered transaction scoring.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Real-World Data Sources](#real-world-data-sources)
3. [Tech Stack](#tech-stack)
4. [Folder Structure](#folder-structure)
5. [Environment Variables](#environment-variables)
6. [Dataset & Feature Engineering](#dataset--feature-engineering)
7. [Model Architecture](#model-architecture)
8. [API Contract](#api-contract)
9. [Testing Strategy](#testing-strategy)
10. [Docker Setup](#docker-setup)
11. [CI/CD Pipeline](#cicd-pipeline)
12. [Deployment](#deployment)
13. [Monitoring & Model Drift](#monitoring--model-drift)
14. [Version Roadmap](#version-roadmap)
15. [Week-by-Week Build Plan](#week-by-week-build-plan)

---

## Project Overview

**Problem:** Mobile money fraud (account takeover, SIM-swap, agent fraud) costs East Africa
hundreds of millions of USD annually. Stripe Radar solves this for card payments with ML.
Nothing comparable exists for MoMo-style USSD transactions.

**Solution:** A fraud scoring API that ingests a transaction payload and returns a risk score
(0–1) + human-readable reasons, backed by a trained XGBoost classifier with SHAP explanations.
Includes a React analyst dashboard and automated model retraining pipeline.

**Industry parallel:** Stripe Radar (real-time ML risk scoring on financial transactions)

---

## Real-World Data Sources

This project uses **real, public, free** datasets and APIs.

### 1. Base Transaction Dataset
- **Source:** [PaySim dataset — Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1)
- **License:** CC0 (public domain) — free to use
- **What it is:** 6.3M synthetic mobile money transactions modeled on real Mpesa data from
  African financial logs, with ground-truth fraud labels. Created for academic fraud research.
- **How to get it:** `kaggle datasets download -d ealaxi/paysim1` (requires free Kaggle account)
  OR download manually and place in `data/raw/`
- **Features included:** transaction type, amount, account balances before/after, fraud flag

### 2. Rwanda / EAC Phone Number Prefixes
- **Source:** [ITU National Numbering Plans](https://www.itu.int/oth/T0202.aspx?lang=en) — free
- **Used for:** Detecting SIM-swap patterns (number recently changed prefix = higher risk)
- **Implementation:** Static JSON file `data/reference/rw_phone_prefixes.json`

### 3. ExchangeRate API (USD ↔ RWF)
- **API:** [ExchangeRate-API](https://www.exchangerate-api.com/) — free tier
- **Used for:** Normalizing transaction amounts across currencies before model inference

### 4. Live Fraud News Feed (for dashboard)
- **API:** [NewsData.io](https://newsdata.io/) — free tier, 200 req/day
- **Endpoint:** `GET https://newsdata.io/api/1/news?q=mobile+money+fraud+africa&country=rw,ke,ug`
- **Used for:** "Recent fraud trends" panel in analyst dashboard

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Data processing | Python + Pandas | Standard for data pipelines |
| ML training | scikit-learn + XGBoost | Industry-standard tabular ML |
| Explainability | SHAP | Explains predictions as feature contributions |
| Experiment tracking | MLflow (local) | Model versioning, metric tracking |
| API | FastAPI | Async Python API, auto-generates OpenAPI docs |
| API validation | Pydantic | Type-safe request/response models |
| Database | PostgreSQL | Stores transactions, predictions, analyst feedback |
| ORM | SQLAlchemy + Alembic | Python ORM + migrations |
| Dashboard | React + TypeScript | Real-time score monitoring |
| Charts | Recharts | Score distributions, feature importance |
| Testing | pytest + httpx | Fast, async-friendly |
| Load testing | Locust | Simulate 100 req/s against scoring endpoint |
| Containerization | Docker + Docker Compose | Reproducible ML environment |
| CI/CD | GitHub Actions | Lint, test, model quality gates |
| Deployment | Render.com (API) + Hugging Face Spaces (dashboard) | Both free |
| Monitoring | Evidently AI | Free open-source ML monitoring / data drift |

---

## Folder Structure

```
momoguard/
├── .github/
│   └── workflows/
│       ├── ci.yml                   # Lint + tests + model quality gate
│       └── deploy.yml               # Deploy API on push to main
│
├── data/
│   ├── raw/                         # PaySim CSV (gitignored — too large)
│   ├── processed/                   # Feature-engineered parquet files
│   └── reference/
│       └── rw_phone_prefixes.json
│
├── notebooks/                       # Jupyter notebooks (EDA only, not prod code)
│   ├── 01_eda.ipynb                 # Exploratory data analysis
│   ├── 02_feature_engineering.ipynb # Feature experiments
│   └── 03_model_comparison.ipynb    # Comparing classifiers
│
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py                # Load and validate raw PaySim CSV
│   │   ├── features.py              # All feature engineering logic
│   │   └── splitter.py              # Train/val/test split (time-aware)
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── trainer.py               # XGBoost training + cross-validation
│   │   ├── evaluator.py             # Precision, recall, F1, AUROC
│   │   └── explainer.py             # SHAP value computation
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app
│   │   ├── routers/
│   │   │   ├── score.py             # POST /score
│   │   │   ├── feedback.py          # POST /feedback (analyst labels FP/FN)
│   │   │   └── health.py            # GET /health
│   │   ├── schemas/
│   │   │   ├── transaction.py       # Pydantic input model
│   │   │   └── score_response.py    # Pydantic output model
│   │   ├── services/
│   │   │   ├── scorer.py            # Loads model, runs inference
│   │   │   └── currency.py          # ExchangeRate-API wrapper
│   │   └── db/
│   │       ├── models.py            # SQLAlchemy ORM models
│   │       ├── session.py           # DB session factory
│   │       └── crud.py              # DB read/write functions
│   │
│   └── monitoring/
│       ├── drift_report.py          # Evidently drift report generation
│       └── scheduler.py             # Weekly drift check (APScheduler)
│
├── alembic/                         # DB migrations
│   ├── env.py
│   └── versions/
│
├── models/                          # Saved model artifacts (gitignored)
│   └── .gitkeep
│
├── mlruns/                          # MLflow experiment tracking (gitignored)
│
├── tests/
│   ├── unit/
│   │   ├── test_features.py         # Feature engineering correctness
│   │   ├── test_scorer.py           # Scorer output shape + range
│   │   └── test_schemas.py          # Pydantic validation
│   ├── integration/
│   │   ├── test_score_endpoint.py   # POST /score full round-trip
│   │   ├── test_feedback_endpoint.py
│   │   └── test_health_endpoint.py
│   └── performance/
│       └── locustfile.py            # Load test: 100 req/s for 60s
│
├── scripts/
│   ├── download_data.sh             # Kaggle download helper
│   ├── train.py                     # CLI: python scripts/train.py
│   └── retrain.py                   # CLI: triggered by feedback loop
│
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── pyproject.toml                   # Poetry deps + ruff config
├── pytest.ini
└── README.md
```

---

## Environment Variables

### `.env.example`
```env
# Database
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/momoguard"

# Model
MODEL_PATH="models/xgboost_fraud_v1.pkl"
FRAUD_THRESHOLD=0.5           # Score above this → flagged

# External APIs (all free)
EXCHANGERATE_API_KEY=""        # exchangerate-api.com free tier
NEWSDATA_API_KEY=""            # newsdata.io free tier

# App
PORT=8000
ENV=development

# Monitoring
SENTRY_DSN=""
```

---

## Dataset & Feature Engineering

### Raw PaySim columns used
```
step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig,
nameDest, oldbalanceDest, newbalanceDest, isFraud
```

### Engineered features (`src/data/features.py`)
```python
# Velocity features
"tx_count_1h"           # How many transactions from this sender in last 1 hour
"tx_count_24h"          # Same, 24 hours
"amount_sum_24h"        # Total amount sent in 24h

# Amount features
"log_amount"            # log(amount + 1) — normalizes skewed distribution
"amount_vs_balance"     # amount / (oldbalanceOrg + 1) — emptying account signal
"balance_diff_orig"     # oldbalanceOrg - newbalanceOrig - amount  (should be ~0)
"balance_diff_dest"     # newbalanceDest - oldbalanceDest - amount  (should be ~0)

# Type encoding
"type_CASH_OUT"         # One-hot encoded transaction type
"type_TRANSFER"

# Time features
"hour_of_day"           # 0-23 — late night = higher risk
"is_weekend"            # bool

# Account features
"is_new_dest_account"   # destination account has < 5 prior transactions
```

### Class imbalance handling
PaySim dataset is ~0.13% fraud. Strategies used:
- `scale_pos_weight` in XGBoost (ratio of negative to positive)
- Evaluation on F1 + AUROC, NOT accuracy (accuracy is misleading here)

---

## Model Architecture

### Training pipeline (`scripts/train.py`)
```
1. Load raw PaySim CSV
2. Feature engineering → DataFrame
3. Time-aware train/val/test split (no data leakage — val/test are chronologically later)
4. XGBoost classifier with MLflow autolog
5. Evaluate: precision, recall, F1, AUROC on test set
6. Compute SHAP values for feature importance
7. Save model artifact + feature list as pkl
8. MLflow logs: params, metrics, model version
```

### Quality gates (enforced in CI)
```
Precision ≥ 0.85  (1 in 6 alerts is a false alarm at most)
Recall    ≥ 0.75  (catch at least 3/4 of all fraud)
AUROC     ≥ 0.90
```
If any gate fails, CI fails and the model is NOT deployed.

### Inference pipeline (`src/api/services/scorer.py`)
```
1. Receive transaction payload
2. Compute real-time features (velocity requires querying last N transactions from DB)
3. Run XGBoost predict_proba → risk_score ∈ [0, 1]
4. Compute SHAP values → top 3 contributing features
5. Return { risk_score, is_flagged, reasons[], model_version }
6. Persist prediction to DB
```

---

## API Contract

### Score a transaction
```
POST /score
Content-Type: application/json

Request:
{
  "transaction_id": "TXN-20240315-001",
  "sender_phone": "078XXXXXXX",
  "receiver_phone": "073XXXXXXX",
  "amount_rwf": 150000,
  "transaction_type": "TRANSFER",
  "timestamp": "2024-03-15T23:41:00Z"
}

Response 200:
{
  "transaction_id": "TXN-20240315-001",
  "risk_score": 0.87,
  "is_flagged": true,
  "risk_level": "HIGH",
  "reasons": [
    "3rd transaction in last 10 minutes from this account",
    "Amount is 94% of available balance",
    "Destination account has no prior transaction history"
  ],
  "model_version": "xgboost_v2",
  "scored_at": "2024-03-15T23:41:00.123Z"
}
```

### Analyst feedback (trains future model)
```
POST /feedback
{
  "transaction_id": "TXN-20240315-001",
  "analyst_label": "FALSE_POSITIVE",  // or "CONFIRMED_FRAUD"
  "note": "Known business account, high volume is normal"
}
```

### Health check
```
GET /health
→ { "status": "ok", "model_version": "xgboost_v2", "db": "connected" }
```

---

## Testing Strategy

### Unit tests (`tests/unit/`)
```
test_features.py
  ✓ balance_diff_orig is 0 for clean transaction
  ✓ amount_vs_balance correctly computes ratio
  ✓ log_amount handles zero-amount transaction
  ✓ is_weekend returns True for Saturday timestamp

test_scorer.py
  ✓ score is between 0 and 1
  ✓ returns exactly 3 reasons
  ✓ model version is included in response
  ✓ identical transactions produce identical scores (deterministic)

test_schemas.py
  ✓ rejects negative amounts
  ✓ rejects malformed phone numbers
  ✓ rejects future timestamps
```

### Integration tests (`tests/integration/`)
```
test_score_endpoint.py
  ✓ POST /score returns 200 with valid payload
  ✓ POST /score returns 422 with missing fields
  ✓ high-risk transaction payload returns is_flagged=True
  ✓ prediction is persisted to DB

test_feedback_endpoint.py
  ✓ POST /feedback updates transaction label in DB
  ✓ POST /feedback returns 404 for unknown transaction_id
```

### Performance test (`tests/performance/locustfile.py`)
```python
class FraudScoringUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task
    def score_transaction(self):
        self.client.post("/score", json=sample_payload())
```
Target: **p95 latency < 200ms at 100 req/s** (run: `locust -f locustfile.py --headless -u 100 -r 10`)

### Model quality gate (run in CI after training)
```python
# scripts/evaluate_model.py — exits with code 1 if gates fail
assert precision >= 0.85, f"Precision {precision:.3f} below threshold"
assert recall >= 0.75,    f"Recall {recall:.3f} below threshold"
assert auroc >= 0.90,     f"AUROC {auroc:.3f} below threshold"
```

---

## Docker Setup

### `docker-compose.yml`
```yaml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: momoguard
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models     # mount trained model artifacts
      - ./mlruns:/app/mlruns
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/momoguard
      MODEL_PATH: models/xgboost_fraud_v1.pkl
    depends_on:
      - postgres
    command: uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
```

### `Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root --no-dev

COPY . .
RUN poetry install --no-dev

EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## CI/CD Pipeline

### `.github/workflows/ci.yml`
```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: momoguard_test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready --health-interval 10s --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install poetry && poetry install
      - run: poetry run ruff check src/ tests/
      - run: poetry run pytest tests/unit tests/integration -v
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/momoguard_test

  model-quality-gate:
    runs-on: ubuntu-latest
    needs: lint-and-test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install poetry && poetry install
      - name: Download PaySim sample
        run: python scripts/download_sample.py   # downloads 10% sample for CI speed
      - name: Train + evaluate
        run: poetry run python scripts/train.py --ci
      - name: Check quality gates
        run: poetry run python scripts/evaluate_model.py
```

---

## Deployment

### API → Render.com (free tier)
1. Connect GitHub repo
2. Set service type: Web Service, runtime: Docker
3. Add env vars from `.env.example`
4. Start command: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

### Dashboard → Hugging Face Spaces (free)
- React build deployed as a static Space
- Connects to Render API URL
- Free, public, shareable — perfect for portfolio

### Resulting live URLs
```
https://momoguard-api.onrender.com
https://huggingface.co/spaces/yourname/momoguard-dashboard

# Auto-generated API docs (FastAPI built-in):
https://momoguard-api.onrender.com/docs
```

---

## Monitoring & Model Drift

### Evidently AI (open-source, free)
```python
# src/monitoring/drift_report.py
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=train_df, current_data=last_week_predictions_df)
report.save_html("drift_report.html")
```

### Weekly drift check (automated)
- APScheduler runs every Monday at 6am Kigali time
- Compares last week's transaction feature distributions vs training baseline
- Flags if drift detected in > 2 features
- Logs alert to Sentry if triggered

### Feedback loop → retraining
1. Analyst marks predictions as `FALSE_POSITIVE` or `CONFIRMED_FRAUD` via `/feedback`
2. Every 4 weeks: `python scripts/retrain.py` pulls feedback labels + new transactions
3. Retrained model must pass quality gates before replacing production model
4. MLflow tracks model lineage (v1 → v2 → v3)

---

## Version Roadmap

### v1.0 (Summer MVP)
- [x] PaySim data pipeline + feature engineering
- [x] XGBoost classifier + SHAP explanations
- [x] FastAPI scoring endpoint with Pydantic validation
- [x] Analyst feedback endpoint
- [x] React dashboard: live score feed, feature importance chart
- [x] All tests passing + quality gate in CI

### v1.1
- [ ] Rule-based pre-filters (block known bad actors instantly before ML)
- [ ] Score distribution dashboard with Evidently drift alerts

### v2.0
- [ ] Replace XGBoost with LightGBM ensemble
- [ ] Add graph features (transaction network — known fraud ring detection)
- [ ] Real-time stream processing with Kafka (producer/consumer demo)

---

## Week-by-Week Build Plan

| Week | Focus | Deliverables |
|------|-------|-------------|
| 1 | Data | Download PaySim, EDA notebook, feature engineering pipeline, unit tests |
| 2 | Model | XGBoost training, MLflow tracking, SHAP, quality gate script |
| 3 | API | FastAPI app, /score endpoint, DB persistence, integration tests |
| 4 | API | /feedback endpoint, currency service, Docker Compose running |
| 5 | Dashboard | React dashboard: score feed, feature importance, fraud news panel |
| 6 | Deploy + Monitor | Render deploy, Evidently drift report, CI/CD pipeline, load test |
