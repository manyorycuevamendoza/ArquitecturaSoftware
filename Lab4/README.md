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
| Enumeración de casos del punto de decisión del AI Gateway | [Decisions/01-decision-ai-gateway.md](Decisions/01-decision-ai-gateway.md) |
| Diagrama Top Down Design (resumen) | [Diagrams/01-topdown-remoteschooly.excalidraw](Diagrams/01-topdown-remoteschooly.excalidraw) |
| Diagrama Top Down por iteraciones (técnico) | [Diagrams/02-topdown-remoteschooly-v2.excalidraw](Diagrams/02-topdown-remoteschooly-v2.excalidraw) |
| Diagrama narrativo del flujo completo (**el de la exposición**) | [Diagrams/03-flujo-narrativo-remoteschooly.excalidraw](Diagrams/03-flujo-narrativo-remoteschooly.excalidraw) |
| Ejemplo de solicitud intermedia | [Examples/solicitud-ia.example.json](Examples/solicitud-ia.example.json) |

## Qué diagrama usar

Hay dos lienzos vigentes y responden preguntas distintas.

**Para exponer el flujo: `Diagrams/03-flujo-narrativo-remoteschooly.excalidraw`.** Es el recorrido completo contado como una historia que se lee de izquierda a derecha, en lenguaje de aula y no de infraestructura. Son 24 momentos numerados repartidos en tres capítulos; cada caja dice qué pasa en palabras corrientes y lleva abajo, en gris pequeño, el nombre técnico de la pieza que lo hace.

| Capítulo | Qué cuenta | Pasos |
| --- | --- | ---: |
| 1 | De Lima al aula: el material llega aunque el Internet se caiga. | 1–9 |
| 2 | Rosa pide ayuda a la IA: todo se resuelve antes de gastar. | 10–19 |
| 3 | El regreso: la escuela responde y Valeria comprueba que el ahorro es real. | 20–24 |

Los colores son el argumento: azul es un paso normal, verde es un paso donde no se gasta nada, ámbar es donde algo falla o hay que esperar, y rojo es el único paso que cuesta dinero (el 18). Las cajas punteadas cuelgan del paso al que corresponden y cuentan qué pasa cuando algo sale mal.

**Para sustentar el diseño: `Diagrams/02-topdown-remoteschooly-v2.excalidraw`.** Es el lienzo Top Down Design: los requerimientos nacen de las personas y el diseño crece en tres iteraciones acumulativas.

| Iteración | Qué muestra |
| --- | --- |
| #1 | El sistema como una sola caja: qué entra y qué sale. |
| #2 | Distribución **offline-first** sobre el Internet que ya existe. Sin SSD ni transporte físico. |
| #3 | Gobernanza de tokens con **login** y **biblioteca de prompts** versionada, incluido el reuso de un prompt de 2026 en 2027. |

Cada paso del lienzo lleva una frase numerada: el diagrama se lee como un relato, no como un conjunto de cajas sueltas.

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
