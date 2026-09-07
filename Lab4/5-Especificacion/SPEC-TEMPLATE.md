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

Un recorrido por usuario, no por problema: cada uno arranca en la persona y cada
paso cita el requisito que lo respalda. Los requisitos están en
[../3-Requerimientos/](../3-Requerimientos/Functional.md).

### 1. Valeria, coordinadora de contenidos

Publica una versión correcta, audita qué llegó a cada escuela y demuestra el ahorro.

| # | Paso | Requisitos |
| ---: | --- | --- |
| 1 | Entra con su cuenta. El rol de coordinadora es lo único que habilita publicar contenido y editar plantillas de prompt. | `FR-AI-09`, `NFR-SEC-01` |
| 2 | Carga el material de la semana 12. El CMS arma el manifiesto con la lista **completa** de lo que la escuela debe tener a esa fecha, el hash de cada archivo, y lo firma. | `FR-DIS-01` |
| 3 | Retira del currículo un tema que ya no va. Basta con sacarlo del manifiesto: lo que no está en la lista se borra de la caché de la escuela. | `FR-DIS-01`, `FR-DIS-02` |
| 4 | Publica una plantilla de prompt para el año nuevo. La anterior queda histórica y no se borra: la necesita para auditar en qué se gastó el presupuesto del periodo en que estuvo vigente. | `FR-AI-10` |
| 5 | Abre el panel y ve, por escuela, qué versión está activa y cuántas semanas de atraso lleva. El orden lo pone la hora de la central, no la del nodo. | `FR-DIS-08`, `NFR-AUD-01`, `NFR-AUD-02` |
| 6 | Revisa el consumo de IA desagregado por docente, curso y escuela. Cada llamada quedó registrada con su `requestId`, modelo, tokens y costo; los aciertos de caché y los bloqueos figuran con cero. | `FR-AI-07`, `FR-AI-14`, `FR-AI-15` |
| 7 | Corre el reporte de reducción sobre 30 tareas. Descarta las que no comparten tarea, modelo y versión curricular, y aprueba la meta solo si la reducción es ≥ 40%. | `FR-AI-08`, `NFR-COST-01`, `NFR-COST-03` |

### 2. Rosa, docente rural

Enseña en la fecha que toca, con o sin señal, y pide material sin perder tiempo ni gastar de más.

| # | Paso | Requisitos |
| ---: | --- | --- |
| 1 | Llega el lunes y no hay señal. Entra igual: la sesión se resuelve contra la réplica local de identidad y cuota que guarda el nodo. | `FR-AI-13` |
| 2 | Abre la guía de la semana. El nodo se la sirve desde la caché por WiFi, sin tocar Internet. | `FR-DIS-05`, `NFR-AVL-01` |
| 3 | A media mañana vuelve la señal. El nodo no se lanza a descargar: es horario de clase, así que sincroniza con tope de ancho de banda para no degradar lo que ya está en la caché. | `FR-DIS-10`, `NFR-NET-03` |
| 4 | Pide a la IA una ficha de comprensión lectora. Llena el formulario: objetivo, grado, curso, tipo de recurso, duración y formato. | `FR-AI-01` |
| 5 | El Gateway evalúa en orden: plantilla vigente, cuota disponible, campos obligatorios. Le falta la duración, así que le pregunta solo eso. Cuesta cero tokens externos. | `FR-AI-03` |
| 6 | Con los campos completos se arma el archivo intermedio: se descarta el saludo, se descarta lo que ya viaja como campo, y del temario entero entran solo los dos fragmentos etiquetados. | `FR-AI-02`, `FR-AI-04` |
| 7 | Antes de presupuestar, se busca la huella en la caché. No está, así que se evalúan los presupuestos de entrada y de salida y se invoca al modelo una sola vez. | `FR-AI-06`, `FR-AI-05`, `NFR-COST-02` |
| 8 | Si el pedido no cupiera en el presupuesto, el sistema le explicaría qué recortar y no reintentaría solo. Si el proveedor no respondiera, la solicitud esperaría con su cuota todavía reservada. | `FR-AI-12`, `FR-AI-16` |
| 9 | Si la red se cayera en ese momento, la solicitud quedaría en cola con la cuota reservada y se revalidaría al volver la conexión. | `FR-AI-11`, `NFR-COST-04`, `NFR-USA-01` |

### 3. Diego, estudiante

Accede al curso completo aunque Internet se caiga, y su avance no se pierde ni se cuenta dos veces.

| # | Paso | Requisitos |
| ---: | --- | --- |
| 1 | Abre la app en la sala de cómputo. El nodo le sirve el catálogo por LAN; con 29 compañeros conectados, la portada de una guía abre en menos de 3 segundos. | `NFR-AVL-01`, `NFR-PER-01` |
| 2 | La escuela estuvo tres semanas sin señal. Al volver, el nodo compara su manifiesto local contra el más reciente y descarga el acumulado, sin aplicar las versiones intermedias. | `FR-DIS-02`, `FR-DIS-09` |
| 3 | Diego no pierde el material de esas semanas: sigue vigente en el manifiesto de la semana 12. | `FR-DIS-01`, `FR-DIS-09` |
| 4 | Primero bajan la guía, la ficha y la actividad. El video queda para el final. | `FR-DIS-04`, `NFR-NET-02` |
| 5 | La transferencia se corta a mitad. Al volver la señal, el nodo pide solo los rangos que faltan; no reinicia desde cero. | `FR-DIS-03`, `NFR-NET-01` |
| 6 | Un archivo llega corrupto. Se rechaza y no se activa nada: Diego sigue viendo la versión anterior completa, no una mezcla. | `FR-DIS-05`, `NFR-INT-01`, `NFR-INT-02` |
| 7 | Con todo lo esencial verificado, el nodo mueve el puntero de versión. Si se corta la luz en ese instante, Diego arranca viendo la anterior completa o la nueva completa, nunca media. | `FR-DIS-07`, `NFR-INT-03` |
| 8 | Termina una actividad un martes sin red. El avance queda en la cola con un identificador que se fijó al **crearlo**, no al enviarlo. | `FR-DIS-06` |
| 9 | El jueves la cola se envía. El primer intento se corta y el nodo reintenta con el mismo identificador. La central lo reconoce, valida el contenido y lo registra una sola vez. | `FR-DIS-06`, `FR-DIS-13` |

### 4. Administrador regional

Dimensiona y supervisa el nodo de la escuela sin tener que viajar hasta ella.

| # | Paso | Requisitos |
| ---: | --- | --- |
| 1 | Instala un nodo en una escuela que nunca tuvo material. Durante el aprovisionamiento le carga la llave pública de la central, por un canal distinto al del contenido. | `FR-DIS-12` |
| 2 | Verifica que el nodo tenga al menos 8 GB: la activación atómica necesita la versión activa y la nueva al mismo tiempo. | `NFR-CAP-01` |
| 3 | El nodo hace su primera carga. No hay versión anterior con la cual respaldarse, así que si la firma no validara se marcaría el estado y se alertaría a la central en lugar de servir contenido sin verificar. | `FR-DIS-05`, `NFR-INT-01` |
| 4 | Programa la ventana de sincronización. Cada escuela entra tras una espera aleatoria propia, para que las 500 no le caigan juntas al almacenamiento central. | `FR-DIS-10`, `NFR-NET-04` |
| 5 | Meses después el disco llega al 85%. El nodo le avisa y frena la descarga de lo opcional, antes del punto en que ya no se podría escribir ni el registro del fallo. | `NFR-CAP-02` |
| 6 | Libera espacio en orden: multimedia vieja, después versiones antiguas completas. Nunca la versión activa ni la cola de eventos, porque el avance de los estudiantes no existe en ningún otro lado. | `FR-DIS-11` |
| 7 | La central rota la llave de firma. El nodo acepta la anterior y la nueva durante el periodo de solapamiento, así que no hace falta reinstalar nada. | `NFR-SEC-02` |

### Cobertura

Los cuatro recorridos ejercitan los 49 requisitos definidos. Ninguno queda sin
un camino feliz que lo recorra, y ningún paso se apoya en algo que no esté
exigido.

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
