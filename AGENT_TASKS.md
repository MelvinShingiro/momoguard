# AGENT_TASKS

This file defines the boundary between scaffolded project setup and the learning-heavy work you want to implement yourself.

## Completed By Setup

- Created the FastAPI application shell and route registration.
- Added a working `GET /health` endpoint.
- Added placeholder `POST /score` and `POST /feedback` endpoints that return `501 Not Implemented`.
- Added package metadata, development dependencies, Docker files, tests, scripts, and data folders.
- Added TODO-oriented placeholder modules for data, model, API service, and database layers.

## Reserved For You

- PaySim ingestion and validation logic.
- Feature engineering and online feature parity.
- Model training, evaluation, explainability, and artifact versioning.
- Real scoring logic for `POST /score`.
- Database models, sessions, and CRUD implementation.
- Analyst feedback persistence and retraining loop.
- Dashboard UI and analytics features.

## Suggested Order

1. Implement request/response schemas you want to lock in first.
2. Implement offline data loading and feature engineering in `src/data/`.
3. Train a first baseline model in `scripts/train.py` and `src/models/`.
4. Implement inference wiring in `src/api/services/scorer.py`.
5. Replace `501` behavior in `src/api/routers/score.py`.
6. Add persistence and feedback flow in `src/api/db/` and `src/api/routers/feedback.py`.
