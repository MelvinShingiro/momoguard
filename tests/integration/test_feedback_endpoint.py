from tests.conftest import create_test_client


def test_feedback_endpoint_validates_payload_then_returns_stub_response() -> None:
    client = create_test_client()

    response = client.post(
        "/feedback",
        json={
            "transaction_id": "TXN-001",
            "analyst_label": "FALSE_POSITIVE",
            "note": "Known customer behavior.",
        },
    )

    assert response.status_code == 501


def test_feedback_endpoint_rejects_invalid_label() -> None:
    client = create_test_client()

    response = client.post(
        "/feedback",
        json={
            "transaction_id": "TXN-001",
            "analyst_label": "WRONG_VALUE",
            "note": "This should fail schema validation.",
        },
    )

    assert response.status_code == 422
