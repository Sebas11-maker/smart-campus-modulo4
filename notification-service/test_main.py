from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert "Notification Microservice" in response.text

def test_enviar_notificacion():
    payload = {
        "estudiante_id": 123,
        "mensaje": "Prueba QA",
        "canal": "email"
    }

    response = client.post("/enviar", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["despachado"] is True
    assert data["canal_utilizado"] == "EMAIL"