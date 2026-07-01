from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
        response = client.get("/")
        assert response.status_code == 200
        assert "Security Microservice" in response.text or "Security Gateway" in response.text

def test_validar():
        response = client.post("/validar", json={"token": "valid_test_token"})
        assert response.status_code == 200
        assert response.json()["valido"] is True