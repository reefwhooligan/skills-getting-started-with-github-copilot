import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Provide a TestClient with the FastAPI app instance."""
    return TestClient(app)
