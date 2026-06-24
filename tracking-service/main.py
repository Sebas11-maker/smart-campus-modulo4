import os
import logging
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [TRACKING-SERVICE] - %(message)s')
logger = logging.getLogger(__name__)

ENV = os.getenv("ENV", "development")
root = "/tracking" if ENV == "production" else ""

app = FastAPI(title="Tracking Service - UCE", root_path=root, docs_url="/docs")

CIRCUIT_STATE = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
FAIL_COUNTER = 0

@app.get("/", response_class=HTMLResponse)
async def frontend_tracking():
    return f"""
    <!DOCTYPE html>
    <html>
    <head><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-900 text-white flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl text-center max-w-md w-full border border-amber-500/20">
            <h1 class="text-2xl font-bold mb-2 text-amber-400">Tracking & Resiliency Service</h1>
            <p class="text-sm text-slate-400 mb-6">Módulo 4 - Monitoreo Elástico de Posición Física</p>
            <div class="p-3 bg-slate-900 rounded-xl font-mono text-xs mb-4">
                Estado del Circuit Breaker: <span class="font-bold text-emerald-400">{CIRCUIT_STATE}</span>
            </div>
            <button onclick="window.location.href='/docs'" class="w-full bg-amber-600 hover:bg-amber-500 py-2 rounded-xl font-semibold">Ver Swagger</button>
        </div>
    </body>
    </html>
    """

@app.get("/localizar/{estudiante_id}", tags=["Resiliency / Circuit Breaker"])
def localizar_dispositivo_estudiante(estudiante_id: int):
    global CIRCUIT_STATE, FAIL_COUNTER
    logger.info(f"Petición de localización para estudiante ID {estudiante_id}. Estado actual del breaker: {CIRCUIT_STATE}")

    if CIRCUIT_STATE == "OPEN":
        logger.warning("Circuit Breaker activo [OPEN]. Bloqueando petición por seguridad (Fail-Fast).")
        raise HTTPException(status_code=503, detail="Servicio degradado temporalmente. Circuit Breaker bloqueó la llamada de red.")

    if random.random() < 0.4:
        FAIL_COUNTER += 1
        logger.error(f"Fallo de conexión intermitente. Contador de errores consecutivos: {FAIL_COUNTER}")
        if FAIL_COUNTER >= 3:
            CIRCUIT_STATE = "OPEN"
            logger.critical("🚨 ¡Límite de fallos superado! Cambiando estado del Circuit Breaker a OPEN")
        raise HTTPException(status_code=500, detail="Error de timeout de red al geolocalizar antena.")

    FAIL_COUNTER = 0
    CIRCUIT_STATE = "CLOSED"
    return {
        "estudiante_id": estudiante_id,
        "campus_zona": "Biblioteca General - UCE",
        "coordenadas": "0.1982° S, 78.5042° W",
        "circuit_breaker": "CLOSED"
    }