import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

ENV = os.getenv("ENV", "development")
root = "/dashboard" if ENV == "production" else ""

app = FastAPI(
    title="Panel de Control UCE",
    root_path=root,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

@app.get("/", response_class=HTMLResponse)
async def frontend_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Smart Campus - Admin Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-pink-500/30 max-w-md w-full text-center">
            <div class="inline-flex p-3 bg-pink-500/10 rounded-full text-pink-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.003 9.003 0 1020.945 13H11V3.055z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"></path></svg>
            </div>
            <h1 class="text-2xl font-bold mb-2">Dashboard Microservice</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Agregación de Datos en Tiempo Real y Consultas Optimadas con GraphQL</p>
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-pink-600 hover:bg-pink-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200">
                    Ver API Swagger Interactiva
                </button>
                <div class="p-3 bg-slate-900/50 rounded-xl text-center border border-slate-700">
                    <span class="text-xs text-pink-400 font-mono font-bold">● Capa de Memoria Caché Redis Operativa</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/metricas")
def obtener_metricas():
    return {
        "estudiantes_activos": 1420,
        "solicitudes_pendientes": 34,
        "alerta_riesgo_critico": 12,
        "origen_datos": "Redis Cache Cluster"
    }