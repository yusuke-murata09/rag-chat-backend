from fastapi.testclient import TestClient
from unittest import TestCase
from rag_chat_backend.main import app

client = TestClient(app)

class TestHealthCheck(TestCase):

    def test_health_check_success(self):
        response = client.get("/api/v1/healthcheck")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"success": True})
