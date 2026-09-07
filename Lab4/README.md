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
| Ejemplo de solicitud intermedia | [Examples/solicitud-ia.example.json](Examples/solicitud-ia.example.json) |

## Qué diagrama usar

Los dos enlaces de Excalidraw están en [Diagrams/](Diagrams/README.md).

| Problema | Qué cuenta | Casos |
| --- | --- | ---: |
| 1. Distribución con Internet intermitente | El recorrido entero de Valeria a Valeria, en diez escenas: publicación, ventana de sincronización, qué archivos bajar, verificación, activación atómica, la clase sin red y el retorno idempotente. | 36 |
| 2. Gasto excesivo de tokens | Ocho escenas donde cada paso descarta una razón para llamar al modelo. La llamada es lo último que queda, y casi nunca se llega a ella. | 18 |

Cada lienzo se lee igual: el guion numerado va en la columna izquierda y se sigue de arriba a abajo mientras se señalan las cajas. Los peores casos aparecen en rojo, junto al componente que los ataja, con su código `P1` a `P34`.

Para sustentar **por qué** está diseñado así, y no solo qué hace, el Top Down Design crece en tres iteraciones acumulativas: la primera plantea el sistema como una caja, la segunda abre la distribución offline-first, la tercera agrega la gobernanza de tokens con login y biblioteca de prompts. Ninguna reemplaza a la anterior.

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
