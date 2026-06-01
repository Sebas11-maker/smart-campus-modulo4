from fastapi.testclient import TestClient
from main import app

cliente_prueba = TestClient(app)

def test_verificar_estado():
    respuesta = cliente_prueba.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "Activo"

def test_enviar_notificacion_exitosa():
    data_simulada = {
        "estudiante_id": 24,
        "mensaje": "Alerta: Registra riesgo académico alto en el sistema.",
        "canal": "CORREO"
    }
    respuesta = cliente_prueba.post("/enviar", json=data_simulada)
    
    assert respuesta.status_code == 200
    assert respuesta.json()["despachado"] is True
    assert respuesta.json()["canal_utilizado"] == "CORREO"