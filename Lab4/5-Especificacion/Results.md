# Resultado EVAL — RemoteSchooly

Evaluación sobre 49 requisitos: 25 funcionales (`FR-DIS-01..13`, `FR-AI-01..16`)
y 24 no funcionales. Cada uno declara el usuario del que nace y el punto de
decisión en el que se resolvió.

## Resultado de la evaluación de requisitos

| Dimensión | Puntaje | Evidencia |
| --- | ---: | --- |
| Cobertura de personas | 9.2/10 | Rosa, Diego, Valeria y el Administrador regional tienen necesidades diferenciadas, requisitos propios y un happy path cada uno. Ninguna persona queda sin requisitos y ningún requisito queda sin persona. |
| Cobertura de los dos problemas | 9.3/10 | `FR-DIS-01..13` cubren red limitada y cortes; `FR-AI-01..16` cubren la reducción de tokens. Cada requisito traza a uno de los 12 puntos de decisión resueltos. |
| Verificabilidad | 9.1/10 | Los criterios son observables: descarga por diferencias, rangos reanudables, estado `READY`, activación atómica frente a 20 cortes provocados, presupuestos de entrada y salida, y la fórmula de ahorro. |
| Trazabilidad | 9.4/10 | Verificado por código: ningún requisito sin usuario responsable, ninguno con un componente como responsable, ninguna referencia a un ID inexistente, ninguno huérfano, y los 49 ejercitados por al menos un happy path. |
| Claridad de alcance | 9.0/10 | Se excluyen transporte físico, Internet satelital y disponibilidad total. Los dos supuestos que el enunciado no da quedan declarados, no dados por hechos. |
| Factibilidad arquitectónica | 8.8/10 | Un monolito modular con almacenamiento HTTPS y un nodo local por escuela resuelve el piloto sin microservicios prematuros. |

**Resultado global: 9.1/10 — Passed (≥ 8/10).**

## Trazabilidad: de quién nace cada requisito

| Persona | Requisitos | Lo que necesita |
| --- | ---: | --- |
| Valeria, coordinadora | 22 | Publicar versiones correctas, auditar qué llegó a cada escuela y demostrar el ahorro en vez de prometerlo. |
| Rosa, docente rural | 14 | Enseñar en la fecha que toca, con o sin señal, y pedir material sin perder tiempo ni gastar de más. |
| Diego, estudiante | 8 | Acceder al curso completo aunque Internet se caiga, y que su avance no se pierda ni se cuente dos veces. |
| Administrador regional | 5 | Dimensionar y supervisar el nodo de la escuela sin viajar hasta ella. |

Los proveedores de almacenamiento y de IA no figuran como responsables: son
sistemas externos y no tienen necesidad propia dentro del caso.

El desglose completo está en
[../3-Requerimientos/Functional.md](../3-Requerimientos/Functional.md).

## Cobertura de los happy paths

Los cuatro recorridos de [SPEC-TEMPLATE.md](SPEC-TEMPLATE.md) ejercitan los 49
requisitos. Ninguno queda sin un camino feliz que lo recorra, y ningún paso se
apoya en algo que no esté exigido por un requisito.

| Recorrido | Pasos | Qué demuestra |
| --- | ---: | --- |
| Valeria | 7 | Que se puede publicar, retirar contenido, versionar plantillas, auditar y medir el ahorro. |
| Rosa | 9 | Que se puede enseñar y pedir material durante un corte, y que el gasto se evita antes de la llamada. |
| Diego | 9 | Que el curso llega completo pese a los cortes y que el avance vuelve una sola vez. |
| Administrador regional | 7 | Que un nodo se da de alta, se dimensiona y se mantiene sin viajar a la escuela. |

## Trazabilidad de pain points críticos

| Persona | Pain point | Requisitos que responden |
| --- | --- | --- |
| Rosa | Una descarga reinicia, la activación queda a medias, o la sincronización le quita la red durante la clase. | `FR-DIS-02/03/07/10`, `NFR-NET-01/03`, `NFR-INT-03` |
| Rosa | No puede entrar al sistema durante un corte porque el login depende de Lima. | `FR-AI-13`, `NFR-SEC-02` |
| Rosa | Pide material a la IA y pierde el tiempo o el control del gasto. | `FR-AI-01/03/11/12/16`, `NFR-USA-01` |
| Diego | Un corte deja el material incompleto, inaccesible, o pierde las semanas sin señal. | `FR-DIS-04/05/09`, `NFR-NET-02`, `NFR-INT-01`, `NFR-AVL-01`, `NFR-PER-01` |
| Diego | Su avance se pierde o se registra dos veces. | `FR-DIS-06/08/13` |
| Valeria | Debe saber qué versión llegó a cada escuela y auditar el orden real de los hechos. | `FR-DIS-01/08`, `NFR-INT-02`, `NFR-AUD-01/02` |
| Valeria | Debe probar el ahorro, no estimarlo, y poder reproducir el número. | `FR-AI-02/04..10/14/15`, `NFR-COST-01..04` |
| Administrador regional | Dimensiona y supervisa el nodo sin viajar a la escuela. | `FR-DIS-11/12`, `NFR-CAP-01/02` |

## Evidencia de la meta de 40%

El requisito no declara un ahorro como hecho sin medirlo. El piloto debe ejecutar las mismas 30 o más tareas con: (a) prompt directo de línea base y (b) solicitud intermedia con Gateway. Debe conservar modelo, versión curricular y objetivo equivalentes, y calcular:

`reducción = (tokens_base − tokens_gateway) / tokens_base × 100`

Solo se marca aprobado si la reducción es ≥ 40%. Se suman los tokens de cualquier paso adicional que use IA, para impedir que el ahorro sea aparente, y se registran también las llamadas fallidas que hayan facturado.

El desglose de una solicitud típica muestra de dónde sale la reducción:

| Concepto | Clase | Libre | Con Gateway |
| --- | --- | ---: | ---: |
| Saludos y cortesías | ruido | 80 | 0 |
| Grado y curso ya puestos en el formulario | redundante | 120 | 0 |
| Temario completo de Comunicación | acotable | 1,100 | 352 |
| Objetivo pedagógico y restricciones | imprescindible | 400 | 280 |
| Instrucciones de formato | imprescindible | 300 | 210 |
| **Total** | | **2,000** | **842** |

Reducción del 58% contra una meta del 40%. El 55% del ahorro sale de un solo caso: enviar dos fragmentos etiquetados en lugar del temario entero. Limpiar saludos y repeticiones aporta el 10%; con eso solo no se llega a la meta.

## Cómo se verificó

No es una revisión a ojo. Sobre los documentos se corre:

| Comprobación | Resultado |
| --- | --- |
| Requisitos sin usuario responsable | ninguno |
| Requisitos con un componente como responsable | ninguno |
| Referencias a un ID de requisito que no existe | ninguna |
| Requisitos que ninguna persona reclama | ninguno |
| Requisitos sin un happy path que los ejercite | ninguno |
| Enlaces relativos rotos en los documentos | ninguno |

## Gaps conservados

1. Falta medir ancho de banda, duración y frecuencia real de los cortes por escuela.
2. El diseño reanuda transferencias, pero no garantiza que cada escuela reúna una ventana de red suficiente para terminar todo el paquete semanal.
3. Falta probar que las plantillas y los límites de tokens conservan calidad pedagógica en cada grado.
4. La estimación de costo requiere precios y telemetría del proveedor elegido en el piloto.
5. Dos supuestos quedan declarados y sin medir: que la caché de resultados de IA reside en el nodo local, de lo que depende que un acierto funcione durante un corte; y que hay energía suficiente para sostener una transferencia iniciada.
6. Tres puntos de decisión quedan identificados y sin resolver: qué pasa con una escuela que estuvo meses sin red cuando la central ya rotó la llave de firma, qué ocurre cuando una escuela se divide o se fusiona y cambia su identificador, y qué hacer con una solicitud de IA encolada que caduca al cambiar la versión curricular.

Estos gaps son explícitos: el diseño mitiga Internet limitado e intermitente sin prometer una conectividad que el caso no proporciona.
