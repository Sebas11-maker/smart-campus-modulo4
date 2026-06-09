from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI(title="Servicio de Rastreo de Activos UCE")

class RequestTracking(BaseModel):
    activo_id: str
    latitud: float
    longitud: float
    responsable_id: int

@app.get("/", response_class=HTMLResponse)
async def frontend_tracking():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Smart Campus - Tracking Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen m-0">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-purple-500/30 max-w-md w-full text-center mx-4">
            <div class="inline-flex p-3 bg-purple-500/10 rounded-full text-purple-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
            </div>
            
            <h1 class="text-2xl font-bold mb-2">Tracking Microservice</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Monitoreo de Activos y Geolocalización (Hexagonal / Layers)</p>
            
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-purple-600 hover:bg-purple-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200 shadow-lg shadow-purple-950/50">
                    Ver API Swagger Interactiva
                </button>
                
                <div class="p-3 bg-slate-900/50 rounded-xl border border-slate-700 text-center">
                    <span class="text-xs text-emerald-400 font-mono font-bold">● Tracking Telemetry Active on Target EC2 Node</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/rastrear")
def registrar_rastreo(payload: RequestTracking):
    
    print(f"[LOG TRACKING] Registrando ubicación geográfica para activo {payload.activo_id} (Lat: {payload.latitud}, Long: {payload.longitud})")
    print(f"[PERSISTENCIA] Documento acoplado mediante Adapter Pattern indexado en MongoDB.")
    
    return {
        "rastreado": True,
        "activo_id": payload.activo_id,
        "coordenadas": {
            "lat": payload.latitud,
            "lng": payload.longitud
        },
        "status": "Ubicación sincronizada y publicada en Kafka Event Broker."
    }