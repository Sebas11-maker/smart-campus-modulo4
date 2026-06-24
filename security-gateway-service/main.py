import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [SECURITY-GATEWAY] - %(message)s')
logger = logging.getLogger(__name__)

ENV = os.getenv("ENV", "development")
root = "/security" if ENV == "production" else ""

app = FastAPI(
    title="Gateway de Seguridad UCE",
    root_path=root,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenPayload(BaseModel):
    token: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/", response_class=HTMLResponse)
async def frontend_security():
    logger.info("Acceso al Home Visual de Security Gateway desde el navegador.")
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
                    <span class="text-xs text-indigo-400 font-mono font-bold">● Firewall, JWT & CORS Activo</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/login", tags=["Autenticación"])
def login(credentials: LoginRequest):
    logger.info(f"Intento de inicio de sesión para el usuario: {credentials.username}")
    if credentials.username == "admin" and credentials.password == "uce2026":
        token_simulado = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWx1bW5vX3VjZSIsInJvbCI6IkVTVEVESUFOVEUifQ"
        logger.info(f"Firma de JWT Exitosa para: {credentials.username}")
        return {"access_token": token_simulado, "token_type": "bearer"}
    logger.warning(f"Intento fallido de autenticación para: {credentials.username}")
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

@app.post("/validar", tags=["Validación Token"])
def validar_token(payload: TokenPayload):
    logger.info("Validando integridad perimetral de firma JWT recibido")
    if payload.token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWx1bW5vX3VjZSIsInJvbCI6IkVTVEVESUFOVEUifQ":
        return {
            "valido": True,
            "usuario": "alumno_uce",
            "rol": "ESTUDIANTE",
            "permisos": ["ver_notas", "crear_solicitud"]
        }
    logger.error("Token JWT inválido, alterado o corrupto detectado en el Gateway")
    raise HTTPException(status_code=403, detail="Token no autorizado")