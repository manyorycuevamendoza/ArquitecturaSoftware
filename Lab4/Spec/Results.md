# Resultado EVAL — RemoteSchooly

## Resultado de la evaluación de requisitos

| Dimensión | Puntaje | Evidencia |
| --- | ---: | --- |
| Cobertura de personas | 8.9/10 | Rosa, Diego y Valeria tienen necesidades diferenciadas y requisitos trazables. |
| Cobertura de los dos problemas | 9.3/10 | `FR-DIS-01..13` cubren red limitada y cortes; `FR-AI-01..16` cubren reducción de tokens. Cada requisito traza a un punto de decisión resuelto y a un lienzo. |
| Verificabilidad | 9.1/10 | Diferencias, rangos, reanudación, estado `READY`, límites y fórmula de ahorro son observables. |
| Claridad de alcance | 9.0/10 | Se excluyen transporte físico, Internet satelital y disponibilidad total. |
| Factibilidad arquitectónica | 8.8/10 | Un servicio modular, almacenamiento HTTPS y un Sync Agent local resuelven el piloto sin microservicios prematuros. |

**Resultado global: 9.0/10 — Passed (≥ 8/10).**

## Trazabilidad de pain points críticos

Cada requisito declara su usuario responsable: la persona cuya necesidad lo
justifica, no el componente que lo implementa. El desglose completo está en
[../Requirements/Functional.md](../Requirements/Functional.md).

| Persona | Pain point | Requisitos que responden |
| --- | --- | --- |
| Rosa | Una descarga reinicia, la activación queda a medias, o la sincronización le quita la red durante la clase. | `FR-DIS-02/03/07/10`, `NFR-NET-01/03`, `NFR-INT-03` |
| Rosa | Pide material a la IA y pierde el tiempo o el control del gasto. | `FR-AI-01/03/11/12`, `NFR-USA-01` |
| Rosa | No puede entrar al sistema durante un corte porque el login depende de Lima. | `FR-AI-13`, `NFR-SEC-02` |
| Diego | Un corte deja el material incompleto, inaccesible, o pierde las semanas sin señal. | `FR-DIS-04/05/09`, `NFR-NET-02`, `NFR-INT-01`, `NFR-AVL-01`, `NFR-PER-01` |
| Diego | Su avance se pierde o se registra dos veces. | `FR-DIS-06/08` |
| Valeria | Debe saber qué versión llegó a cada escuela y auditar el orden real de los hechos. | `FR-DIS-01/08`, `NFR-INT-02`, `NFR-AUD-01/02` |
| Valeria | Debe probar el ahorro, no estimarlo, y poder reproducir el número. | `FR-AI-02/04..10`, `NFR-COST-01..04` |
| Administrador regional | Dimensiona y supervisa el nodo sin viajar a la escuela. | `FR-DIS-11`, `NFR-CAP-01/02` |

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
