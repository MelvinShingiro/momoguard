from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ScoreResponse(BaseModel):
    """Target response contract for a fully implemented scoring endpoint."""

    model_config = ConfigDict(extra="forbid")

    transaction_id: str = Field(min_length=3, max_length=64)
    risk_score: float = Field(ge=0, le=1)
    is_flagged: bool
    risk_level: RiskLevel
    reasons: list[str]
    model_version: str
    scored_at: datetime


class ApiMessage(BaseModel):
    """Small reusable response shape for scaffolded endpoints."""

    model_config = ConfigDict(extra="forbid")

    detail: str
