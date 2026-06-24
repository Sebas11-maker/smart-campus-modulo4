from locust import HttpUser, task, between

class RendimientoSmartCampus(HttpUser):
    wait_time = between(1, 3) # Simula retraso humano de 1 a 3 segundos

    @task(2)
    def consultar_riesgos_cqrs(self):
        """Simula lectura masiva en el Query Stack (CQRS Read)"""
        self.client.get("/analytics/riesgos")

    @task(1)
    def ejecutar_evaluacion_command(self):
        """Simula escritura masiva disparando comandos e hilos de RabbitMQ"""
        self.client.post("/risk/evaluar", json={
            "estudiante_id": 99,
            "promedio": 5.4
        })