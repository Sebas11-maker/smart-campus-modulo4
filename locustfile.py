from locust import HttpUser, task, between

class RendimientoSmartCampus(HttpUser):
    host = "http://elb-uce-m4-prod-876695815.us-east-1.elb.amazonaws.com"
    wait_time = between(1, 3) # Simula retraso humano de 1 a 3 segundos

    @task(2)
    def consultar_riesgos_cqrs(self):
        """Simula lectura masiva en el Query Stack (CQRS Read Stack)"""
        self.client.get("/analytics/proyecciones/alertas")

    @task(1)
    def ejecutar_evaluacion_command(self):
        """Simula escritura masiva disparando comandos al Command Stack (CQRS Write Stack)"""
        self.client.post("/risk/command/evaluar", json={
            "estudiante_id": 2,
            "promedio": 5.4
        })