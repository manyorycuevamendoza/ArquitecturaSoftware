# Requerimientos no funcionales

El enunciado interpretado, las estimaciones de carga, los SPOF y los puntos de
decisión están en [../1-Problema/Problema.md](../1-Problema/Problema.md).

La columna **Usuario responsable** dice de quién nace el requisito: qué persona
tiene la necesidad que lo justifica, no qué componente lo implementa. La columna
**PD** dice en qué punto de decisión se resolvió.

Los números son metas de piloto derivadas de las estimaciones declaradas en el
problema. Se ponen aquí para que sean discutibles y medibles, no porque el
enunciado los fije.

## Disponibilidad y tolerancia a fallos

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-AVL-01 | El camino de consulta de Genius mantiene una disponibilidad mensual ≥ 99.5%. Cuenta como no disponible tanto el error como la respuesta que excede su presupuesto de latencia. Una respuesta degradada —estado y ficha del incidente sin modelo, marcada como tal— **sí** cuenta como disponible; un error genérico no. | Andrés, ingeniero de guardia | PD-13 |
| NFR-AVL-02 | Durante la primera semana del mes, la clase `CUSTOMER` mantiene la misma meta de disponibilidad que el resto del mes. Mientras el sistema de registro esté disponible, ninguna consulta de un *customer escalation* crítico se rechaza por saturación: el descarte se aplica sobre las clases con SLA de tres días. | Camila, ingeniera de soporte | PD-11 |
| NFR-AVL-03 | Ningún componente del camino de consulta es una instancia única. En la prueba de fallas, apagar cualquier réplica individual no produce error visible; apagar el conjunto completo de inferencia degrada el servicio a respuestas sin modelo, pero no lo interrumpe. Se verifica componente por componente contra la tabla de SPOF del problema. | Martín, dueño del harness | PD-14 |
| NFR-AVL-04 | La caída de un sistema externo —Slack, el índice de recuperación o el proveedor de pruebas E2E— degrada solo la capacidad que depende de él. Con Slack fuera de servicio, consultar y aprobar siguen disponibles; con el índice fuera de servicio, el estado sigue respondiéndose y las preguntas analíticas se abstienen en lugar de inventar. | Camila, ingeniera de soporte | PD-12 |

## Latencia y rendimiento

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-PER-01 | Con 100 ingenieros activos, una consulta de estado o una pregunta frecuente con respuesta canónica vigente responde con p95 ≤ 2 s y p99 ≤ 4 s. Estas consultas no invocan al modelo, así que su latencia no depende de la saturación de la inferencia. | Andrés, ingeniero de guardia | PD-9 |
| NFR-PER-02 | Una solicitud de clase `CUSTOMER` crítica se admite a la cola de inferencia en ≤ 5 s aun con la cola de `ENGINEERING` saturada, y su respuesta generada cumple p95 ≤ 15 s. Es la meta de "tiempo real para decisiones críticas" del enunciado, acotada a la clase que la necesita. | Camila, ingeniera de soporte | PD-11 |
| NFR-PER-03 | Una solicitud de clase `ENGINEERING` responde con p95 ≤ 30 s. Superado el presupuesto de latencia, la solicitud no sigue esperando: se degrada o se encola como trabajo asíncrono con aviso, y el usuario recibe posición y tiempo estimado. | Andrés, ingeniero de guardia | PD-13 |
| NFR-PER-04 | La respuesta por el camino degradado tiene p95 ≤ 1 s. Con un cortacircuito abierto, la solicitud no espera el tiempo de espera de la dependencia caída: se responde de inmediato por el camino alterno. | Camila, ingeniera de soporte | PD-12 |

## Capacidad

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-CAP-01 | El sistema sostiene ráfagas de 5 consultas por segundo con al menos el 60% resuelto sin invocar al modelo. El conjunto de inferencia se dimensiona N+1 para sostener el 40% restante dentro de `NFR-PER-02` y `NFR-PER-03`; una réplica menos sigue cumpliendo la meta. | Martín, dueño del harness | PD-11 |
| NFR-CAP-02 | El diseño absorbe 1.7 veces el volumen semanal promedio —el pico de la primera semana— sin cambios de arquitectura. A 3 veces el promedio, el sistema degrada por prioridad y descarta clases de menor SLA, pero no cae ni pierde solicitudes admitidas. Ambos escenarios se ejecutan como prueba de carga antes del pico, no durante. | Paola, incident manager | PD-13 |
| NFR-CAP-03 | Las colas son persistentes y están dimensionadas para al menos 30 minutos de acumulación a carga de pico. Al alcanzar el 80% de su capacidad se alerta y se activa el descarte por prioridad, antes del punto en que ya no se puede admitir una solicitud crítica. | Martín, dueño del harness | PD-13 |

## Frescura y consistencia del dato

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-FRE-01 | Un cambio de estado de un incidente se refleja en las respuestas con p95 ≤ 5 s y p99 ≤ 15 s. En el camino de lectura directa contra el sistema de registro la ventana es cero: la respuesta refleja el estado vigente al instante de la lectura. La prueba es la queja original: cerrar un incidente y preguntar por él enseguida no puede devolver "abierto". | Camila, ingeniera de soporte | PD-6, PD-7 |
| NFR-FRE-02 | Cuando el estado se sirve desde una réplica de lectura —solo durante un relevo— el retraso de la réplica se declara en la respuesta y no supera 30 s. Superado ese umbral, la consulta se rechaza con motivo en lugar de entregar un dato viejo sin advertirlo. Ninguna respuesta afirma un estado sin decir de cuándo es. | Camila, ingeniera de soporte | PD-6 |

## Determinismo y calidad de la respuesta

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-DET-01 | Sobre el conjunto de preguntas frecuentes, veinte ejecuciones consecutivas de la misma pregunta devuelven la misma respuesta literal mientras la evidencia y las versiones no cambien. Una diferencia entre ejecuciones es un defecto, no una variación aceptable del modelo. | Camila, ingeniera de soporte | PD-9 |
| NFR-DET-02 | Ninguna respuesta se genera con una versión de modelo o de plantilla que no haya pasado la evaluación y esté publicada. Cada cambio de versión queda fechado, de modo que una diferencia de respuesta entre dos semanas siempre tiene una causa identificable. En el conjunto de evaluación, ninguna versión publicada empeora exactitud, abstención correcta ni procedencia respecto de la vigente. | Martín, dueño del harness | PD-10 |
| NFR-DET-03 | El 100% de las respuestas entregadas incluye procedencia verificable. Una afirmación sin incidente citado, sin versión del dato y sin hora de lectura no se entrega: se convierte en abstención. | Paola, incident manager | PD-8 |

## Seguridad de las acciones y del dato

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-SEC-01 | El 100% de las llamadas a herramientas atraviesa el Action Guard. En una batería de al menos 50 intentos de inyección —instrucciones ocultas en el cuerpo del incidente, en comentarios del cliente y en adjuntos de texto— el número de acciones destructivas ejecutadas es cero, y el 100% de los intentos queda registrado como evento de seguridad. | Camila, ingeniera de soporte | PD-5 |
| NFR-SEC-02 | Ninguna credencial utilizada por el harness tiene permisos de definición de esquema, y el acceso por defecto a cualquier sistema es de solo lectura. La escritura se obtiene por la identidad del ingeniero y su rol, para la operación concreta autorizada. El inventario de credenciales y permisos se revisa cada periodo y la revisión queda registrada. | Paola, incident manager | PD-4 |
| NFR-SEC-03 | Una acción destructiva exige aprobación de una persona distinta del solicitante y su ventana de aprobación caduca en 15 minutos. Ninguna acción destructiva se ejecuta sin un registro completo de solicitante, aprobador, alcance simulado y resultado. Sin aprobador disponible, la acción no se ejecuta: no existe modo de emergencia que salte el control. | Paola, incident manager | PD-3 |
| NFR-SEC-04 | El detalle de los incidentes no sale de la red corporativa: prompts, evidencia recuperada y respuestas se almacenan y procesan dentro. Lo que se publica en Slack son referencias —identificador, clase y enlace—, no el detalle del incidente, porque Slack es un servicio externo. Un intento de publicar detalle se bloquea y se registra. | Paola, incident manager | PD-2 |

## Recuperación

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-REC-01 | Una acción destructiva ejecutada por error se revierte en ≤ 60 minutos, con pérdida de datos ≤ 5 minutos. Se verifica en simulacro al menos una vez por periodo, sobre datos reales restaurados en un entorno aparte, y se mide el tiempo real, no el estimado. Un procedimiento de reversión que nunca se ejecutó no cuenta como cumplido. | Paola, incident manager | PD-3 |
| NFR-REC-02 | El relevo del sistema de registro se completa en ≤ 2 minutos sin pérdida de transacciones confirmadas. Durante el relevo, las consultas de estado se sirven desde la réplica bajo las condiciones de `NFR-FRE-02` y las escrituras se rechazan con motivo. El simulacro de relevo se ejecuta por periodo con la aplicación en funcionamiento. | Martín, dueño del harness | PD-14 |

## Auditoría y observabilidad

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-AUD-01 | El 100% de consultas y acciones queda en un registro append-only con actor, incidente, evidencia usada, versión de prompt y de modelo, herramienta invocada, aprobación y resultado, retenido 12 meses. El harness no tiene permiso para modificar ni borrar ese registro. El criterio de suficiencia es concreto: reconstruir el incidente del borrado de la base de datos usando solo la bitácora. | Paola, incident manager | PD-15 |
| NFR-AUD-02 | El orden temporal de la auditoría lo establece el reloj del servidor, sincronizado por NTP. Un desfase superior a 1 s se alerta. Ningún identificador de solicitud, acción o generación depende del reloj para ser único. | Paola, incident manager | PD-15 |
| NFR-OBS-01 | Se miden por clase de escalamiento: latencia p95 y p99, tasa de error, profundidad de cola, saturación de inferencia, tasa de consultas resueltas sin modelo, tasa de abstención, acciones propuestas y rechazadas por el Guard, y estado de cada cortacircuito. La alerta se emite al 80% de cualquier umbral, antes del punto en que la degradación ya es visible para el usuario. | Martín, dueño del harness | PD-12 |
| NFR-OBS-02 | Cada solicitud tiene un `requestId` que atraviesa entrada, clasificación, recuperación, inferencia y herramientas, de modo que una consulta se reconstruye extremo a extremo. El `requestId` nace en la entrada del harness y no cambia si la solicitud se encola o se reintenta. | Martín, dueño del harness | PD-15 |

## Uso

| ID | Requerimiento y verificación | Usuario responsable | PD |
| --- | --- | --- | --- |
| NFR-USA-01 | Al probar con cinco ingenieros, al menos cuatro distinguen una respuesta degradada de una completa, entienden qué significa una abstención y saben qué hacer a continuación, y verifican una afirmación abriendo el incidente citado sin volver a preguntarle al sistema. | Camila, ingeniera de soporte | PD-13 |
| NFR-USA-02 | Un rechazo —por presupuesto de latencia, por descarte de prioridad, por permisos o por falta de aprobación— siempre indica motivo y siguiente paso. Ningún camino de fallo termina en un mensaje de error genérico. | Andrés, ingeniero de guardia | PD-13 |

## Alcance declarado

No se compromete disponibilidad total, recuperación ante desastre regional ni
redundancia del centro de datos. El diseño tolera la falla de cualquier
componente del harness y del sistema de registro dentro de un mismo sitio.

Tres supuestos que el enunciado no da y el diseño necesita, declarados aquí para
que no pasen por hechos:

1. La capacidad de inferencia es fija y escasa. Todas las metas de latencia se
   sostienen sobre el supuesto de que el 60% de las consultas no invoca al
   modelo. Si esa proporción resulta menor en producción, la meta que cede
   primero es `NFR-PER-03`, no `NFR-PER-02`.
2. La base de datos de incidentes admite réplica y recuperación a un punto en el
   tiempo. `NFR-REC-01` y `NFR-REC-02` dependen de eso; sin esa capacidad, la
   promesa de reversión no es sostenible y habría que restringir aún más las
   acciones de escritura.
3. La frecuencia real del pico está estimada, no medida: se asume que la primera
   semana concentra el 40% del volumen mensual. `FR-REL-13` existe precisamente
   para corregir ese supuesto con lo observado en cada ciclo.
