from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Report Microservice" in response.text

def test_generar_reporte():
    payload = {"facultad_id": 1, "periodo": "2026-2026"}
    response = client.post("/generar", json=payload)
    assert response.status_code == 200
    assert response.json()["estado"] == "COMPLETADO"