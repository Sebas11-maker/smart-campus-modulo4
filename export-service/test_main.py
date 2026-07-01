from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Export Microservice" in response.text

def test_solicitar():
    response = client.post("/solicitar", json={"tipo_formato": "excel", "dataset_id": "fac_01"})
    assert response.status_code == 200
    assert response.json()["tarea_encolada"] is True