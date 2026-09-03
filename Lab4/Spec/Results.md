# Resultado EVAL — RemoteSchooly

## Resultado de la evaluación de requisitos

| Dimensión | Puntaje | Evidencia |
| --- | ---: | --- |
| Cobertura de personas | 8.9/10 | Rosa, Diego y Valeria tienen necesidades diferenciadas y requisitos trazables. |
| Cobertura de los dos problemas | 9.3/10 | `FR-DIS-01..06` cubren red limitada/cortes; `FR-AI-01..08` cubren reducción de tokens. |
| Verificabilidad | 9.1/10 | Diferencias, rangos, reanudación, estado `READY`, límites y fórmula de ahorro son observables. |
| Claridad de alcance | 9.0/10 | Se excluyen transporte físico, Internet satelital y disponibilidad total. |
| Factibilidad arquitectónica | 8.8/10 | Un servicio modular, almacenamiento HTTPS y un Sync Agent local resuelven el piloto sin microservicios prematuros. |

**Resultado global: 9.0/10 — Passed (≥ 8/10).**

## Trazabilidad de pain points críticos

| Persona | Pain point | Requisitos que responden |
| --- | --- | --- |
| Rosa | Una descarga reinicia o no puede enviar una solicitud durante un corte. | `FR-DIS-03/04/05/06`, `FR-AI-01/02/03/05/06` |
| Diego | Un corte deja el material incompleto o inaccesible. | `FR-DIS-04/05`, `NFR-NET-01/02`, `NFR-AVL-01` |
| Valeria | Debe saber qué versión llegó y probar ahorro, no solo estimarlo. | `FR-DIS-01/02/05/06`, `FR-AI-07/08`, `NFR-COST-01` |

## Evidencia de la meta de 40%

El requisito no declara un ahorro como hecho sin medirlo. El piloto debe ejecutar las mismas 30 o más tareas con: (a) prompt directo de línea base y (b) solicitud intermedia + Gateway. Debe conservar modelo, versión curricular y objetivo equivalentes, y calcular:

`reducción = (tokens_base − tokens_gateway) / tokens_base × 100`

Solo se marca aprobado si la reducción es ≥ 40%. También se suman tokens de cualquier paso adicional que use IA, para impedir que el ahorro sea aparente.

## Gaps conservados

1. Falta medir ancho de banda, duración y frecuencia real de los cortes por escuela.
2. El diseño reanuda transferencias, pero no garantiza que cada escuela reúna una ventana de red suficiente para terminar todo el paquete semanal.
3. Falta probar que las plantillas y límites conservan calidad pedagógica para cada grado.
4. La estimación de costo requiere precios y telemetría del proveedor elegido en el piloto.

Estos gaps son explícitos: el diseño mitiga Internet limitado e intermitente sin prometer una conectividad que el caso no proporciona.
