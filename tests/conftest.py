from fastapi.testclient import TestClient

from src.api.main import app


def create_test_client() -> TestClient:
    return TestClient(app)
