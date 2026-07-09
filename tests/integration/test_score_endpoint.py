from tests.conftest import create_test_client


def test_score_endpoint_validates_payload_then_returns_stub_response() -> None:
    client = create_test_client()

    response = client.post(
        "/score",
        json={
            "transaction_id": "TXN-001",
            "sender_phone": "0781234567",
            "receiver_phone": "0737654321",
            "amount_rwf": 150000,
            "transaction_type": "TRANSFER",
            "timestamp": "2024-03-15T23:41:00Z",
        },
    )

    assert response.status_code == 501


def test_score_endpoint_rejects_invalid_payload() -> None:
    client = create_test_client()

    response = client.post(
        "/score",
        json={
            "transaction_id": "TXN-001",
            "sender_phone": "078-123-4567",
            "receiver_phone": "0737654321",
            "amount_rwf": -10,
            "transaction_type": "TRANSFER",
            "timestamp": "2024-03-15T23:41:00Z",
        },
    )

    assert response.status_code == 422
