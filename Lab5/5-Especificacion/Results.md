# Resultados de la evaluación — Genius-x

Evaluación sobre 65 requisitos: 37 funcionales (`FR-ACT-01..12`,
`FR-ANS-01..13`, `FR-REL-01..12`) y 28 no funcionales. Ejecutada con el agente
definido en [Eval-Spec.md](Eval-Spec.md).

## Iteración 1

### Verificación mecánica previa

| Comprobación | Resultado |
| --- | --- |
| IDs citados en personas o requisitos que no existen | ninguno |
| Requisitos que ninguna persona reclama | ninguno |
| Tabla de cobertura del README de personas vs. cada archivo de persona | consistente |
| Componentes citados en requisitos que no están en el diagrama | ninguno |
| Servicios del diagrama sin ningún requisito que los exija | ninguno |
| Puntos de decisión citados que no existen en Problema.md | ninguno |
| Enlaces relativos rotos | `4-Arquitectura/` (entregable aún pendiente) |

### Evaluaciones por persona

| Persona | Cobertura | Gaps principales |
| --- | --- | --- |
| Camila | 90% | `NFR-FRE-01` admite hasta 5 minutos de antigüedad del estado (BD1 se sincroniza cada 5 min en el diagrama): una incidencia cerrada hace 4 minutos aún puede responder "abierta". `FR-ANS-10` no dice qué pasa con una calificación negativa aislada. |
| Andrés | 88% | `FR-REL-06` descarta "ingeniería de baja criticidad" sin definir criticidad. La **Cola por prioridad** aparece como una sola caja en el diagrama y `FR-REL-07` no la nombra en la redundancia N+1. |
| Paola | 90% | `FR-ACT-04` y `NFR-SEC-03` la convierten en aprobadora única sin modo de emergencia: si no está disponible, ninguna acción destructiva avanza. No hay rol de aprobador suplente. `FR-ACT-09` no dice quién puede revertir el kill switch. |
| Martín | 82% | `FR-ANS-12` no fija tamaño mínimo ni composición del eval set. `FR-ANS-11` no exige anonimizar en la **Ingesta de data del cliente**; la anonimización solo aparece en la réplica de pruebas (`NFR-SEC-04`). |
| Lucía | 78% | Su objetivo "recibir aviso cuando su incidencia cambie" queda parcial: `FR-ANS-13` notifica al ingeniero, no al cliente. `FR-ACT-11` limita el acceso a sus incidencias pero no define qué campos internos ve. |

### Puntaje global

| Dimensión | Puntaje | Peso | Ponderado |
| --- | --- | --- | --- |
| Cobertura de personas | 86% | 25% | 21.50% |
| Cobertura de los problemas del caso | 92% | 25% | 23.00% |
| Verificabilidad | 90% | 15% | 13.50% |
| Trazabilidad al diagrama | 95% | 15% | 14.25% |
| Reliability y fault tolerance | 85% | 15% | 12.75% |
| Claridad y no duplicación | 88% | 5% | 4.40% |

**Puntaje global: 89.4%**
**Veredicto:** Aceptable con correcciones menores.

### Justificación

- **Cobertura de personas (86%):** promedio de las cinco coberturas. Las tres personas operativas (Camila, Andrés, Paola) están bien cubiertas por `FR-ACT-02..06`, `FR-ANS-01..06` y `FR-REL-01..06`. Martín y Lucía bajan el promedio: Martín por la falta de definición del eval set y de la anonimización en ingesta; Lucía porque el diagrama la incluye como actora con su propio "Auth y rol" pero los requisitos la tratan casi solo como beneficiaria.
- **Cobertura de los problemas del caso (92%):** los seis problemas tienen requisitos que los resuelven, según la tabla de pain points de `Functional.md`. El borrado tiene cinco barreras (`FR-ACT-02..06`); el estado desactualizado, `FR-ANS-02/03/04` y `NFR-FRE-01`; las respuestas distintas, `FR-ANS-04/06/07` y `NFR-DET-01`; el LLM que no aprende, `FR-ANS-10/11/12`; el pico, `FR-REL-02/05/06` y `NFR-CAP-02`; la tolerancia a fallos, `FR-REL-04/07/08`. El punto débil es la frescura: el problema dice "tiempo real" y `NFR-FRE-01` compromete 5 minutos.
- **Verificabilidad (90%):** los NFR tienen umbral y método (`NFR-PER-01..04`, `NFR-CAP-01..03`, `NFR-REC-01/02`). De los FR, `FR-ANS-09` ("con su contexto ya cargado") y `FR-ANS-11` ("conocimiento validado") tienen criterios cualitativos; `FR-REL-06` depende de una criticidad no definida.
- **Trazabilidad al diagrama (95%):** verificado por código: todo componente citado existe en el diagrama y todo servicio del diagrama tiene al menos un requisito. Se descuenta porque el diagrama dibuja un solo LLM y un solo Orquestador mientras `FR-REL-07` y `NFR-AVL-03` exigen N+1; la redundancia solo está dibujada como "backup (anti SPOF)" en BD1 y BD2.
- **Reliability y fault tolerance (85%):** los SPOF de la tabla de `Problema.md` están tratados: LLM (`FR-REL-05/07`), BD1 (`FR-REL-08`), Slack (`FR-REL-10`), orquestador (`FR-REL-07`). Faltan dos: la **Cola por prioridad** como componente único no nombrado en `FR-REL-07`, y el aprobador humano único de `NFR-SEC-03`, que es un SPOF organizacional, no técnico. Cortacircuito, degradación, descarte y simulacros están (`FR-REL-04/05/06/12`).
- **Claridad y no duplicación (88%):** las descripciones son de una oración y no hay solapamientos entre IDs. Quedan sin definir "crítica" (`FR-REL-06`, `NFR-AVL-02`, `NFR-PER-02`) y "similar" (`FR-ANS-08`).

### Gaps críticos

1. Definir qué hace "crítica" a una customer escalation: es el criterio que decide a quién no se descarta en `FR-REL-06`, `NFR-AVL-02` y `NFR-PER-02`.
2. Decidir la frescura del estado: si BD1 se sincroniza cada 5 minutos (diagrama), `NFR-FRE-01` es honesto pero no es "tiempo real"; si se quiere menos, el diagrama debe mostrar invalidación por evento entre BD1 y **Estado de incidencia**.
3. Incluir la **Cola por prioridad** en la redundancia N+1 de `FR-REL-07` y dibujar la redundancia del LLM y del Orquestador en el diagrama.
4. Agregar un aprobador suplente con el mismo rol para `FR-ACT-04` / `NFR-SEC-03`, de modo que la ausencia de una persona no bloquee toda acción.
5. Exigir anonimización en **Ingesta de data del cliente** (`FR-ANS-11`), no solo en la réplica de pruebas.
6. Definir la notificación al cliente cuando cambia su incidencia (Lucía) y qué campos puede ver.

### Acciones recomendadas

1. Agregar un glosario corto al inicio de `Functional.md`: crítica, similar, baja criticidad.
2. Ajustar `NFR-FRE-01` o el diagrama (gap 2) antes de sustentar; es la pregunta más probable del profesor sobre "tiempo real".
3. Extender `FR-REL-07` a la cola y `FR-ACT-04` al aprobador suplente; dibujar ambos en el diagrama.
4. Volver a ejecutar Eval-Spec tras los cambios.
