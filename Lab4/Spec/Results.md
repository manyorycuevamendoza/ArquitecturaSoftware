# Resultado EVAL — RemoteSchooly

## Resultado de la evaluación de requisitos

| Dimensión | Puntaje | Evidencia |
| --- | ---: | --- |
| Cobertura de personas | 8.8/10 | Rosa, Diego y Valeria tienen necesidades diferenciadas y requisitos trazables. |
| Cobertura de los dos problemas | 9.2/10 | `FR-DIS-01..06` cubren distribución sin Internet; `FR-AI-01..08` cubren reducción de tokens. |
| Verificabilidad | 9.0/10 | Hash, firma, WAN desconectada, presupuestos, cero llamadas y fórmula de ahorro son observables. |
| Claridad de alcance | 9.0/10 | Se excluyen explícitamente Internet remoto, HA y confiabilidad avanzada. |
| Factibilidad arquitectónica | 8.6/10 | Una plataforma modular, nodo local y logística física satisfacen el piloto sin servicios distribuidos innecesarios. |

**Resultado global: 8.9/10 — Passed (≥ 8/10).**

## Trazabilidad de pain points críticos

| Persona | Pain point | Requisitos que responden |
| --- | --- | --- |
| Rosa | No puede descargar materiales; la pregunta es extensa o ambigua. | `FR-DIS-03/04/05`, `FR-AI-01/02/03/05/06` |
| Diego | No tiene Internet ni distingue una versión correcta. | `FR-DIS-04/05`, `NFR-OFF-01`, `NFR-INT-01` |
| Valeria | Debe asegurar entrega correcta y probar ahorro, no solo estimarlo. | `FR-DIS-01/02/03`, `FR-AI-07/08`, `NFR-COST-01` |

## Evidencia de la meta de 40%

El requisito no declara un ahorro como hecho sin medirlo. El piloto debe ejecutar las mismas 30 o más tareas con: (a) prompt directo de línea base y (b) solicitud intermedia + Gateway. Debe conservar modelo, versión curricular y objetivo equivalentes, y calcular:

`reducción = (tokens_base − tokens_gateway) / tokens_base × 100`

Solo se marca aprobado si la reducción es ≥ 40%. También se suman tokens de cualquier paso adicional que use IA, para impedir que el ahorro sea aparente.

## Gaps conservados

1. Falta validar frecuencia real de transporte, capacidad eléctrica y hardware de cada comunidad.
2. La integridad detecta corrupción, pero aún no resuelve extravío, demora o sustitución física del medio.
3. Falta probar que las plantillas y límites conservan calidad pedagógica para cada grado.
4. La estimación de costo requiere precios y telemetría del proveedor elegido en el piloto.

Estos gaps no contradicen el enunciado: la entrega exige que los cursos lleguen correctamente, no disponibilidad perfecta ni mecanismos completos de confiabilidad todavía.
