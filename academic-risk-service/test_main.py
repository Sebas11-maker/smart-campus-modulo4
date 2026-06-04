from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main_frontend_risk():
    response = client.get("/")
    assert response.status_code == 200
    assert "Academic Risk Microservice" in response.text