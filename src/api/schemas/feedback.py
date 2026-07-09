from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class AnalystLabel(str, Enum):
    FALSE_POSITIVE = "FALSE_POSITIVE"
    CONFIRMED_FRAUD = "CONFIRMED_FRAUD"
    BENIGN = "BENIGN"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class FeedbackRequest(BaseModel):
    """Validated input contract for `POST /feedback`."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "transaction_id": "TXN-20240315-001",
                "analyst_label": "FALSE_POSITIVE",
                "note": "Known business account, high volume is expected.",
            }
        },
    )

    transaction_id: str = Field(min_length=3, max_length=64)
    analyst_label: AnalystLabel
    note: str | None = Field(default=None, max_length=1000)


class FeedbackResponse(BaseModel):
    """Target response contract for a fully implemented feedback endpoint."""

    model_config = ConfigDict(extra="forbid")

    transaction_id: str
    analyst_label: AnalystLabel
    recorded_at: datetime
    detail: str
