from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Audit Microservice" in response.text

def test_registrar():
    payload = {"usuario": "admin", "accion": "crear_reporte", "modulo": "comunicaciones"}
    response = client.post("/registrar", json=payload)
    assert response.status_code == 200
    assert response.json()["guardado"] is True