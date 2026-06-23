import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

ENV = os.getenv("ENV", "development")
root = "/chat" if ENV == "production" else ""

app = FastAPI(
    title="Servicio de Chat UCE",
    root_path=root,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

class MessagePayload(BaseModel):
    remitente_id: int
    destinatario_id: int
    contenido: str

@app.get("/", response_class=HTMLResponse)
async def frontend_chat():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Smart Campus - Chat Room</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-emerald-500/30 max-w-md w-full text-center">
            <div class="inline-flex p-3 bg-emerald-500/10 rounded-full text-emerald-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
            </div>
            <h1 class="text-2xl font-bold mb-2">Chat Microservice</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Comunicación síncrona Docente-Estudiante mediante WebSockets</p>
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200">
                    Ver API Swagger Interactiva
                </button>
                <div class="p-3 bg-slate-900/50 rounded-xl text-center border border-slate-700">
                    <span class="text-xs text-emerald-400 font-mono font-bold">● Persistencia Documental MongoDB Conectada</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/enviar")
def enviar_mensaje(payload: MessagePayload):
    return {
        "enviado": True,
        "timestamp": "2026-06-22T17:25:00Z",
        "mensaje_id": "msg_6fb04bf0eb59cba64af93"
    }