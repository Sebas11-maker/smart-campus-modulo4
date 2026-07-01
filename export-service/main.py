import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

ENV = os.getenv("ENV", "development")
root = "/export" if ENV == "production" else ""

app = FastAPI(
    title="Servicio de Exportación UCE",
    root_path=root,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

class ExportRequest(BaseModel):
    tipo_formato: str
    dataset_id: str

@app.get("/", response_class=HTMLResponse)
async def frontend_export():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Smart Campus - Export Engine</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-orange-500/30 max-w-md w-full text-center">
            <div class="inline-flex p-3 bg-orange-500/10 rounded-full text-orange-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
            </div>
            <h1 class="text-2xl font-bold mb-2">Export Microservice</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Procesamiento en Segundo Plano de Reportes Pesados (RabbitMQ Workers)</p>
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-orange-600 hover:bg-orange-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200">
                    Ver API Swagger Interactiva
                </button>
                <div class="p-3 bg-slate-900/50 rounded-xl text-center border border-slate-700">
                    <span class="text-xs text-orange-400 font-mono font-bold">● Cola de Mensajería RabbitMQ Conectada</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/solicitar")
def solicitar_exportacion(payload: ExportRequest):
    return {
        "tarea_encolada": True,
        "task_id": "job_exp_9921a",
        "mensaje": f"Su archivo {payload.tipo_formato.upper()} se está procesando asíncronamente."
    }