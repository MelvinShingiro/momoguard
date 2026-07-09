from fastapi import APIRouter, HTTPException, status

from src.api.schemas.feedback import FeedbackRequest
from src.api.schemas.score_response import ApiMessage

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", responses={501: {"model": ApiMessage}})
def submit_feedback(payload: FeedbackRequest) -> None:
    # TODO: Use `payload` once you define how analyst feedback is stored.
    # TODO: Persist analyst feedback once the database layer exists.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Feedback persistence is intentionally left for you to implement.",
    )
