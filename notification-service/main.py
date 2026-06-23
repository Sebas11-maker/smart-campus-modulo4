import os
import json
import pika
import threading
from fastapi import FastAPI



from fastapi.responses import HTMLResponse
from pymongo import MongoClient
from datetime import datetime

ENV = os.getenv("ENV", "development")
root = "/notifications" if ENV == "production" else ""

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

app = FastAPI(
    title="Servicio de Notificaciones UCE",
    root_path=root
)

historial_notificaciones = []

def guardar_en_mongodb(data: dict):
    """Conecta e inserta la alerta en MongoDB usando el patrón Adapter seguro"""
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        db = client["smartcampus_db"]
        collection = db["alertas_historial"]
        
        documento = {
            "estudiante_id": data["estudiante_id"],
            "nivel_riesgo": data["nivel_riesgo"],
            "motivo": data["motivo"],
            "fecha_registro": datetime.utcnow().isoformat(),
            "origen": "RabbitMQ-Worker"
        }
        
        inspeccion_id = collection.insert_one(documento).inserted_id
        print(f" [💾 MongoDB] Alerta guardada exitosamente con ID: {inspeccion_id}")
        client.close()
    except Exception as mongo_err:
        print(f" [⚠️ Alerta DB] No se pudo persistir en MongoDB (Modo Degradado Activo): {mongo_err}")

def iniciar_worker_consumidor():
    """Ejecuta el loop de escucha asíncrona de RabbitMQ"""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue='alertas_riesgo', durable=True)

        def callback(ch, method, properties, body):
            print(f" [-->] Mensaje crudo recibido en worker: {body}")
            
            try:
                data = json.loads(body.decode())
                
                if "estudiante_id" not in data or "nivel_riesgo" not in data:
                    raise ValueError("Mensaje Malformado (Poison Pill detectada)")
                
                alerta_formateada = f"NOTIFICACIÓN ENVIADA: Alerta de riesgo {data['nivel_riesgo']} para el estudiante ID {data['estudiante_id']}."
                historial_notificaciones.append(alerta_formateada)
                print(f" [✓] Procesado exitosamente: {alerta_formateada}")
                
                guardar_en_mongodb(data)
                
            except (json.JSONDecodeError, ValueError) as err:
                print(f" [🪓 Poison Pill Descartada] Error procesando el mensaje: {err}")
            
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='alertas_riesgo', on_message_callback=callback)
        print(" [*] Worker de Notificaciones escuchando alertas_riesgo...")
        channel.start_consuming()
    except Exception as e:
        print(f" [!] Fallo crítico en el worker de RabbitMQ: {e}")

thread = threading.Thread(target=iniciar_worker_consumidor, daemon=True)
thread.start()

@app.get("/", response_class=HTMLResponse)
async def frontend_notifications():
    lista_html = "".join([f"<li class='p-2 bg-slate-700/50 rounded-lg border border-slate-600 mb-2 font-mono text-xs text-amber-300'>{n}</li>" for n in historial_notificaciones])
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Smart Campus - Notificaciones Worker</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white flex items-center justify-center h-screen m-0">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl max-w-lg w-full text-center mx-4 border border-slate-700">
            <h1 class="text-2xl font-bold mb-2 text-emerald-400">Notification Service Worker</h1>
            <p class="text-sm text-slate-400 mb-6">Eventos capturados asíncronamente desde RabbitMQ</p>
            <div class="p-4 bg-slate-900 rounded-xl h-48 overflow-y-auto border border-slate-700 text-left mb-4">
                <ul>{lista_html if lista_html else "<p class='text-slate-500 text-xs text-center pt-16'>Esperando eventos de Alerta...</p>"}</ul>
            </div>
            <div class="p-3 bg-slate-900/50 rounded-xl border border-slate-700/60 text-center">
                <span class="text-xs text-emerald-400 font-mono font-bold">● Persistencia políglota lista (MongoDB Adapter)</span>
            </div>
        </div>
    </body>
    </html>
    """



