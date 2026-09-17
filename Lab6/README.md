# Caso de Estudio #5 — Lea$e (again)

Arquitectura de Software — UTEC — 2026-II · 20 puntos (Reliability)

## Equipo

Grupo 03

| Integrantes |
| --- |
| Manyory Cueva |
| Jean Pier Angeles |
| Gonzalo Rodriguez |

## Parte 1 — Propuesta individual

Se eligió el happy path de **compra financiada con entrega conforme**. Una
empresa con RUC activo y habido solicita insumos disponibles; Lea$e valida la
operación, obtiene las aprobaciones internas, registra la aceptación del
contrato, activa la orden y cierra el caso cuando el cliente confirma la
entrega sin observaciones dentro de 48 horas.

Por indicación del docente, el dibujo utiliza solamente nombres de roles; no se
crean personas ficticias.

## Entregable principal

[Abrir arquitectura básica en Excalidraw](Diagrams/parte1-arquitectura-basica.excalidraw)

El lienzo presenta un diseño **top-down** en una sola vista:

- Los roles: Empresa cliente, Gerente de Ventas, Gerente de Logística y
  Gerente de Finanzas.
- La Iteración 1 muestra actores y `Lea$e App` sin detalle interno.
- La Iteración 2 abre login, seguridad, registro y validación de la empresa.
- La Iteración 3 abre solicitud, disponibilidad, capacidad financiera,
  ranking y preaprobación.
- La Iteración 4 abre aprobaciones, contrato, orden, entrega y conformidad.
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
- El límite de la Parte 1: una instancia, una base e integraciones síncronas,
  todavía sin balanceador, réplicas, colas, reintentos, circuit breaker o
  failover.

## Material de apoyo

| Documento | Propósito |
| --- | --- |
| [Happy path](4-Arquitectura/HappyPath.md) | Explica los pasos, estados y cobertura del recorrido dibujado. |
| [Arquitectura](4-Arquitectura/Architecture.md) | Sustenta los componentes y los límites de la propuesta sin escalar. |
| [Generador del dibujo](Diagrams/generadores/gen_parte1.ps1) | Permite regenerar el archivo editable. |

## Estructura

```text
Lab6/
├── README.md
├── 4-Arquitectura/
│   ├── HappyPath.md
│   └── Architecture.md
└── Diagrams/
    ├── parte1-arquitectura-basica.excalidraw
    └── generadores/
        ├── gen_parte1.ps1
        └── gen_parte1.source.ps1
```

## Decisión base

La Parte 1 usa un **monolito modular** en una sola instancia, una base de datos
relacional, almacenamiento privado de documentos e integraciones síncronas.
Es la línea base que el grupo podrá consensuar en la Parte 2 y escalar con
patrones de confiabilidad en la Parte 3.
