# Caso de Estudio #5 — Genius-x

Arquitectura de Software — UTEC — 2026-II · 20 ptos (Reliability)

Genius maneja los incidentes diarios de la compañía —*customer*, *engineering* y
*support escalations*— con un LLM local que además ejecuta acciones sobre
sistemas reales. El harness actual (API → LLM → MCP base de datos / MCP Slack)
dejó que el modelo borrara la base de datos, entrega estados vencidos, responde
distinto a la misma pregunta y se cae en el pico de la primera semana del mes.
Este laboratorio rediseña el harness alrededor del LLM con patrones de
confiabilidad y tolerancia a fallos.

## Entregables

| Entregable | Archivo | Estado |
| --- | --- | --- |
| Enunciado interpretado, alcance, supuestos, SPOF y puntos de decisión | [1-Problema/Problema.md](1-Problema/Problema.md) | Listo |
| Usuarios, roles y personas | [2-Personas/](2-Personas/) | Pendiente |
| Requerimientos funcionales | [3-Requerimientos/Functional.md](3-Requerimientos/Functional.md) | Listo |
| Requerimientos no funcionales | [3-Requerimientos/NonFunctional.md](3-Requerimientos/NonFunctional.md) | Listo |
| Arquitectura del harness con reliability y fault tolerance | [4-Arquitectura/](4-Arquitectura/) | Pendiente |
| Diagrama de arquitectura (Excalidraw) | [Diagrams/](Diagrams/) | Pendiente |
| Especificación y evaluación | [5-Especificacion/](5-Especificacion/) | Pendiente |

## La decisión central

El LLM se trata como un **componente no confiable por diseño**: no determinista,
influenciable por el texto del incidente que lee y capaz de proponer acciones
equivocadas. La confiabilidad no se le pide al modelo, se construye alrededor de
él. De ahí salen las tres líneas del diseño:

1. **El LLM propone, el harness ejecuta.** Catálogo de herramientas por nivel de
   riesgo, simulación previa, aprobación de una persona distinta del solicitante,
   privilegio mínimo por identidad y reversión declarada. Cuatro barreras, porque
   ninguna sola habría evitado el borrado.
2. **Ninguna afirmación sin evidencia vigente.** El estado se lee del sistema de
   registro y viaja con su versión; la caché se invalida por evento; sin
   evidencia el sistema se abstiene; las preguntas frecuentes tienen respuesta
   canónica reproducible.
3. **La capacidad escasa se reparte, no se sortea.** El recurso crítico es la
   GPU del LLM local: el 60% de las consultas se resuelve sin modelo, el resto
   entra por colas separadas por clase de SLA, con cortacircuitos, degradación a
   respuesta sin modelo y descarte explícito por prioridad.

Los tres tipos de escalamiento no son un detalle de dominio: son la razón por la
que hay tres colas. Customer tiene SLA de un día; engineering, de tres. Cuando la
capacidad no alcanza, el sistema tiene que saber de antemano a quién sacrificar.

## Orden de lectura

1. [Problema, SPOF y puntos de decisión](1-Problema/Problema.md)
2. [Requerimientos funcionales](3-Requerimientos/Functional.md)
3. [Requerimientos no funcionales](3-Requerimientos/NonFunctional.md)
