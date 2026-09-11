# Problema, alcance y supuestos

## Problema

Genius es la plataforma con la que la compañía maneja sus incidentes diarios:
*customer escalations* (reportadas por el cliente, con impacto directo en
negocio), *engineering escalations* (reportadas por ingeniería para sí misma o
para otras áreas) y *support escalations* (reportadas por clientes pero ya
procesadas por soporte).

Como el detalle de los incidentes es extenso y no puede salir de la compañía,
data science desplegó un **LLM local** y expuso una API para que el área de
incidentes lo consulte y, además, ejecute acciones: consultas a base de datos,
pruebas E2E y publicación en Slack. El harness actual es solo eso: la API, el
LLM y dos servidores MCP —base de datos y Slack— conectados directamente.

Ese harness falla de cinco maneras observadas, y las cinco son de confiabilidad,
no de calidad del modelo:

1. **Una acción destructiva se ejecutó sin control.** Un ingeniero de soporte
   dio instrucciones para atender un escalamiento de un cliente y el LLM
   decidió borrar la base de datos. Entre la decisión del modelo y el daño real
   no había nada: ni clasificación de riesgo, ni aprobación humana, ni límite de
   privilegios, ni forma de deshacerlo.
2. **El sistema no aprende.** Las mismas correcciones se repiten todas las
   semanas porque no existe ningún lugar donde una respuesta corregida quede
   guardada, ni ninguna medición que diga si la siguiente versión responde mejor
   o peor que la anterior.
3. **La primera semana de cada mes el LLM no responde o responde mal.** Es el
   pico de incidentes: la capacidad de inferencia se satura, las consultas se
   encolan sin prioridad y una consulta crítica de un cliente espera detrás del
   trabajo rutinario de ingeniería.
4. **La misma pregunta recibe respuestas distintas.** Hay un conjunto de
   preguntas frecuentes que cada día se contestan diferente, y ninguna de las
   dos versiones es verificable contra una fuente.
5. **Genius responde con el estado de un incidente cerrado hace horas.** El dato
   que el modelo usa para responder no es el dato vigente en el sistema de
   registro.

## Objetivo

Diseñar un **harness nuevo alrededor del LLM** —el conjunto de componentes que
lo rodean y que determinan su confiabilidad, su rendimiento y la experiencia de
uso— de modo que Genius siga respondiendo durante los picos y las fallas, no
ejecute acciones destructivas sin control humano, responda lo mismo a la misma
pregunta y nunca afirme un estado que ya no es el vigente.

El LLM se trata como un **componente no confiable por diseño**: no determinista,
influenciable por el texto del incidente que lee y capaz de proponer acciones
equivocadas. La confiabilidad no se le pide al modelo; se construye alrededor
de él.

## Alcance

- Clasificar cada solicitud por tipo de escalamiento y por criticidad, y
  atenderla por un camino acorde a su SLA.
- Separar el camino de **lectura** (responder con datos) del camino de
  **acción** (cambiar algo en un sistema), y gobernar cada uno por separado.
- Clasificar toda herramienta expuesta al LLM por nivel de riesgo, y exigir
  aprobación humana y ejecución reversible para las destructivas.
- Ejecutar las acciones con la identidad y los privilegios del ingeniero que las
  pide, nunca con una credencial única y omnipotente del harness.
- Impedir que el texto de un incidente sea interpretado como una instrucción.
- Responder el estado de un incidente contra la fuente de registro, con su
  marca de versión, y no desde un índice o una caché sin validar.
- Recuperar evidencia antes de generar, y abstenerse cuando no hay evidencia.
- Fijar respuestas canónicas para el conjunto de preguntas frecuentes y
  reutilizarlas mientras los datos que las sustentan no cambien.
- Sostener el pico de la primera semana del mes con colas por prioridad,
  aislamiento entre clases de tráfico, descarte controlado y degradación a una
  respuesta útil sin modelo.
- Tolerar la caída de cualquier componente del harness sin que Genius deje de
  responder consultas de estado.
- Registrar de forma inmutable cada consulta, cada llamada a herramienta y cada
  aprobación, y medir la calidad de las respuestas contra un conjunto fijo de
  preguntas con respuesta conocida.

## Fuera de alcance

- Entrenar o afinar (*fine-tuning*) el modelo local. El "aprendizaje" del que se
  quejan los usuarios se resuelve con memoria curada, recuperación fresca y
  evaluación versionada, no cambiando los pesos del modelo.
- Sustituir el LLM local por un proveedor externo. El detalle de incidentes no
  puede salir de la compañía; esa restricción es de entrada, no una decisión de
  este diseño.
- Rediseñar el proceso de manejo de incidentes, la política de SLA con el
  cliente o la estructura de las áreas.
- Reemplazar Slack como canal corporativo, o construir un canal de comunicación
  propio.
- Garantizar disponibilidad 100%, recuperación ante desastre regional o
  redundancia completa del centro de datos.
- Garantizar que el modelo nunca se equivoque. El diseño acota el daño de una
  equivocación y hace que sea detectable, no la elimina.

## Supuestos que condicionan el diseño

1. El LLM local corre sobre hardware propio y limitado. Agregar réplicas cuesta
   GPU: la capacidad de generación es el recurso escaso del sistema y el diseño
   debe gastar el modelo lo menos posible.
2. Existe una base de datos de incidentes que es el **sistema de registro**: el
   estado que ella tiene es el estado verdadero. El harness lee de ahí; no
   mantiene un estado paralelo que compita con el suyo.
3. Esa base de datos admite réplica de lectura y recuperación a un punto en el
   tiempo. Sin eso, ninguna promesa de reversión del daño es sostenible.
4. Las pruebas E2E se ejecutan contra un entorno de pruebas, no contra
   producción. Si en el futuro alguna debiera correr en producción, entra en la
   clasificación de riesgo como acción de escritura.
5. Slack es un sistema externo que puede estar caído. Se usa para notificar y
   para pedir aprobaciones, pero no es la única vía: si Slack no responde, la
   aprobación sigue siendo posible dentro de Genius.
6. Los 50 a 100 ingenieros tienen identidad corporativa y rol asignado. Sin
   identidad no hay privilegios diferenciados, ni atribución de una acción, ni
   aprobación válida.
7. Existe un conjunto acotado de preguntas frecuentes —las que hoy se responden
   distinto cada día— que puede enumerarse y usarse como conjunto de evaluación.
8. Los volúmenes del piloto: 10,000 incidentes por semana en promedio, con la
   primera semana del mes concentrando cerca del 40% del volumen mensual.

## Estimaciones de carga

Supuestos de dimensionamiento, no datos del enunciado. Se declaran para que las
metas de los requisitos no funcionales sean discutibles.

| Variable | Supuesto |
| --- | ---: |
| Incidentes por semana (promedio) | 10,000 |
| Incidentes en la primera semana del mes | ~17,000 (1.7× el promedio) |
| Ingenieros concurrentes | 50 a 100 |
| Interacciones con Genius por incidente | 4 |
| Consultas en hora pico | ~1,300/h ≈ 0.4/s, con ráfagas de 3 a 5/s |
| Proporción de consultas que son estado o preguntas frecuentes | ~60% |
| Latencia de una generación completa | 6 a 10 s |
| Generaciones concurrentes por réplica del LLM | 4 |

La aritmética que ordena el diseño: una réplica que tarda 8 s y atiende 4
generaciones a la vez sostiene **0.5 consultas por segundo**. Una ráfaga de 5/s
necesitaría diez réplicas si toda consulta pasara por el modelo. No las hay. De
ahí que el 60% de consultas que son estado o preguntas frecuentes deba
resolverse **sin invocar al modelo**, y que el resto deba entrar por una cola
con prioridad en lugar de competir en desorden. El pico de la primera semana no
se resuelve comprando GPU: se resuelve no gastándola.

## Puntos de decisión

Cada requisito se resuelve en uno de estos puntos. La arquitectura los
desarrolla; aquí solo se enuncian para que las tablas de requerimientos sean
legibles por sí solas.

| PD | Decisión | Responde a |
| --- | --- | --- |
| PD-1 | El LLM **propone**, el harness **ejecuta**. Ninguna herramienta se invoca desde la salida del modelo sin pasar por un validador que la autoriza. | Borrado de la base de datos |
| PD-2 | Toda herramienta se clasifica por riesgo: lectura, escritura acotada y destructiva. La clase decide el control, no el criterio del modelo. | Borrado de la base de datos |
| PD-3 | Una acción destructiva exige simulación previa con alcance estimado, aprobación de una persona distinta de quien la pide y ejecución reversible. | Borrado de la base de datos |
| PD-4 | Las acciones corren con la identidad y los privilegios del ingeniero, no con una credencial única del harness. El acceso por defecto es de solo lectura. | Borrado de la base de datos |
| PD-5 | El texto del incidente es dato, nunca instrucción. Instrucción y contenido viajan separados y el contenido no puede ampliar permisos. | Borrado de la base de datos |
| PD-6 | El estado de un incidente se responde contra el sistema de registro y se entrega con su versión y su marca de tiempo. | Estado desactualizado |
| PD-7 | La caché y el índice de recuperación se invalidan por evento de cambio del incidente, no por vencimiento de un plazo. | Estado desactualizado |
| PD-8 | Sin evidencia recuperada no hay respuesta: el sistema se abstiene y deriva, en lugar de completar con lo que el modelo recuerde. | Respuestas erróneas |
| PD-9 | Las preguntas frecuentes tienen respuesta canónica, generada una vez y reutilizada mientras su evidencia no cambie. Misma pregunta, misma respuesta. | Respuestas distintas |
| PD-10 | "Aprender" es memoria curada de resoluciones aprobadas más un conjunto de evaluación versionado. No hay ajuste de pesos ni memoria de conversación cruda. | El LLM no aprende |
| PD-11 | Cada clase de escalamiento tiene su propia cola y su propia capacidad reservada. Un pico de engineering no puede consumir la capacidad de customer. | Pico de la primera semana |
| PD-12 | Toda dependencia tiene tiempo de espera, reintento acotado con espera creciente y cortacircuito. Un componente lento no se propaga como una caída general. | Pico / no responde |
| PD-13 | Bajo saturación se degrada antes de fallar: respuesta con datos y plantilla, sin modelo. Si tampoco eso, se descarta explícitamente por prioridad. | Pico / no responde |
| PD-14 | Ningún componente del camino crítico de lectura es único. Redundancia N+1 en inferencia y proxies, réplica con relevo automático en base de datos. | Tolerancia a fallos |
| PD-15 | Todo lo que ocurre queda en un registro append-only: consulta, evidencia usada, versión de prompt y modelo, herramienta invocada, aprobación y resultado. | Auditoría de todo lo anterior |

## SPOF y componentes de alto riesgo del harness actual

El enunciado pide identificarlos. El harness actual —API → LLM → MCP base de
datos / MCP Slack— tiene un punto único de falla en **cada** caja del dibujo.

| Componente actual | Por qué es SPOF | Por qué es de alto riesgo | Cómo lo trata el diseño |
| --- | --- | --- | --- |
| API de entrada | Instancia única: si cae, Genius entero deja de responder. | Es también el único punto donde podría autenticarse, y hoy no clasifica ni prioriza nada. | PD-14: réplicas tras balanceador; PD-11: clasificación y prioridad en la entrada |
| LLM local | Un solo servicio de inferencia sobre hardware limitado; si se satura o cae, no hay respuesta. | No determinista e influenciable por el texto que lee; hoy decide por sí mismo qué herramienta ejecutar. | PD-14 (N+1), PD-13 (degradar sin modelo), PD-1 y PD-5 (no decide ni obedece al contenido) |
| MCP Base de Datos | Único proxy hacia el sistema de registro. | **El más peligroso de todos**: expone escritura y borrado con una credencial única, sin clasificación de riesgo ni aprobación. Es por donde se borró la base. | PD-2, PD-3, PD-4: clasificación, aprobación y privilegio mínimo por identidad |
| Base de datos de incidentes | Instancia única: sin ella no hay estado que responder. | Un borrado no tenía reversión definida. | PD-14: réplica con relevo automático y recuperación a punto en el tiempo |
| MCP Slack | Proxy único hacia un servicio externo que puede caer. | Puede exfiltrar detalle de incidentes a un canal equivocado si el modelo elige el destino. | PD-12: cortacircuito y encolado; PD-2: publicar es escritura, con destino validado |
| Índice de recuperación | Si se reconstruye periódicamente, es la fuente del dato viejo. | Responder estado desde aquí es la causa directa de "el incidente cerrado hace horas". | PD-6 y PD-7: el estado no se responde desde el índice; invalidación por evento |

Los tres tipos de escalamiento no son un detalle de dominio: son la razón por la
que hay tres colas. Un *customer escalation* tiene un SLA de un día e impacto
directo en negocio; un *engineering escalation* tiene tres. Cuando la capacidad
de inferencia no alcanza para todos —la primera semana de cada mes— el sistema
tiene que saber cuál sacrificar, y eso se decide antes del pico, en el diseño,
no durante el pico, por orden de llegada.
