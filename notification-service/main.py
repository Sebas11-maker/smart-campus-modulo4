from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Servicio de Notificaciones UCE")


class RequestNotificacion(BaseModel):
    estudiante_id: int
    mensaje: str
    canal: str  

@app.get("/")
def verificar_estado():
    return {
        "modulo": "Comunicación, Analítica y Reportes",
        "servicio": "Notification Service",
        "estado": "Activo"
    }

@app.post("/enviar")
def enviar_notificacion(payload: RequestNotificacion):
    
    print(f"[LOG NOTIFICACIÓN] Enviando alerta al estudiante {payload.estudiante_id} por el canal {payload.canal}")
    
    return {
        "despachado": True,
        "canal_utilizado": payload.canal.upper(),
        "estudiante_id": payload.estudiante_id,
        "confirmacion": "Mensaje encolado y enviado exitosamente a los servidores de la UCE."
    }