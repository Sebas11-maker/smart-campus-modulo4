import os
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [CHAT-WEBSOCKET] - %(message)s')
logger = logging.getLogger(__name__)

ENV = os.getenv("ENV", "development")
root = "/chat" if ENV == "production" else ""

app = FastAPI(title="Chat & Telemetry Service - UCE", root_path=root, docs_url="/docs")

@app.get("/", response_class=HTMLResponse)
async def frontend_chat():
    return """
    <!DOCTYPE html>
    <html>
    <head><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-slate-900 text-white flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl text-center max-w-md w-full border border-fuchsia-500/20">
            <h1 class="text-2xl font-bold mb-2 text-fuchsia-400">Chat & Telemetry Service</h1>
            <p class="text-sm text-slate-400 mb-6">Módulo 4 - Comunicación Full-Duplex Bi-Direccional NAtiva</p>
            <button onclick="window.location.href='/docs'" class="w-full bg-fuchsia-600 hover:bg-fuchsia-500 py-2 rounded-xl font-semibold">Ver Swagger</button>
        </div>
    </body>
    </html>
    """

@app.websocket("/telemetria/stream")
async def websocket_telemetria_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Conexión entrante establecida por Socket TCP de WebSocket.")
    try:
        while True:
            msg_cliente = await websocket.receive_text()
            logger.info(f"[Websocket Data Received] Trama de telemetría: {msg_cliente}")
            await websocket.send_text(f"Confirmación UCE M4 Servidor: Procesado '{msg_cliente}'")
    except WebSocketDisconnect:
        logger.warning("Canal de Websocket cerrado por el dispositivo cliente.")