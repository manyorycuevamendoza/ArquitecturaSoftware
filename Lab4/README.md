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
| Diagrama Top Down Design | [Diagrams/01-topdown-remoteschooly.excalidraw](Diagrams/01-topdown-remoteschooly.excalidraw) |
| Ejemplo de solicitud intermedia | [Examples/solicitud-ia.example.json](Examples/solicitud-ia.example.json) |

## Decisión central

La central de Lima publica el contenido por Internet. En cada escuela, un **Nodo Escolar Local** sincroniza solo las diferencias mediante descargas segmentadas y reanudables; prioriza el material esencial y conserva la última versión válida durante un corte. Cuando la red vuelve, reanuda desde el último bloque verificado y confirma la instalación. No se usa transporte físico.

Para IA, el docente no conversa directamente con el modelo. Primero completa una solicitud estructurada; un **AI Gateway** local valida que sea concreta, pide solo los datos faltantes y construye un prompt breve con el fragmento curricular pertinente. Solo entonces invoca el modelo con límites de entrada/salida, caché y medición por curso. La meta no es “prometer” ahorro: se mide contra una línea base equivalente y se acepta si reduce tokens facturados al menos en 40%.

## Orden de lectura

1. [Problema y supuestos](Problema.md)
2. [Personas](Personas/)
3. [Requerimientos](Requirements/)
4. [Evaluación](Spec/Results.md)
5. [Arquitectura y diagrama](Architecture.md)
