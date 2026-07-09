from fastapi import FastAPI

from src.api.config import settings
from src.api.routers import feedback, health, score

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Scaffolded API shell for the MomoGuard learning project.",
)

app.include_router(health.router)
app.include_router(score.router)
app.include_router(feedback.router)
