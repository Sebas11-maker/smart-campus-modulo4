from fastapi.testclient import TestClient
from main import app

cliente_prueba = TestClient(app)


def test_verificar_estado():
    respuesta = cliente_prueba.get("/")
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "Activo"

# --- PRUEBAS FUNCIONALES ---
# Valida la lógica del negocio simulando un caso de Riesgo Alto (ID par)
def test_evaluar_riesgo_alto():
    respuesta = cliente_prueba.get("/evaluar/44")
    assert respuesta.status_code == 200
    assert respuesta.json()["nivel_riesgo"] == "ALTO"

# Valida la lógica del negocio simulando un caso de Riesgo Bajo (ID impar)
def test_evaluar_riesgo_bajo():
    respuesta = cliente_prueba.get("/evaluar/33")
    assert respuesta.status_code == 200
    assert respuesta.json()["nivel_riesgo"] == "BAJO"