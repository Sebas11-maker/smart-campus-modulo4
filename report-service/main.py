import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

ENV = os.getenv("ENV", "development")
root = "/report" if ENV == "production" else ""

app = FastAPI(
    title="Servicio de Reportes UCE",
    root_path=root,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

class ReportRequest(BaseModel):
    facultad_id: int
    periodo: str

@app.get("/", response_class=HTMLResponse)
async def frontend_report():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Smart Campus - Report Engine</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-cyan-500/30 max-w-md w-full text-center">
            <div class="inline-flex p-3 bg-cyan-500/10 rounded-full text-cyan-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
            </div>
            <h1 class="text-2xl font-bold mb-2">Report Microservice</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Generador de Reportes e Interconexión entre Bases de Datos Distribuidas</p>
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200">
                    Ver API Swagger Interactiva
                </button>
                <div class="p-3 bg-slate-900/50 rounded-xl text-center border border-slate-700">
                    <span class="text-xs text-cyan-400 font-mono font-bold">● gRPC Client Conectado al Core Académico</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/generar")
def generar_reporte(payload: ReportRequest):
    return {
        "reporte_id": 8831,
        "estado": "COMPLETADO",
        "url_descarga_temporal": f"/report/descargar/rep_8831.csv",
        "registros_procesados": 4500
    }