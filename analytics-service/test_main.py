from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Analytics Microservice" in response.text

def test_prediccion():
    response = client.get("/prediccion/455")
    assert response.status_code == 200
    assert response.json()["estado_alerta"] == "BAJO"