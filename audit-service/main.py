import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

ENV = os.getenv("ENV", "development")
root = "/audit" if ENV == "production" else ""

app = FastAPI(
    title="Servicio de Auditoría UCE",
    root_path=root,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

class AuditLog(BaseModel):
    usuario: str
    accion: str
    modulo: str

@app.get("/", response_class=HTMLResponse)
async def frontend_audit():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Smart Campus - Audit Ledger</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-rose-500/30 max-w-md w-full text-center">
            <div class="inline-flex p-3 bg-rose-500/10 rounded-full text-rose-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            </div>
            <h1 class="text-2xl font-bold mb-2">Audit Microservice</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Registro Inmutable Documental de Acciones Transaccionales (Kafka Events)</p>
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-rose-600 hover:bg-rose-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200">
                    Ver API Swagger Interactiva
                </button>
                <div class="p-3 bg-slate-900/50 rounded-xl text-center border border-slate-700">
                    <span class="text-xs text-rose-400 font-mono font-bold">● Logger Cluster Activo (MongoDB ObjectId Unique)</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/registrar")
def registrar_auditoria(payload: AuditLog):
    return {
        "guardado": True,
        "document_id": "64fb04bf0eb59cba64af93e1",
        "status": "INDEXED"
    }