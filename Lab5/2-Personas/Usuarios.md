# Usuarios y actores

Los actores son los que aparecen a la izquierda del diagrama
([../Diagrams/diagramaLab5.excalidraw](../Diagrams/diagramaLab5.excalidraw)),
cada uno con su propio "Auth y rol".

| Actor | Tipo | Qué hace en Genius | Alcance de acceso |
| --- | --- | --- | --- |
| Ingeniero de soporte | Usuario directo | Atiende customer y support escalations; pregunta estado, pide acciones. | Sus incidencias y las de su área; escritura solo con aprobación. |
| Ingeniero de desarrollo | Usuario directo | Recibe engineering escalations y las escaladas desde soporte; consulta histórico, corre E2E. | Lectura de BD2, E2E en entorno de pruebas; escritura solo con aprobación. |
| Incident Manager | Usuario directo (operador) | Aprueba o rechaza acciones, opera el kill switch, mira el dashboard, aprueba cambios al conocimiento. | Aprueba, no ejecuta. |
| Data Science | Usuario interno | Ingesta datos del cliente, cura conocimiento, mantiene el eval set y enriquece el LLM. | BD3 y pipeline de conocimiento; no opera incidencias. |
| Cliente (empresa) | Usuario externo / beneficiario | Consulta el estado de sus propias incidencias y recibe notificaciones. | Solo sus incidencias. |
| Sistemas del cliente | Sistema externo | Fuente de datos para la ingesta. | — |
| Slack | Sistema externo | Canal de notificación. Puede caer. | — |
| LLM local | Componente no confiable por diseño | Propone respuestas y acciones; nunca ejecuta. | — |

## Personas frente a actores

| Persona | Actor que representa | Foco |
| --- | --- | --- |
| [Camila](Camila.md) | Ingeniera de soporte | Que una instrucción suya no se convierta en daño y que el estado sea el vigente. |
| [Andrés](Andres.md) | Ingeniero de desarrollo | Que Genius responda en el pico y que las pruebas no toquen producción. |
| [Paola](Paola.md) | Incident Manager | Aprobar lo que puede hacer daño, cumplir el SLA y reconstruir lo que pasó. |
| [Martín](Martin.md) | Data Science | Que el LLM mejore con conocimiento validado, sin sorpresas en cada versión. |
| [Lucía](Lucia.md) | Cliente (empresa) | Saber el estado real de su escalación sin que su información se exponga. |

Slack, los sistemas del cliente y el LLM son sistemas externos o componentes:
no tienen una necesidad propia dentro del caso.
