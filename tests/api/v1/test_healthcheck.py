from fastapi.testclient import TestClient
from rag_chat_backend.main import app

client = TestClient(app)


def test_healthcheck_success():
    response = client.get("/api/v1/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"success": True}
