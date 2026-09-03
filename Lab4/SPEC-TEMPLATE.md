# SPEC TEMPLATE — RemoteSchooly

## Summary

RemoteSchooly lleva el material semanal de la central de Lima a escuelas remotas sin depender de Internet en el destino. Un paquete firmado viaja físicamente y se instala en un Nodo Escolar Local, desde el cual alumnos y docentes lo consumen por Wi-Fi/LAN. El mismo sistema reduce el costo de IA: convierte el pedido docente en una solicitud estructurada, pregunta solo lo que falta y envía al proveedor un prompt breve y acotado.

## Problem and objective

Las escuelas remotas no pueden depender de una descarga, una videollamada ni una API para tener el curso de la semana. A la vez, usar IA con instrucciones libres, repetidas y ambiguas consume más tokens de los necesarios. El objetivo es que los materiales correctos lleguen sin Internet y que el consumo externo de tokens disminuya al menos 40% respecto a la misma carga de solicitudes sin optimización.

## Product concepts

| Concepto | Definición |
| --- | --- |
| Paquete semanal | Archivo físico versionado con recursos, manifiesto, hashes y firma para una escuela. |
| Nodo Escolar Local | Servidor/appliance de la escuela que publica materiales en LAN/Wi-Fi sin salida a Internet. |
| Paquete de retorno | Archivo físico que contiene avances, incidencias y solicitudes creadas offline. |
| Solicitud intermedia | Archivo JSON estructurado que representa la intención docente antes de llamar a IA. |
| Clarification Gate | Validación local que pregunta campos críticos faltantes y no usa tokens externos. |
| Context Builder | Componente que selecciona el mínimo de fragmentos curriculares necesarios. |
| Prompt canónico | Instrucción final con plantilla, contexto permitido y presupuesto de tokens. |
| Línea base | Tokens medidos sobre las mismas tareas, modelo y versión de contenido sin el Gateway. |

## Key decisions

1. La escuela remota no recibe Internet por ningún medio. La distribución y el retorno son físicos.
2. El Nodo Escolar Local sirve contenido en la red local; no intenta sincronizarse automáticamente con Lima.
3. Firma + hash prueban que el paquete recibido corresponde a una versión publicada; el paquete no se publica si falla la verificación.
4. La solicitud intermedia reemplaza la pregunta larga por campos concretos y una plantilla determinista; no es un “resumen con IA” oculto.
5. La IA se llama solo después de que los datos críticos estén completos. Las aclaraciones son preguntas cortas, visibles y sin consumo externo.
6. Se recuperan fragmentos curriculares etiquetados, no el curso completo. Cada llamada tiene presupuestos de entrada y salida.
7. El ahorro se valida comparando tokens realmente facturados, no por estimación. Caché, reformulación y resultados reutilizados cuentan como parte del Gateway.

## Main happy paths

### A. Material semanal sin Internet

1. Valeria selecciona contenidos por escuela, región, grado y semana.
2. La central genera `packageId`, manifiesto, hashes y firma; el medio físico queda registrado para el transportista.
3. El transportista entrega el medio en la escuela.
4. El administrador lo importa en el Nodo Escolar Local, que verifica firma y hashes sin conectarse a ningún servicio.
5. Tras una verificación válida, Rosa y Diego navegan al catálogo local, descargan y usan la versión vigente por Wi-Fi/LAN.
6. Rosa registra avances o incidencias; el nodo los exporta en un paquete de retorno para el siguiente viaje.

### B. Solicitud IA de bajo costo

1. Rosa elige grado, curso y tipo de recurso, e indica objetivo, duración y formato.
2. El Clarification Gate valida los campos. Si falta, por ejemplo, el grado o duración, pregunta exactamente eso y detiene el flujo sin llamar a IA.
3. El Prompt Rewriter elimina repeticiones y genera `solicitud_ia.json`; el Context Builder añade solo fragmentos etiquetados para ese objetivo.
4. El Budget Guard calcula el máximo permitido. Si el prompt no cabe, muestra qué reducir; si cabe, el AI Gateway invoca el modelo en Lima.
5. El resultado se guarda con la huella de solicitud, plantilla y versión curricular. Una solicitud equivalente reutiliza el resultado.
6. Valeria compara los tokens externos acumulados con la línea base y acepta la iteración únicamente cuando la reducción es ≥ 40%.

## States

### Paquete semanal

`DRAFT → SIGNED → DISPATCHED → RECEIVED → VERIFIED → PUBLISHED`.

Una validación fallida termina en `REJECTED`; el último paquete `PUBLISHED` se mantiene visible. No se afirma tolerancia automática al extravío físico.

### Solicitud IA

`DRAFT → NEEDS_CLARIFICATION → READY → CACHE_HIT | SENT → GENERATED → APPROVED`.

`BUDGET_EXCEEDED` y `REJECTED` no llaman al proveedor. Una respuesta que no satisfaga a Rosa se marca `REVISE`, crea una nueva solicitud y conserva la trazabilidad.

## Acceptance criteria

1. Con WAN desconectada, un estudiante abre materiales publicados desde la LAN.
2. Un paquete modificado no se publica.
3. Un paquete válido reemplaza la versión visible de forma completa, sin mezclar archivos.
4. Una incidencia creada offline aparece en el paquete de retorno exportado.
5. Una petición que omite grado o duración recibe una aclaración y cero llamadas externas.
6. El prompt final contiene la plantilla y solo los fragmentos curriculares registrados como pertinentes.
7. Toda llamada respeta un presupuesto de tokens y registra consumo de entrada/salida.
8. Una solicitud equivalente reutiliza el resultado sin una llamada nueva.
9. El reporte usa al menos 30 tareas equivalentes y demuestra reducción de tokens externos ≥ 40%.

## Scope by stages

| Etapa | Incluye |
| --- | --- |
| POC | Importación local simulada, manifiesto/hash, catálogo LAN, formulario intermedio, aclaraciones deterministas, prompt canónico y reporte de token simulado. |
| Piloto | Firma real, medios físicos, nodo en una escuela, proveedor IA sandbox, caché y medición con tareas docentes reales. |
| Producción | Gestión de inventario/logística, gobierno curricular nacional, continuidad eléctrica, seguridad reforzada, analítica y acuerdos con proveedores. |
