from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse


app = FastAPI(title="Servicio de Notificaciones UCE")


class RequestNotificacion(BaseModel):
    estudiante_id: int
    mensaje: str
    canal: str  

@app.get("/", response_class=HTMLResponse)
async def frontend_notifications():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Smart Campus - Notification Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-blue-500/30 max-w-md w-full text-center">
            <div class="inline-flex p-3 bg-blue-500/10 rounded-full text-blue-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg>
            </div>
            <h1 class="text-2xl font-bold mb-2">Notification Microservice</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Procesamiento Asíncrono Reactivo (Kafka Event-Driven)</p>
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200">
                    Ver API Swagger Interactiva
                </button>
                <div class="p-3 bg-slate-900/50 rounded-xl text-left border border-slate-700 text-center">
                    <span class="text-xs text-emerald-400 font-mono font-bold">● Consumidor Worker Activo (Alta Disponibilidad)</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/enviar")
def enviar_notificacion(payload: RequestNotificacion):
    
    print(f"[LOG NOTIFICACIÓN] Enviando alerta al estudiante {payload.estudiante_id} por el canal {payload.canal}")
    
    return {
        "despachado": True,
        "canal_utilizado": payload.canal.upper(),
        "estudiante_id": payload.estudiante_id,
        "confirmacion": "Mensaje encolado y enviado exitosamente a los servidores de la UCE."
    }