# Requerimientos no funcionales

Las estimaciones de carga, los SPOF y los puntos de decisión están en
[../1-Problema/Problema.md](../1-Problema/Problema.md). Cada requisito se traza
al componente del diagrama que lo cumple y al punto de decisión (PD) que lo
resuelve.

Los números son metas de piloto derivadas de las estimaciones del problema. Se
declaran para que sean discutibles y medibles.

## Disponibilidad y tolerancia a fallos

| ID | Requerimiento | Verificación | Componente del diagrama | PD |
| --- | --- | --- | --- | --- |
| NFR-AVL-01 | El camino de consulta tiene disponibilidad mensual ≥ 99.5%. | Una respuesta degradada marcada como tal cuenta como disponible; un error genérico o una respuesta fuera de su presupuesto de latencia, no. | Modo degradado | PD-13 |
| NFR-AVL-02 | En la primera semana del mes, la clase `CUSTOMER` mantiene la misma disponibilidad que el resto del mes. | Con BD1 disponible, ninguna consulta de customer escalation crítica se rechaza por saturación; el descarte se aplica a ingeniería. | Cola por prioridad | PD-11 |
| NFR-AVL-03 | Ningún componente del camino de consulta es una instancia única. | Apagar cualquier réplica no produce error visible; apagar todo el LLM degrada a respuestas sin modelo, pero no interrumpe. | LLM N+1, Orquestador de herramientas N+1, Cola por prioridad N+1, BD1 (réplica + failover) | PD-14 |
| NFR-AVL-04 | La caída de un sistema externo degrada solo lo que depende de él. | Con Slack caído, consultar y aprobar siguen disponibles; con BD2 caído, el estado sigue respondiendo y las preguntas analíticas se abstienen. | Notificación al ingeniero, Abstención | PD-12 |

## Latencia y rendimiento

| ID | Requerimiento | Verificación | Componente del diagrama | PD |
| --- | --- | --- | --- | --- |
| NFR-PER-01 | Una consulta de estado o pregunta frecuente responde con p95 ≤ 2 s y p99 ≤ 4 s con 100 ingenieros activos. | Estas consultas no invocan al modelo, así que su latencia no depende de la saturación del LLM. | Estado de incidencia, Caché de preguntas frecuentes | PD-9 |
| NFR-PER-02 | Una solicitud `CUSTOMER` crítica se admite a la cola en ≤ 5 s y su respuesta generada tiene p95 ≤ 15 s. | Se mide con la cola de `ENGINEERING` saturada. Es la meta de "tiempo real para decisiones críticas". | Cola por prioridad | PD-11 |
| NFR-PER-03 | Una solicitud `ENGINEERING` responde con p95 ≤ 30 s. | Superado el presupuesto, la solicitud se degrada o se encola con aviso de posición y tiempo estimado. | Cola por prioridad, Modo degradado | PD-13 |
| NFR-PER-04 | La respuesta por el camino degradado tiene p95 ≤ 1 s. | Con un cortacircuito abierto, la solicitud no espera el tiempo de espera de la dependencia caída. | Circuit Breaker, Modo degradado | PD-12 |

## Capacidad

| ID | Requerimiento | Verificación | Componente del diagrama | PD |
| --- | --- | --- | --- | --- |
| NFR-CAP-01 | El sistema sostiene ráfagas de 5 consultas/s con al menos 60% resueltas sin modelo. | El LLM se dimensiona N+1 para el 40% restante; con una réplica menos sigue cumpliendo `NFR-PER-02`. | Pregunta en lenguaje natural, Caché de preguntas frecuentes, LLM N+1 | PD-11 |
| NFR-CAP-02 | El diseño absorbe 1.7× el volumen semanal promedio sin cambios; a 3× degrada por prioridad sin caer. | Ambos escenarios se ejecutan como prueba de carga antes del pico, no durante. | Cola por prioridad | PD-13 |
| NFR-CAP-03 | Las colas son persistentes y aguantan 30 minutos de acumulación a carga de pico. | Al 80% de capacidad se alerta y se activa el descarte por prioridad. | Cola por prioridad, Métricas y dashboard | PD-13 |

## Frescura y consistencia del dato

| ID | Requerimiento | Verificación | Componente del diagrama | PD |
| --- | --- | --- | --- | --- |
| NFR-FRE-01 | El estado de una incidencia que responde Genius tiene como máximo 5 minutos de antigüedad y siempre declara la hora del dato. | Cerrar una incidencia y preguntar por ella pasado ese plazo no puede devolver "abierta". La respuesta muestra la hora de lectura de BD1. | Estado de incidencia, BD1, Respuesta con hora del dato | PD-6, PD-7 |
| NFR-FRE-02 | Cuando el estado se sirve desde la réplica durante un relevo, el retraso se declara y no supera 30 s. | Superado ese umbral, la consulta se rechaza con motivo en lugar de entregar un dato viejo. | BD1 (réplica + failover), Respuesta con hora del dato | PD-6 |

## Determinismo y calidad de la respuesta

| ID | Requerimiento | Verificación | Componente del diagrama | PD |
| --- | --- | --- | --- | --- |
| NFR-DET-01 | Veinte ejecuciones consecutivas de la misma pregunta frecuente devuelven la misma respuesta literal. | Una diferencia entre ejecuciones con el mismo dato es un defecto, no una variación aceptable. | Match determinístico, Caché de preguntas frecuentes | PD-9 |
| NFR-DET-02 | Ninguna respuesta se genera con un modelo, prompt o conocimiento que no haya pasado el eval set. | Cada cambio queda fechado; ninguna versión publicada empeora exactitud ni abstención correcta respecto de la vigente. | Eval set de respuestas conocidas, Aprobación de cambios al conocimiento | PD-10 |
| NFR-DET-03 | El 100% de las respuestas incluye hora del dato y fuente. | Una afirmación sin fuente ni hora se convierte en abstención. | Respuesta con hora del dato, Abstención | PD-8 |

## Seguridad de las acciones y del dato

| ID | Requerimiento | Verificación | Componente del diagrama | PD |
| --- | --- | --- | --- | --- |
| NFR-SEC-01 | El 100% de las llamadas a herramientas pasa por el Orquestador. | En una batería de 50 intentos de inyección en el cuerpo del incidente, cero acciones destructivas ejecutadas y 100% registradas. | Orquestador de herramientas, Auditoría | PD-5 |
| NFR-SEC-02 | Ninguna credencial del harness tiene permisos de esquema; el acceso por defecto es solo lectura. | La escritura se obtiene por la identidad del ingeniero y para la operación aprobada. | Permisos del ingeniero | PD-4 |
| NFR-SEC-03 | Una acción destructiva exige aprobación de una persona distinta del solicitante, con ventana de 15 minutos. | Sin aprobador disponible la acción no se ejecuta; no existe modo de emergencia que salte el bloqueo. | Bloqueo de escritura, Aprobación de la acción | PD-3 |
| NFR-SEC-04 | El detalle de las incidencias no sale de la red corporativa. | Las pruebas usan la réplica anonimizada; Slack recibe solo referencias (identificador, clase, enlace), nunca el detalle. | Réplica anonimizada, Notificación al ingeniero | PD-2 |

## Recuperación

| ID | Requerimiento | Verificación | Componente del diagrama | PD |
| --- | --- | --- | --- | --- |
| NFR-REC-01 | Una acción destructiva ejecutada por error se revierte en ≤ 60 minutos con pérdida de datos ≤ 5 minutos. | Se verifica en simulacro por periodo, midiendo el tiempo real. | Deshacer acción | PD-3 |
| NFR-REC-02 | El relevo de BD1 o BD2 se completa en ≤ 2 minutos sin perder transacciones confirmadas. | Durante el relevo el estado se sirve desde la réplica bajo `NFR-FRE-02` y las escrituras se rechazan con motivo. | BD1 (réplica + failover), BD2 (réplica + failover) | PD-14 |

## Auditoría y observabilidad

| ID | Requerimiento | Verificación | Componente del diagrama | PD |
| --- | --- | --- | --- | --- |
| NFR-AUD-01 | El 100% de consultas y acciones queda en auditoría append-only, retenida 12 meses. | El harness no puede modificar ni borrar ese registro. El incidente del borrado se reconstruye solo con la auditoría. | Auditoría | PD-15 |
| NFR-AUD-02 | El orden temporal de la auditoría lo da el reloj del servidor sincronizado por NTP. | Un desfase superior a 1 s se alerta. Ningún identificador depende del reloj para ser único. | Auditoría | PD-15 |
| NFR-OBS-01 | Se miden por clase: latencia p95/p99, tasa de error, profundidad de cola, saturación del LLM, consultas sin modelo, abstenciones, estado del Circuit Breaker y acciones rechazadas. | La alerta se emite al 80% de cualquier umbral. | Circuit Breaker, Métricas y dashboard | PD-12 |
| NFR-OBS-02 | Cada solicitud tiene un `requestId` que atraviesa entrada, cola, LLM y herramientas. | El `requestId` nace en la entrada y no cambia si la solicitud se encola o se reintenta. | Auth y rol, Auditoría | PD-15 |

## Uso

| ID | Requerimiento | Verificación | Componente del diagrama | PD |
| --- | --- | --- | --- | --- |
| NFR-USA-01 | El ingeniero distingue una respuesta degradada de una completa y entiende una abstención. | Al probar con cinco ingenieros, al menos cuatro lo logran y verifican una afirmación abriendo la incidencia citada. | Modo degradado, Abstención | PD-13 |
| NFR-USA-02 | Todo rechazo indica motivo y siguiente paso. | Ningún camino de fallo —latencia, prioridad, permisos, aprobación— termina en un error genérico. | Cola por prioridad, Permisos del ingeniero | PD-13 |

## Alcance declarado

No se compromete disponibilidad total, recuperación ante desastre regional ni
redundancia del centro de datos. El diseño tolera la falla de cualquier
componente del harness dentro de un mismo sitio.

Tres supuestos que el enunciado no da y el diseño necesita:

1. La capacidad del LLM es fija y escasa. Las metas de latencia dependen de que
   el 60% de las consultas no invoque al modelo.
2. BD1 y BD2 admiten réplica y recuperación a un punto en el tiempo. Sin eso,
   `NFR-REC-01` y `NFR-REC-02` no son sostenibles.
3. La primera semana concentra el 40% del volumen mensual. `FR-REL-11` y
   `NFR-CAP-02` existen para corregir ese supuesto con lo observado.
