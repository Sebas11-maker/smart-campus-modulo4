# Tracking Microservice - Smart Campus

## Patrón de Diseño Arquitectónico
Este microservicio implementa **Arquitectura Hexagonal (Puertos y Adaptadores)** combinada con **Event-Driven Architecture (EDA)**.

* **Dominio:** Lógica pura de rastreo de activos del campus.
* **Puertos de Entrada:** Controladores REST API.
* **Puertos de Salida (Adaptadores):** Capa de persistencia políglota acoplada a MongoDB y mensajería asíncrona mediante un productor/consumidor de **Kafka**.

## Endpoints Expuestos (Contracts)
* `GET /api/v1/tracking/health` -> Validación de Alta Disponibilidad del servicio.
* `POST /api/v1/tracking/routes` -> Registro de telemetría de activos protegidos por firma de JWT verificada.

## DockerHub Strategy
* **QA Target:** `xaandrade/tracking-service:qa-latest`
* **PROD Target:** `xaandrade/tracking-service:prod-latest`