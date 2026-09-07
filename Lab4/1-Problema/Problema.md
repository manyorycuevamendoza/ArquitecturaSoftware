# Problema, alcance y supuestos

## Problema

RemoteSchooly distribuye materiales semanales desde Lima a escuelas remotas que sí tienen acceso a Internet, pero con poco ancho de banda y cortes frecuentes. Una descarga convencional puede reiniciarse, consumir nuevamente los datos disponibles o dejar al docente con una versión incompleta. El curso debe llegar correctamente por la red y continuar disponible localmente durante un corte.

Además, los docentes generan materiales con IA a través de la plataforma y envían preguntas extensas, repetidas o incompletas. Esto incrementa los tokens de entrada y salida y eleva el costo. El caso exige reducir el gasto de tokens en al menos 40%.

## Objetivo

Distribuir por Internet versiones semanales verificables que se descarguen por partes, se reanuden tras un corte y queden disponibles en la escuela; permitir también que el docente genere material con IA mediante solicitudes concretas, contexto mínimo necesario y consumo medible de tokens.

## Alcance

- Publicar desde Lima un manifiesto y archivos versionados por región, escuela, grado y curso.
- Sincronizar el Nodo Escolar Local por Internet mediante descargas segmentadas y reanudables.
- Priorizar texto, guías y actividades sobre multimedia opcional cuando el ancho de banda sea limitado.
- Mantener disponible la última versión verificada en el nodo durante un corte.
- Verificar hash y firma antes de activar una nueva versión y enviar confirmación cuando la conectividad vuelva.
- Encolar avances, incidencias y solicitudes creadas durante un corte, y sincronizarlos después por la red.
- Guiar al docente con una solicitud intermedia estructurada antes de usar IA.
- Reformular la petición, recuperar solo el fragmento curricular necesario, limitar tokens, reutilizar resultados y registrar el consumo.
- Preguntar al docente únicamente por campos faltantes que impiden producir una respuesta útil.
- Medir la reducción de tokens contra una línea base comparable y bloquear o ajustar el flujo si no alcanza la meta.

## Fuera de alcance

- Distribución física de contenidos mediante USB, SSD, tarjetas o transportistas.
- Internet satelital y la construcción de nueva infraestructura de conectividad para la comunidad.
- Disponibilidad 100%, recuperación ante desastre o redundancia completa del proveedor de conectividad.
- Autenticación nacional de estudiantes, notas oficiales, videollamadas y clases en vivo.
- Entrenar un modelo de IA propio, negociar precios con el proveedor o garantizar calidad pedagógica absoluta de toda respuesta generada.

## Supuestos que condicionan el diseño

1. Cada escuela tiene Internet intermitente y limitado, y un equipo que puede operar como Nodo Escolar Local y conservar una caché de contenidos.
2. La sincronización dispone de intervalos acumulados de conectividad suficientes para completar el paquete semanal. El diseño reduce y reanuda transferencia; no crea conectividad donde no exista.
3. La central de Lima publica los archivos en almacenamiento accesible por HTTPS. El Nodo Escolar Local puede solicitar rangos de bytes y retomar una descarga desde el último bloque validado.
4. La línea base de tokens se obtiene ejecutando el mismo conjunto de solicitudes docentes sin el AI Gateway. Los tokens se comparan por tarea, modelo y versión de contenido equivalentes.
5. La reformulación, validación de campos y selección de plantillas no invocan el modelo externo. Si en el futuro se usara un modelo para resumir, sus tokens también se sumarían a la métrica de costo.
