# Caso de Estudio #4 — RemoteSchooly

Arquitectura de Software — UTEC — 2026-II

RemoteSchooly distribuye educación semanal a pueblos remotos del Perú y controla el uso de IA por parte de docentes. Los contenidos llegan por una conexión limitada e intermitente y las solicitudes a IA se preparan y gobiernan antes de consumir tokens.

## Entregables

| Entregable | Archivo |
| --- | --- |
| Enunciado interpretado, alcance y supuestos | [Problema.md](Problema.md) |
| Usuarios, roles y usuario modelo | [Usuarios.md](Usuarios.md) |
| Personas | [Personas/](Personas/) |
| Requerimientos funcionales | [Requirements/Functional.md](Requirements/Functional.md) |
| Requerimientos no funcionales | [Requirements/NonFunctional.md](Requirements/NonFunctional.md) |
| Especificación completa | [SPEC-TEMPLATE.md](SPEC-TEMPLATE.md) |
| Evaluación de requisitos | [Spec/Results.md](Spec/Results.md) |
| Diseño R.E.D.A.L.E. y happy paths | [Architecture.md](Architecture.md) |
| **Diagramas y enlaces de Excalidraw** | [Diagrams/](Diagrams/README.md) |
| Diagramas del problema 1: distribución, 36 casos | [Diagrams/Problema1/](Diagrams/Problema1/README.md) |
| Diagrama del problema 2: gasto de tokens, 18 casos | [Diagrams/Problema2/](Diagrams/Problema2/README.md) |
| Contexto: los 12 puntos de decisión y 34 peores casos | [Diagrams/Contexto/00-contexto-diagrama.md](Diagrams/Contexto/00-contexto-diagrama.md) |
| Enumeración de casos del punto de decisión del AI Gateway | [Diagrams/Contexto/01-decision-ai-gateway.md](Diagrams/Contexto/01-decision-ai-gateway.md) |
| Ejemplo de solicitud intermedia | [Examples/solicitud-ia.example.json](Examples/solicitud-ia.example.json) |

## Qué diagrama usar

Los enlaces de Excalidraw y el índice completo están en [Diagrams/](Diagrams/README.md).

**Para exponer, uno por problema.**

| Problema | Lienzo | Qué cuenta |
| --- | --- | --- |
| 1. Distribución con Internet intermitente | [Problema1/E-problema1-completo.excalidraw](Diagrams/Problema1/E-problema1-completo.excalidraw) | El recorrido entero de Valeria a Valeria, en diez escenas, con los 36 casos repartidos en el camino. |
| 2. Gasto excesivo de tokens | [Problema2/problema2.excalidraw](Diagrams/Problema2/problema2.excalidraw) | Ocho escenas donde cada paso descarta una razón para llamar al modelo. La llamada es lo último que queda. |

**Para responder una pregunta puntual del problema 1**, cada bloque tiene su propio lienzo con guion y tres iteraciones acumulativas.

| Lienzo | Bloque | Casos |
| --- | --- | ---: |
| `A-que-bajar` | ¿Qué archivos transferir? | 4 |
| `B-integridad-y-activacion` | ¿Puedo confiar en lo que llegó? | 11 |
| `C-retorno-idempotente` | Lo hecho sin red vuelve una sola vez | 7 |
| `D-cuando-sincronizar` | ¿Conviene sincronizar ahora? | 14 |

**Para sustentar el diseño**, el Top Down Design con tres iteraciones acumulativas está en [Contexto/02-topdown-remoteschooly-v2.excalidraw](Diagrams/Contexto/02-topdown-remoteschooly-v2.excalidraw). Cada iteración conserva la anterior: la primera plantea el sistema como una caja, la segunda abre la distribución offline-first, la tercera agrega la gobernanza de tokens con login y biblioteca de prompts.

## Decisión central

La central de Lima publica el contenido por Internet. En cada escuela, un **Nodo Escolar Local** sincroniza solo las diferencias mediante descargas segmentadas y reanudables; prioriza el material esencial y conserva la última versión válida durante un corte. Cuando la red vuelve, reanuda desde el último bloque verificado y confirma la instalación. No se usa transporte físico.

Se descarta el medio físico (SSD, USB, transportista). El enunciado no dice que la escuela esté sin Internet: dice que el Internet es limitado y se corta. Un SSD resolvería un problema que la escuela no tiene y agregaría custodia, viajes y una semana de retraso por cada error de empaquetado. «Offline» aquí significa que la clase no depende de la red en el momento en que ocurre, no que no exista red: el nodo local es el que responde.

Para IA, el docente no conversa directamente con el modelo. Primero completa una solicitud estructurada; un **AI Gateway** local valida que sea concreta, pide solo los datos faltantes y construye un prompt breve con el fragmento curricular pertinente. Solo entonces invoca el modelo con límites de entrada/salida, caché y medición por curso. La meta no es “prometer” ahorro: se mide contra una línea base equivalente y se acepta si reduce tokens facturados al menos en 40%.

## Orden de lectura

1. [Problema y supuestos](Problema.md)
2. [Personas](Personas/)
3. [Requerimientos](Requirements/)
4. [Evaluación](Spec/Results.md)
5. [Arquitectura y diagrama](Architecture.md)
