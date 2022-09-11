from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)


@pytest.fixture(autouse=True)
def init_test_enf(monkeypatch):
    monkeypatch.setenv("FAMT_SECRET_KEY", "TEST123")


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == "Hello world!"
