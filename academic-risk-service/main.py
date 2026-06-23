import os  
import json
import pika
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

ENV = os.getenv("ENV", "development")
root = "/risk" if ENV == "production" else ""

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

app = FastAPI(
    title="Servicio de Riesgo Académico UCE",
    root_path=root,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

def enviar_evento_alerta(evento: dict):
    """Envía un mensaje de alerta a la cola de RabbitMQ"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        
        channel.queue_declare(queue='alertas_riesgo', durable=True)
        
        channel.basic_publish(
            exchange='',
            routing_key='alertas_riesgo',
            body=json.dumps(evento),
            properties=pika.BasicProperties(
                delivery_mode=2, # Hace que el mensaje sea persistente
            )
        )
        connection.close()
        print(f" [x] Evento enviado exitosamente: {evento}")
    except Exception as e:
        print(f" [!] Error conectando a RabbitMQ: {e}")

@app.get("/", response_class=HTMLResponse)
async def frontend_risk():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Campus - Academic Risk Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen m-0">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-red-500/30 max-w-md w-full text-center mx-4">
            <div class="inline-flex p-3 bg-red-500/10 rounded-full text-red-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
            </div>
            <h1 class="text-2xl font-bold mb-2">Academic Risk Microservice</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Evaluación de Riesgo Estudiantil (CQRS / Hexagonal)</p>
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-red-600 hover:bg-red-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200 shadow-lg shadow-red-950/50">
                    Ver API Swagger Interactiva
                </button>
                <div class="p-3 bg-slate-900/50 rounded-xl border border-slate-700 text-center">
                    <span class="text-xs text-emerald-400 font-mono font-bold">● Broker asíncrono RabbitMQ integrado</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/evaluar/{estudiante_id}")
def evaluar_riesgo(estudiante_id: int):
    if estudiante_id % 2 == 0:
        respuesta = {
            "estudiante_id": estudiante_id,
            "nivel_riesgo": "ALTO",
            "motivo": "El estudiante registra un promedio proyectado inferior a 7.0/10 en el módulo académico."
        }
        enviar_evento_alerta(respuesta)
        return respuesta
    
    return {
        "estudiante_id": estudiante_id,
        "nivel_riesgo": "BAJO",
        "motivo": "Rendimiento dentro de los parámetros normales estables."
    }