from fastapi import FastAPI

app = FastAPI(title="Servicio de Riesgo Académico UCE")

@app.get("/")
def verificar_estado():
    return {
        "modulo": "Comunicación, Analítica y Reportes", 
        "servicio": "Academic Risk Service", 
        "estado": "Activo"
    }

@app.get("/evaluar/{estudiante_id}")
def evaluar_riesgo(estudiante_id: int):

    if estudiante_id % 2 == 0:
        return {
            "estudiante_id": estudiante_id,
            "nivel_riesgo": "ALTO",
            "motivo": "El estudiante registra un promedio proyectado inferior a 7.0/10 en el módulo académico."
        }
    
    return {
        "estudiante_id": estudiante_id,
        "nivel_riesgo": "BAJO",
        "motivo": "Rendimiento dentro de los parámetros normales estables."
    }