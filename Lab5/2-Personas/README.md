# Personas

Cinco personas, una por actor del diagrama. Cada archivo sigue la misma
estructura: perfil, contexto, objetivos, pain points, escenario clave sobre el
diagrama, criterios de éxito y requisitos que la cubren.

Los actores y su alcance de acceso están en [Usuarios.md](Usuarios.md).

| Persona | Rol | Tipo | Necesidad principal | Componentes del diagrama que usa |
| --- | --- | --- | --- | --- |
| [Camila](Camila.md) | Ingeniera de soporte | Usuario directo | Atender escalaciones de cliente sin que una instrucción suya cause daño, y con el estado vigente. | Pregunta en lenguaje natural, Estado de incidencia, Vista previa de impacto, Bloqueo de escritura, Score y motivo |
| [Andrés](Andres.md) | Ingeniero de desarrollo | Usuario directo | Que Genius responda durante el pico y que las pruebas E2E nunca toquen producción. | Incidencia escalada, Incidencias similares, Consulta de solo lectura, Pruebas E2E, Modo degradado, Abstención |
| [Paola](Paola.md) | Incident Manager | Usuario directo (operador) | Aprobar lo peligroso, cumplir el SLA por clase y reconstruir qué pasó. | Aprobación de la acción, Kill switch, Métricas y dashboard, Auditoría, Aprobación de cambios al conocimiento |
| [Martín](Martin.md) | Data Science | Usuario interno | Que el LLM aprenda con conocimiento validado y que cada versión se pruebe antes de publicarse. | Ingesta, Curación de conocimiento, Enriquecimiento del LLM, Eval set, BD3 |
| [Lucía](Lucia.md) | Cliente (empresa) | Usuario externo / beneficiaria | Saber el estado real de su escalación sin que su información se exponga. | Auth y rol (solo sus incidencias), Respuesta con hora del dato, Notificación |

## Cobertura por persona

Un requisito puede servir a varias personas; ninguna persona queda sin
requisitos y ningún requisito queda sin persona que lo necesite.

| Persona | Requisitos que la cubren |
| --- | --- |
| Camila | `FR-ACT-03`, `FR-ACT-04`, `FR-ACT-05`, `FR-ACT-07`, `FR-ANS-01`, `FR-ANS-02`, `FR-ANS-03`, `FR-ANS-04`, `FR-ANS-06`, `FR-ANS-10`, `FR-ANS-13`, `FR-REL-05`, `NFR-PER-01`, `NFR-FRE-01`, `NFR-FRE-02`, `NFR-DET-01`, `NFR-DET-03`, `NFR-SEC-01`, `NFR-USA-01` |
| Andrés | `FR-ACT-08`, `FR-ACT-10`, `FR-ANS-05`, `FR-ANS-08`, `FR-ANS-09`, `FR-REL-03`, `FR-REL-04`, `FR-REL-05`, `FR-REL-06`, `FR-REL-07`, `FR-REL-09`, `NFR-AVL-01`, `NFR-AVL-04`, `NFR-PER-03`, `NFR-PER-04`, `NFR-CAP-01`, `NFR-USA-02` |
| Paola | `FR-ACT-01`, `FR-ACT-02`, `FR-ACT-04`, `FR-ACT-06`, `FR-ACT-09`, `FR-ACT-12`, `FR-ANS-12`, `FR-REL-01`, `FR-REL-02`, `FR-REL-06`, `FR-REL-08`, `FR-REL-10`, `FR-REL-11`, `FR-REL-12`, `NFR-AVL-02`, `NFR-AVL-03`, `NFR-PER-02`, `NFR-CAP-02`, `NFR-CAP-03`, `NFR-SEC-02`, `NFR-SEC-03`, `NFR-REC-01`, `NFR-REC-02`, `NFR-AUD-01`, `NFR-AUD-02`, `NFR-OBS-01`, `NFR-OBS-02` |
| Martín | `FR-ANS-07`, `FR-ANS-10`, `FR-ANS-11`, `FR-ANS-12`, `FR-ACT-08`, `NFR-DET-02`, `NFR-SEC-04`, `NFR-CAP-01` |
| Lucía | `FR-ACT-11`, `FR-ANS-02`, `FR-ANS-03`, `FR-ANS-13`, `FR-REL-01`, `FR-REL-02`, `NFR-AVL-02`, `NFR-PER-02`, `NFR-SEC-04` |
