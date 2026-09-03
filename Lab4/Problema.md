# Problema, alcance y supuestos

## Problema

RemoteSchooly debe llevar los materiales de cada semana desde una central en Lima a escuelas de pueblos remotos donde puede no existir Internet. Una plataforma que dependa de descargar contenidos o de consultar un servicio remoto en la escuela deja a docentes y alumnos sin curso cuando más lo necesitan.

Además, los docentes generan materiales con IA a través de la plataforma y envían preguntas extensas, repetidas o incompletas. Esto incrementa los tokens de entrada y salida y eleva el costo. El caso exige reducir el gasto de tokens en al menos 40%.

## Objetivo

Entregar a tiempo paquetes semanales de curso verificables y utilizables sin Internet, y permitir que el docente produzca material asistido por IA con solicitudes concretas, contexto mínimo necesario y consumo medible de tokens.

## Alcance

- Preparar en Lima paquetes semanales por región, grado y curso.
- Transportar físicamente los paquetes a la escuela y cargarlos en un Nodo Escolar Local.
- Permitir a docentes y alumnos consultar y descargar el material por Wi-Fi/LAN local, sin conexión externa.
- Verificar versión, firma y hash antes de publicar un paquete a estudiantes.
- Devolver avances, incidencias y solicitudes de contenido mediante un paquete de retorno físico.
- Guiar al docente con una solicitud intermedia estructurada antes de usar IA.
- Reformular localmente la petición, recuperar solo el fragmento curricular necesario, limitar tokens, reutilizar resultados y registrar el consumo.
- Preguntar al docente únicamente por campos faltantes que impiden producir una respuesta útil.
- Medir la reducción de tokens contra una línea base comparable y bloquear/ajustar el flujo si no alcanza la meta.

## Fuera de alcance

- Internet satelital, radioenlaces, redes móviles, enlaces comunitarios u otro mecanismo para llevar Internet a la escuela remota.
- Disponibilidad 100%, alta disponibilidad, recuperación ante desastre o mecanismos completos de confiabilidad del transporte.
- Autenticación nacional de estudiantes, notas oficiales, videollamadas y clases en vivo.
- Entrenar un modelo de IA propio, negociar precios con el proveedor o garantizar calidad pedagógica absoluta de toda respuesta generada.

## Supuestos que condicionan el diseño

1. Cada escuela cuenta con electricidad y un equipo que puede operar como Nodo Escolar Local; si no la tiene, esa provisión física se gestiona fuera del alcance.
2. Un transportista regional puede visitar la escuela al menos una vez por semana. El paquete viaja en SSD, USB o tarjeta SD sellada; **no requiere ni habilita Internet**.
3. La central de Lima sí dispone de conectividad para preparar contenidos e invocar el proveedor de IA. Una escuela remota puede preparar solicitudes que se procesan en la próxima visita, pero no necesita conectarse para estudiar los materiales ya entregados.
4. La línea base de tokens se obtiene ejecutando el mismo conjunto de solicitudes docentes sin el AI Gateway. Los tokens se comparan por tarea, modelo y versión de contenido equivalentes.
5. La reformulación, validación de campos y selección de plantillas no invocan el modelo externo. Si en el futuro se usara un modelo para resumir, sus tokens también se sumarían a la métrica de costo.
