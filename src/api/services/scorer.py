"""Scoring service placeholder."""


def score_transaction_payload(payload: object) -> None:
    """Run fraud scoring for a transaction payload.

    TODO:
    - Load the trained model artifact.
    - Build online features that match offline training features.
    - Compute a risk score and explanation reasons.
    - Return a typed response object once schemas are defined.
    """

    raise NotImplementedError("Implement fraud scoring in this service.")
