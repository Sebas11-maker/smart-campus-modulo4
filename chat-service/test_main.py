from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
        response = client.get("/")
        assert response.status_code == 200
        assert "Chat Microservice" in response.text

def test_enviar_mensaje():
        payload = {"remitente_id": 1, "destinatario_id": 2, "contenido": "Hola Profesor"}
        response = client.post("/enviar", json=payload)
        assert response.status_code == 200
        assert response.json()["enviado"] is True