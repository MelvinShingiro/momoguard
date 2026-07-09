from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TransactionType(str, Enum):
    CASH_IN = "CASH_IN"
    CASH_OUT = "CASH_OUT"
    DEBIT = "DEBIT"
    PAYMENT = "PAYMENT"
    TRANSFER = "TRANSFER"


class ScoreRequest(BaseModel):
    """Validated input contract for `POST /score`.

    Keep this model stable as you build the scoring pipeline behind it.
    """

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "transaction_id": "TXN-20240315-001",
                "sender_phone": "0781234567",
                "receiver_phone": "0737654321",
                "amount_rwf": 150000,
                "transaction_type": "TRANSFER",
                "timestamp": "2024-03-15T23:41:00Z",
            }
        },
    )

    transaction_id: str = Field(min_length=3, max_length=64)
    sender_phone: str = Field(min_length=10, max_length=15)
    receiver_phone: str = Field(min_length=10, max_length=15)
    amount_rwf: float = Field(gt=0)
    transaction_type: TransactionType
    timestamp: datetime

    @field_validator("sender_phone", "receiver_phone")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized.isdigit():
            raise ValueError("phone numbers must contain only digits")
        return normalized
