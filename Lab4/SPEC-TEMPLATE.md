# SPEC TEMPLATE — RemoteSchooly

## Summary

RemoteSchooly lleva el material semanal de Lima a escuelas con Internet limitado e intermitente. La central publica contenido versionado y cada Nodo Escolar Local sincroniza por HTTPS en bloques reanudables; conserva la última versión válida para docentes y alumnos durante un corte. El mismo sistema reduce el costo de IA: convierte el pedido docente en una solicitud estructurada, pregunta solo lo que falta y envía al proveedor un prompt breve y acotado.

## Problem and objective

Las escuelas remotas sí tienen Internet, pero no pueden depender de una transferencia continua ni de volver a descargar todo después de un corte. Los materiales deben llegar por red, activarse solo después de validar integridad y seguir disponibles desde el nodo local. A la vez, usar IA con instrucciones libres, repetidas y ambiguas consume más tokens de los necesarios. El objetivo es sincronizar correctamente el curso y reducir los tokens externos al menos 40% frente a la misma carga sin optimización.

## Product concepts

| Concepto | Definición |
| --- | --- |
| Paquete semanal | Versión lógica de recursos con manifiesto, hashes y firma publicada por Internet. |
| Nodo Escolar Local | Servidor/appliance de la escuela que sincroniza por HTTPS y publica la última versión válida en LAN/Wi-Fi. |
| Sincronización reanudable | Transferencia por rangos que persiste bloques validados y continúa después de un corte. |
| Cola local | Registro duradero de avances, incidencias y solicitudes pendientes de enviar cuando vuelva la red. |
| Solicitud intermedia | Archivo JSON estructurado que representa la intención docente antes de llamar a IA. |
| Clarification Gate | Validación local que pregunta campos críticos faltantes y no usa tokens externos. |
| Context Builder | Componente que selecciona el mínimo de fragmentos curriculares necesarios. |
| Línea base | Tokens medidos sobre las mismas tareas, modelo y versión de contenido sin el Gateway. |

## Key decisions

1. La distribución es exclusivamente por red; no se usan transportistas ni medios físicos.
2. El Nodo consulta manifiestos, obtiene únicamente diferencias y descarga con HTTP Range/HTTPS; un corte no reinicia bloques ya validados.
3. Texto, guías y actividades tienen prioridad sobre multimedia opcional para que el curso esencial llegue primero.
4. Firma y hash evitan publicar una versión parcial o alterada. La última versión `READY` permanece disponible durante el corte.
5. Las acciones creadas sin red entran a una cola local y se sincronizan de forma idempotente al recuperar conectividad.
6. La solicitud intermedia reemplaza la pregunta larga por campos concretos y una plantilla determinista; no es un “resumen con IA” oculto.
7. La IA se llama solo después de que los datos críticos estén completos. Las aclaraciones son preguntas cortas, visibles y sin consumo externo.
8. Se recuperan fragmentos curriculares etiquetados, no el curso completo. Cada llamada tiene presupuestos de entrada y salida.

## Main happy paths

### A. Material semanal por Internet limitado

1. Valeria publica el manifiesto y archivos versionados en Lima.
2. Cuando tiene conectividad, el Nodo Escolar Local consulta el manifiesto y calcula qué archivos cambiaron.
3. Descarga primero guía, ficha y actividad en bloques reanudables; un corte conserva los bloques ya verificados.
4. Tras validar firma y hashes, activa la nueva versión completa como `READY` y confirma la sincronización a Lima.
5. Rosa y Diego usan el catálogo local por Wi-Fi/LAN. Si se corta Internet, continúan con la última versión `READY`.
6. Avances e incidencias quedan en la cola local durante el corte y se envían una vez al recuperar red.

### B. Solicitud IA de bajo costo

1. Rosa elige grado, curso y tipo de recurso, e indica objetivo, duración y formato.
2. El Clarification Gate valida los campos. Si falta, por ejemplo, el grado o duración, pregunta exactamente eso y detiene el flujo sin llamar a IA.
3. El Prompt Rewriter elimina repeticiones y genera `solicitud_ia.json`; el Context Builder añade solo fragmentos etiquetados para ese objetivo.
4. El Budget Guard calcula el máximo permitido. Si el prompt no cabe, muestra qué reducir; si cabe, el AI Gateway invoca el modelo cuando la conexión está disponible.
5. El resultado se guarda con la huella de solicitud, plantilla y versión curricular. Una solicitud equivalente reutiliza el resultado.
6. Valeria compara los tokens externos acumulados con la línea base y acepta la iteración únicamente cuando la reducción es ≥ 40%.

## States

### Sincronización de paquete

`PUBLISHED → CHECKING → DOWNLOADING → VERIFYING → READY`.

Un corte lleva a `PAUSED`; al volver la red se retoma `DOWNLOADING`. Un hash o firma inválidos llevan a `REJECTED`; la última versión `READY` no se reemplaza.

### Solicitud IA

`DRAFT → NEEDS_CLARIFICATION → READY → CACHE_HIT | SENT → GENERATED → APPROVED`.

`BUDGET_EXCEEDED`, `PENDING_NETWORK` y `REJECTED` no llaman al proveedor. Una respuesta que no satisfaga a Rosa se marca `REVISE`, crea una nueva solicitud y conserva la trazabilidad.

## Acceptance criteria

1. Con una versión con un solo archivo cambiado, el nodo descarga solo el manifiesto y ese archivo.
2. Tras simular un corte, la descarga se reanuda desde el siguiente bloque pendiente, sin repetir bloques validados.
3. Un paquete alterado no llega a `READY` ni reemplaza la versión visible.
4. Durante un corte, un estudiante abre la última guía `READY` desde la LAN.
5. Una incidencia creada sin red pasa a `PENDING_SYNC` y se entrega una sola vez al recuperar conexión.
6. Una petición que omite grado o duración recibe una aclaración y cero llamadas externas.
7. El prompt final contiene la plantilla y solo los fragmentos curriculares registrados como pertinentes.
8. Toda llamada respeta un presupuesto de tokens y registra consumo de entrada/salida.
9. El reporte usa al menos 30 tareas equivalentes y demuestra reducción de tokens externos ≥ 40%.

## Scope by stages

| Etapa | Incluye |
| --- | --- |
| POC | Manifiesto, simulación de HTTP Range, reanudación, catálogo local, cola de pendientes, formulario intermedio, aclaraciones deterministas y reporte de token simulado. |
| Piloto | Almacenamiento HTTPS real, Nodo en una escuela, telemetría de cortes, proveedor IA sandbox, caché y medición con tareas docentes reales. |
| Producción | Observabilidad de red, gestión de dispositivos, seguridad reforzada, analítica, políticas de retención y acuerdos con proveedores. |
