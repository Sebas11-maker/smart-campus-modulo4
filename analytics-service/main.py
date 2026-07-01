import os
import logging
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [ANALYTICS-QUERY] - %(message)s')
logger = logging.getLogger(__name__)

ENV = os.getenv("ENV", "development")
root = "/analytics" if ENV == "production" else ""

app = FastAPI(title="Analytics Service - UCE", root_path=root, docs_url="/docs")

VISTA_COMPACTA_RIESGOS = [
    {"estudiante_id": 1, "riesgo": "BAJO", "facultad": "Ingeniería"},
    {"estudiante_id": 2, "riesgo": "ALTO", "facultad": "Ingeniería"},
    {"estudiante_id": 3, "riesgo": "BAJO", "facultad": "Medicina"}
]

@app.get("/", response_class=HTMLResponse)
async def frontend_analytics():
    return """
    <!DOCTYPE html>
    <html>
    <head><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-900 text-white flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl text-center max-w-md w-full border border-teal-500/20">
            <h1 class="text-2xl font-bold mb-2 text-teal-400">Analytics CQRS Query Service</h1>
            <p class="text-sm text-slate-400 mb-6">Módulo 4 - Proyecciones y Lecturas de Solo Escritura Desnormalizadas</p>
            <button onclick="window.location.href='/docs'" class="w-full bg-teal-600 hover:bg-teal-500 py-2 rounded-xl font-semibold">Ver Swagger</button>
        </div>
    </body>
    </html>
    """

@app.get("/proyecciones/alertas", tags=["CQRS Read Stack"])
def obtener_proyeccion_alertas_masivas():
    logger.info("[CQRS Read Query] Despachando consulta optimizada sobre vista desnormalizada NoSQL.")
    return {
        "stack_mode": "CQRS-Read-Only",
        "data_cached": True,
        "registros": VISTA_COMPACTA_RIESGOS
    }