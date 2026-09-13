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
| Usuarios, actores y personas | [2-Personas/](2-Personas/README.md) | Listo |
| Requerimientos funcionales | [3-Requerimientos/Functional.md](3-Requerimientos/Functional.md) | Listo |
| Requerimientos no funcionales | [3-Requerimientos/NonFunctional.md](3-Requerimientos/NonFunctional.md) | Listo |
| Diagrama de arquitectura del harness (Excalidraw) | [Diagrams/diagramaLab5.excalidraw](Diagrams/diagramaLab5.excalidraw) | Listo |
| Agente evaluador de requerimientos y resultados | [5-Especificacion/](5-Especificacion/README.md) | Listo (iteración 1: 89.4%) |
| Documento de arquitectura con reliability y fault tolerance | 4-Arquitectura/ | Pendiente |

## Estructura

```
Lab5/
├── README.md
├── 1-Problema/
│   └── Problema.md            # Problema, alcance, supuestos, SPOF, puntos de decisión
├── 2-Personas/
│   ├── README.md              # Índice y cobertura por persona
│   ├── Usuarios.md            # Actores del diagrama y su alcance de acceso
│   ├── Camila.md              # Ingeniera de soporte
│   ├── Andres.md              # Ingeniero de desarrollo
│   ├── Paola.md               # Incident Manager
│   ├── Martin.md              # Data Science
│   └── Lucia.md               # Cliente (empresa)
├── 3-Requerimientos/
│   ├── Functional.md          # 37 FR trazados a componente del diagrama y PD
│   └── NonFunctional.md       # 28 NFR con umbral y verificación
├── 5-Especificacion/
│   ├── README.md              # Cómo ejecutar el agente evaluador
│   ├── Eval-Spec.md           # Agente evaluador (rúbrica y formato)
│   └── Results.md             # Resultado por iteración
└── Diagrams/
    └── diagramaLab5.excalidraw
```

## La decisión central

El LLM se trata como un **componente no confiable por diseño**: no determinista,
influenciable por el texto del incidente que lee y capaz de proponer acciones
equivocadas. La confiabilidad no se le pide al modelo, se construye alrededor de
él. De ahí salen las tres líneas del diseño, que el diagrama dibuja como
servicios del harness:

1. **El LLM propone, el harness ejecuta.** Orquestador de herramientas con
   catálogo por nivel de riesgo, vista previa de impacto, bloqueo de escritura
   hasta la aprobación del Incident Manager, permisos del ingeniero y deshacer
   acción. Cinco barreras, porque ninguna sola habría evitado el borrado.
2. **Ninguna afirmación sin dato vigente.** El estado se lee de BD1 y viaja con
   la hora del dato; las preguntas frecuentes salen de una caché que se invalida
   al cambiar el dato; varias respuestas del LLM se reducen a una por match
   determinístico; sin dato, abstención.
3. **La capacidad escasa se reparte, no se sortea.** El recurso crítico es la
   GPU del LLM local: el 60% de las consultas se resuelve sin modelo, el resto
   entra por una cola por prioridad (cliente > ingeniería), con cortacircuitos,
   modo degradado y descarte explícito por prioridad.

Los tres tipos de escalamiento no son un detalle de dominio: son la razón por la
que la cola tiene prioridades. Customer tiene SLA de un día; engineering, de
tres. Cuando la capacidad no alcanza, el sistema tiene que saber de antemano a
quién sacrificar.

## Orden de lectura

1. [Problema, SPOF y puntos de decisión](1-Problema/Problema.md)
2. [Actores y personas](2-Personas/README.md)
3. [Requerimientos funcionales](3-Requerimientos/Functional.md)
4. [Requerimientos no funcionales](3-Requerimientos/NonFunctional.md)
5. [Diagrama del harness](Diagrams/diagramaLab5.excalidraw)
6. [Evaluación de requerimientos](5-Especificacion/Results.md)
