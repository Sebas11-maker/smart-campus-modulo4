from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert "Academic Risk Microservice" in response.text

def test_riesgo_alto():
    response = client.get("/evaluar/2")

    assert response.status_code == 200

    data = response.json()

    assert data["nivel_riesgo"] == "ALTO"

def test_riesgo_bajo():
    response = client.get("/evaluar/3")

    assert response.status_code == 200

    data = response.json()

    assert data["nivel_riesgo"] == "BAJO"