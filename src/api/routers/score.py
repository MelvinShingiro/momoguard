from fastapi import APIRouter, HTTPException, status

from src.api.schemas.score_response import ApiMessage
from src.api.schemas.transaction import ScoreRequest

router = APIRouter(prefix="/score", tags=["score"])


@router.post("", responses={501: {"model": ApiMessage}})
def score_transaction(payload: ScoreRequest) -> None:
    # TODO: Use `payload` to build online features once inference is implemented.
    # TODO: Call the scoring service after implementing feature engineering and model inference.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Scoring logic is intentionally left for you to implement.",
    )
