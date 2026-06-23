import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

ENV = os.getenv("ENV", "development")
root = "/analytics" if ENV == "production" else ""

app = FastAPI(
    title="Servicio Analítico UCE",
    root_path=root,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

@app.get("/", response_class=HTMLResponse)
async def frontend_analytics():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Smart Campus - Analytics Platform</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-violet-500/30 max-w-md w-full text-center">
            <div class="inline-flex p-3 bg-violet-500/10 rounded-full text-violet-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
            </div>
            <h1 class="text-2xl font-bold mb-2">Analytics Microservice</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Procesamiento Estadístico Avanzado de Datos Históricos</p>
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-violet-600 hover:bg-violet-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200">
                    Ver API Swagger Interactiva
                </button>
                <div class="p-3 bg-slate-900/50 rounded-xl text-center border border-slate-700">
                    <span class="text-xs text-violet-400 font-mono font-bold">● Motor OLAP / Consultas de Red Académica</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/prediccion/{estudiante_id}")
def predecir_desercion(estudiante_id: int):
    return {
        "estudiante_id": estudiante_id,
        "probabilidad_aprobacion": 0.88,
        "estado_alerta": "BAJO"
    }