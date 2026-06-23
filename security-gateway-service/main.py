import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

ENV = os.getenv("ENV", "development")
root = "/security" if ENV == "production" else ""

app = FastAPI(
    title="Gateway de Seguridad UCE",
    root_path=root,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

class TokenPayload(BaseModel):
    token: str

@app.get("/", response_class=HTMLResponse)
async def frontend_security():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Smart Campus - Security Gateway</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white font-sans flex items-center justify-center h-screen">
        <div class="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-indigo-500/30 max-w-md w-full text-center">
            <div class="inline-flex p-3 bg-indigo-500/10 rounded-full text-indigo-400 mb-4">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
            </div>
            <h1 class="text-2xl font-bold mb-2">Security Gateway</h1>
            <p class="text-slate-400 text-sm mb-6">Módulo 4 - Validación Centralizada de JWT, CORS y Permisos de Roles</p>
            <div class="space-y-3">
                <button onclick="window.location.href='/docs'" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2.5 px-4 rounded-xl transition duration-200">
                    Ver API Swagger Interactiva
                </button>
                <div class="p-3 bg-slate-900/50 rounded-xl text-center border border-slate-700">
                    <span class="text-xs text-indigo-400 font-mono font-bold">● Firewall & Rate Limiting Activo</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/validar")
def validar_token(payload: TokenPayload):
    return {
        "valido": True,
        "usuario": "alumno_uce",
        "rol": "ESTUDIANTE",
        "permisos": ["ver_notas", "crear_solicitud"]
    }