from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert "Tracking Microservice" in response.text

def test_rastrear():
    payload = {
        "activo_id": "ACT-001",
        "latitud": -0.22985,
        "longitud": -78.52495,
        "responsable_id": 100
    }

    response = client.post("/rastrear", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["rastreado"] is True
    assert data["activo_id"] == "ACT-001"