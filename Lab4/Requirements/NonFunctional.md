# Requerimientos no funcionales

La columna PD indica el punto de decisión de
[../Diagrams/Contexto/00-contexto-diagrama.md](../Diagrams/Contexto/00-contexto-diagrama.md) del que
sale el requisito. La columna **Usuario responsable** dice de quién nace: qué
persona tiene la necesidad que lo justifica, no qué componente lo implementa.

## Red y transferencia

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-NET-01 | Ante un corte de hasta 30 min, una descarga segmentada conserva el progreso de los bloques ya verificados y se reanuda automáticamente dentro de 5 min después de recuperar conectividad. | Rosa, docente rural | PD-1 |
| NFR-NET-02 | La sincronización usa HTTPS, compresión y solicitudes por rango; con un enlace de 1 Mbps no inicia multimedia opcional hasta que todos los recursos esenciales estén `READY`. | Diego, estudiante | PD-1 |
| NFR-NET-03 | En horario de clase la sincronización se ejecuta con un tope de ancho de banda configurado, de modo que abrir un recurso ya presente en la caché no se degrade por la transferencia de fondo. Con 30 clientes LAN activos y una sincronización en curso, el p95 de apertura sigue cumpliendo `NFR-PER-01`. | Rosa, docente rural | PD-7 |
| NFR-NET-04 | Cada escuela entra a la ventana de sincronización tras una espera aleatoria propia dentro de la ventana configurada, para que la carga sobre el almacenamiento central no se concentre en un mismo instante. | Valeria, coordinadora | PD-7 |

## Capacidad del nodo

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-CAP-01 | Cada Nodo Escolar Local dispone de al menos 8 GB de almacenamiento utilizable: la activación atómica exige mantener la versión activa y la versión nueva al mismo tiempo, más la cola de eventos, el índice de bloques y el margen del sistema. Un nodo dimensionado por debajo de ese mínimo no puede completar una activación. | Administrador regional | PD-8 |
| NFR-CAP-02 | Al alcanzar el 85% de ocupación de disco, el nodo emite alerta al administrador regional y detiene la descarga de contenido opcional. La alerta se emite antes del punto en que ya no se puede escribir el registro del propio fallo. | Administrador regional | PD-8 |

## Integridad y continuidad

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-INT-01 | Un paquete con firma o hash inválido no se activa y deja un registro con archivo y razón del rechazo. Si además no existe versión anterior `READY`, el estado se marca de forma explícita y se alerta a la central. | Diego, estudiante | PD-2 |
| NFR-INT-02 | El manifiesto, los bloques descargados y los eventos de sincronización son auditables con versión e identificadores; una nueva versión no mezcla archivos con la anterior. | Valeria, coordinadora | PD-2 |
| NFR-INT-03 | El cambio de versión activa es atómico frente a un corte de energía. En una prueba de al menos 20 cortes provocados en instantes distintos del proceso de activación, el nodo arranca sirviendo la versión anterior completa o la nueva completa, nunca una mezcla. | Rosa, docente rural | PD-5 |
| NFR-AVL-01 | Durante un corte, el catálogo y la última versión `READY` permanecen accesibles para 30 clientes LAN; no se requiere que las funciones que dependen de Internet estén disponibles. | Diego, estudiante | PD-7 |
| NFR-PER-01 | Con 30 clientes LAN activos, el p95 para abrir la portada de una guía de hasta 5 MB es ≤ 3 s. | Diego, estudiante | |

## Costo de IA

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-COST-01 | Sobre un conjunto de al menos 30 solicitudes equivalentes, los tokens externos del AI Gateway son ≥ 40% menores que la línea base; se cuentan prompt y completion, incluido cualquier paso de IA adicional. | Valeria, coordinadora | PD-11 |
| NFR-COST-02 | El 100% de invocaciones externas respeta los presupuestos configurados de entrada y salida o queda bloqueado antes de enviarse. | Valeria, coordinadora | PD-12 |
| NFR-COST-03 | Una tarea entra en la comparación de `NFR-COST-01` solo si línea base y ejecución con Gateway coinciden en tarea, modelo y versión curricular. Las tareas que no cumplen las tres condiciones se listan aparte como no comparables y no cuentan para la meta. | Valeria, coordinadora | PD-12 |
| NFR-COST-04 | Las solicitudes en cola `PENDING_NETWORK` tienen su cuota reservada: el consumo comprometido más el ya facturado nunca supera el presupuesto del periodo, aunque la cola se drene entera de una vez. | Valeria, coordinadora | PD-10 |

## Auditoría, seguridad y uso

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-AUD-01 | Sincronizaciones e invocaciones IA son auditables con identificador, versión, actor, fecha y resultado; no se registra contenido sensible innecesario del estudiante. | Valeria, coordinadora | PD-3 |
| NFR-AUD-02 | El orden temporal de la auditoría se establece con la hora de la central, no con la del nodo. Un nodo con el reloj desviado produce registros con hora local incorrecta pero conserva orden e identidad correctos. | Valeria, coordinadora | PD-6 |
| NFR-SEC-01 | Solo los roles autorizados pueden publicar contenido, administrar un nodo, editar plantillas de prompt o ver reportes de costo; los clientes LAN solo leen sus recursos permitidos. | Valeria, coordinadora | PD-9 |
| NFR-SEC-02 | La sesión resuelta sin conexión caduca en un plazo configurado y se revalida contra la central en la siguiente ventana de red. La llave pública de verificación de manifiestos se puede rotar sin reinstalar el nodo: durante la rotación el nodo acepta la llave anterior y la nueva por un periodo declarado. | Administrador regional | PD-9 |
| NFR-USA-01 | Al probar con cinco docentes, al menos cuatro completan una solicitud IA válida o responden una aclaración sin asistencia y entienden el estado "pendiente de sincronización". | Rosa, docente rural | PD-9 |

## Alcance declarado

No se especifica una meta de disponibilidad total ni una segunda conexión. El diseño aprovecha el Internet existente, reduce datos transferidos y asegura continuidad local con la última versión verificada durante un corte.

Dos supuestos que el enunciado no da y el diseño necesita, declarados aquí para que no pasen por hechos:

1. La caché de resultados de IA reside en el nodo local. De eso depende que un acierto de caché funcione durante un corte.
2. El nodo dispone de energía suficiente para sostener una transferencia iniciada. `NFR-CAP-01` y `FR-DIS-10` acotan qué ocurre cuando no es así, pero la frecuencia real de cortes de energía por escuela no está medida.
