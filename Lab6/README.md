# Caso de Estudio #5 — Lea$e (again)

Arquitectura de Software — UTEC — 2026-II · 20 puntos (Reliability)

## Equipo

Grupo 03

| Integrantes |
| --- |
| Manyory Cueva |
| Jean Pier Angeles |
| Gonzalo Rodriguez |

## Arquitectura top-down y confiabilidad

Se eligió el happy path de **compra financiada con entrega conforme**. Una
empresa con RUC activo y habido solicita insumos disponibles; Lea$e valida la
operación, obtiene las aprobaciones internas, registra la aceptación del
contrato, activa la orden y cierra el caso cuando el cliente confirma la
entrega sin observaciones dentro de 48 horas.

Por indicación del docente, el dibujo utiliza solamente nombres de roles; no se
crean personas ficticias.

## Entregable principal

[Abrir arquitectura top-down en Excalidraw](Diagrams/diagrama-top-down.excalidraw)

[Abrir arquitectura escalada con reliability en Excalidraw](Diagrams/diagrama-reliability.excalidraw)

El lienzo presenta un diseño **top-down** en una sola vista:

- Los roles: Empresa cliente, Gerente de Ventas, Gerente de Logística y
  Gerente de Finanzas.
- La Iteración 1 muestra actores y `Lea$e App` sin detalle interno.
- La Iteración 2 abre login, seguridad, registro y validación de la empresa.
- La Iteración 3 abre solicitud, disponibilidad, capacidad financiera,
  ranking y preaprobación.
- La Iteración 4 abre aprobaciones, contrato, orden, entrega y conformidad.
- La Iteración 5 consolida **todos los servicios end-to-end** en la línea base:
  acceso, registro, validación, solicitud, preaprobación, aprobaciones,
  contrato, orden, entrega, conformidad e incidencia. Todavía no escala.
- Componentes como `LoginService`, `RegisterCompanyService`,
  `LeaseRequestService`, `ContractService` y `DeliveryService`.
- Cada llamada a SUNAT, historial crediticio, proveedor y correo.
- Cada `READ`, `WRITE` y `UPDATE` en la base o almacenamiento documental.
- Un componente repetido entre iteraciones representa la misma dependencia a
  diferente nivel de detalle, no otra instancia.
- La secuencia explícita de aprobaciones: Ventas → Logística → Finanzas →
  contrato definitivo → aceptación del cliente.
- Las salidas cuando una validación o aprobación responde `NO`, incluida la
  apertura de una incidencia si la entrega no es conforme.
- Las iteraciones 1–4 muestran el descubrimiento progresivo; la Iteración 5
  reúne el diseño completo sin mezclar todavía los patrones de reliability.

El segundo lienzo parte de esa Iteración 5 y agrega `Load Balancer`, instancias
N+1, `Health Endpoints`, failover de datos, outbox, broker, workers,
idempotencia, retries con exponential backoff, tres circuit breakers,
bulkheads, degradación elegante, observabilidad y Chaos Engineering.

## Material de apoyo

| Documento | Propósito |
| --- | --- |
| [Happy path](4-Arquitectura/HappyPath.md) | Explica los pasos, estados y cobertura del recorrido dibujado. |
| [Arquitectura](4-Arquitectura/Architecture.md) | Sustenta la línea base y su evolución escalada. |
| [Generador de los dibujos](Diagrams/generadores/gen_parte1.ps1) | Regenera ambos archivos editables. |

## Estructura

```text
Lab6/
├── README.md
├── 4-Arquitectura/
│   ├── HappyPath.md
│   └── Architecture.md
└── Diagrams/
    ├── diagrama-top-down.excalidraw
    ├── diagrama-reliability.excalidraw
    └── generadores/
        ├── gen_parte1.ps1
        └── gen_parte1.source.ps1
```

## Decisión arquitectónica

La línea base usa un **monolito modular** y una base relacional. La versión
escalada conserva esos límites lógicos, pero ejecuta la aplicación en instancias
stateless N+1 detrás de un balanceador, agrega primary/standby/read replica con
failover y desacopla las notificaciones mediante outbox, broker y workers. Las
dependencias externas quedan aisladas por bulkhead y protegidas por timeout,
retry con exponential backoff y circuit breaker.
