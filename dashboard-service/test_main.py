from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Dashboard Microservice" in response.text

def test_metricas():
    response = client.get("/metricas")
    assert response.status_code == 200
    assert "estudiantes_activos" in response.json()