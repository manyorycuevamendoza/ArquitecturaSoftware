# Resumen Lab4 — RemoteSchooly
Arquitectura de Software — UTEC — 2026-II

## El problema

RemoteSchooly distribuye educacion semanal a escuelas remotas del Peru con dos restricciones:

1. **Internet intermitente.** Las escuelas tienen conexion limitada que se corta. La clase no puede depender de que haya red en ese momento.
2. **Costo de IA desbordado.** Los docentes piden material a un modelo de lenguaje sin estructura. El gasto no es medible ni comparable.

## Personas

| Persona | Rol | Necesidad principal |
| --- | --- | --- |
| Valeria | Coordinadora de contenidos (Lima) | Publicar versiones curriculares y controlar el presupuesto de IA |
| Rosa | Docente rural | Ensenar con o sin Internet, pedir material con IA |
| Diego | Estudiante | Acceder al curso aunque Internet se caiga |

## Arquitectura elegida

Monolito modular central con tres zonas:

- **Lima:** CMS, publicador, almacenamiento HTTPS, AI Gateway, bases de datos centrales.
- **Internet (intermitente):** unico medio de distribucion, no se reemplaza con SSD ni transporte fisico.
- **Escuela:** Nodo Escolar Local que descarga diferencias, verifica, activa y sirve por WiFi/LAN.

El SSD se descarta porque el enunciado dice Internet *intermitente*, no *sin Internet*. Un SSD resuelve un problema que la escuela no tiene y agrega custodia, viajes y retraso.

## Metodo de analisis: "casos posibles"

Cada punto de decision se resuelve con tres pasos:

1. Declarar las variables observables (A, B, C...).
2. Calcular el producto cartesiano y colapsar las combinaciones imposibles o equivalentes.
3. Asignar una accion a cada caso que queda.

Esto garantiza que no quede ningun caso sin decision y que el numero de casos sea demostrable.

---

## Los 12 puntos de decision (PD)

### PD-1 — Que archivos transferir

Variables: A = archivo en manifiesto local, B = en manifiesto remoto, C = hashes iguales.

| Caso | Accion |
| --- | --- |
| NUEVO (B si, A no) | bajar |
| EDITADO (A y B, hash distinto) | bajar |
| SIN CAMBIO (A y B, hash igual) | no bajar |
| RETIRADO (A si, B no) | borrar de la cache |
| A no y B no | imposible por algebra relacional |

**Clave:** el caso NUEVO no se detecta por hash, se detecta por path. El hash entra en PD-2. El manifiesto es la lista autoritativa: lo que no esta en el de Lima, se borra.

**Bases de datos:**
- Lima: `content_packages` y `package_files`
- Nodo (SQLite): `local_manifest` y `download_plan`

---

### PD-2 — El archivo llego bien

Variables: A = hash del archivo descargado coincide con el del manifiesto, B = firma del manifiesto valida, C = hay version anterior en READY.

| Caso | Accion |
| --- | --- |
| hash OK, firma OK, hay anterior | activar la version nueva |
| hash OK, firma OK, no hay anterior | activar; es la primera carga |
| hash OK, firma invalida, hay anterior | rechazar; conservar la anterior |
| hash OK, firma invalida, sin anterior | rechazar; alertar a Lima |
| hash no OK, firma OK, hay anterior | descartar ese archivo; conservar anterior; reintentar el bloque |
| hash no OK, firma OK, sin anterior | rechazar; alertar a Lima |

**Clave:** la diferencia de hash tiene significados opuestos segun el momento. Antes de bajar = hay contenido nuevo (buena noticia). Despues de bajar = se corrompio (mala noticia).

---

### PD-3 — Este evento ya lo procese (idempotencia)

Variables: A = el event_id ya esta en la base de Lima, B = el payload es identico.

**Clave:** `event_id = school_id + seq + hash(contenido)`. Se fija al *crear* el evento, no al enviar. Mismo event_id en dos envios = segundo se ignora. Un evento recibido dos veces no genera dos registros.

---

### PD-4 — La escuela salto varias versiones

**Decision de diseno:** el manifiesto es de **estado completo**, no delta encadenado.

El manifiesto de la semana 12 dice "esto es todo lo que la escuela debe tener hoy", no "esto cambio respecto de la semana 11". Con eso, saltar versiones no es un caso especial: es el mismo algoritmo de PD-1.

**Medicion:** escuela en semana 9 con semanas 10, 11 y 12 pendientes:
- Delta encadenado: 369 MB, 49 min
- Estado completo: 185 MB, 25 min (50% menos)

Diego no pierde el material de las semanas sin senal: sigue vigente en el manifiesto.

---

### PD-5 — Se corta la luz durante la activacion

**Activar no es copiar archivos, es mover un puntero.**

```
/cache/s11/   <- version anterior, intacta
/cache/s12/   <- version nueva descargada y verificada
/cache/ACTIVE --> s11    activar = apuntar a s12 (rename POSIX)
```

Orden obligatorio:
1. descargar en directorio propio de la version
2. verificar hash y firma de todo lo esencial
3. mover el puntero
4. recien entonces borrar la version anterior

La cuarta fila imposible del cruce (puntero movido antes de verificar) prueba que el orden es correcto: si ocurre, es un defecto grave.

---

### PD-6 — El reloj del nodo esta desincronizado

Un reloj desviado no rompe la idempotencia si el event_id se fija al crear el evento. Si lo tomara al enviar, cada reintento generaria un id distinto y el avance de Diego se registraria dos veces.

Se guardan dos tiempos separados:
- `created_at`: puesto por el nodo. Contexto pedagogico.
- `received_at`: puesto por Lima. Orden y auditoria confiables.

---

### PD-7 — Sincronizar ahora o esperar

La prioridad no es aprovechar toda ventana de red, es **no degradar la clase que esta ocurriendo**.

| Caso | Accion |
| --- | --- |
| sin senal | esperar; la clase sigue contra el nodo |
| senal, sin clase, con energia | sincronizar a fondo |
| senal, sin clase, sin energia | no iniciar; ventana desperdiciada |
| senal, hay clase, con energia | sincronizar con limite de ancho de banda |
| senal, hay clase, sin energia | no sincronizar; toda la energia va a servir la LAN |

Si las 500 escuelas sincronizan al mismo horario, el pico derrumba el almacenamiento central. Se mitiga con espera aleatoria por escuela.

---

### PD-8 — El disco del nodo se llena

La activacion atomica necesita **dos versiones en disco a la vez**: la activa y la nueva descargandose. Por eso el minimo no es 4 GB sino 8 GB por nodo.

| Concepto | Espacio |
| --- | ---: |
| Version activa | 3.0 GB |
| Version nueva descargandose | 3.0 GB |
| Cola de eventos e indices | 0.5 GB |
| Sistema y margen | 1.5 GB |
| **Minimo por nodo** | **8.0 GB** |

Jerarquia de borrado (de lo que se puede borrar a lo que no se toca):
1. Multimedia opcional de versiones antiguas
2. Versiones antiguas completas, excepto la activa
3. **Nunca:** version activa, cola de eventos, indice de bloques

La cola tiene prioridad sobre el espacio: primero se envia, nunca se borra sin confirmar.

---

### PD-9 — Se puede construir el prompt o hay que preguntar

El Clarification Gate **no invoca al modelo**. Las preguntas salen de los campos obligatorios de la plantilla. Costo: 0 tokens externos.

Orden de evaluacion (el orden importa):
1. Revisar que existe plantilla vigente para ese tipo de recurso y ano.
2. Revisar la cuota **antes** de pedir aclaraciones.
3. Verificar que esten los campos obligatorios.

Si se avisa de la cuota al final, Rosa completa todo y choca con un muro que existia desde el inicio.

---

### PD-10 — Reutilizar de cache o invocar al modelo

Huella: `hash(prompt_id + version + campos + IDs_fragmentos + modelo + curriculum_version)`

La version curricular es parte de la huella: un pedido identico hecho en 2027 no encuentra la huella de 2026, encuentra una huella vieja y la descarta. Se regenera una vez y se vuelve a cachear.

El acierto de cache **funciona sin red**. Es la unica forma de producir material con IA durante un corte, y sale gratis.

---

### PD-11 — Este dato entra al prompt o se queda fuera

El archivo intermedio es la frontera de costo. Cuatro clases de datos:

| Clase | Que es | Tokens libres | Tokens gateway |
| --- | --- | ---: | ---: |
| RUIDO | saludos, cortesias | 80 | 0 |
| REDUNDANTE | repite grado/curso ya puestos en el formulario | 120 | 0 |
| ACOTABLE | pega el temario completo cuando solo hacen falta 2 fragmentos | 1,100 | 352 |
| IMPRESCINDIBLE | objetivo pedagogico y restricciones | 700 | 490 |
| **Total** | | **2,000** | **842** |

Reduccion del 58%. El 55% del ahorro sale de un solo caso: ACOTABLE. Si el diseno solo limpiara saludos, nunca llegaria al 40%.

---

### PD-12 — Que se hace si no cabe en el presupuesto

El Budget Guard controla **entrada y salida**. Controlar solo la entrada es el error mas comun: la respuesta se desborda y el costo real duplica lo estimado.

Cuando se bloquea, se le explica a Rosa que recortar. El sistema no reintenta solo. Bloquear cuesta cero; enviar y recibir un cobro no.

---

## Los 34 peores casos (catalogo)

| # | Peor caso | Consecuencia | Mitigacion |
| --- | --- | --- | --- |
| P1 | ventana de conexion no alcanza | la escuela nunca actualiza | solo viajan diferencias; esencial tiene prioridad |
| P2 | se pierde el indice de bloques | la descarga reinicia desde cero cada corte | indice persistente, no en memoria |
| P3 | activacion parcial | guia nueva con ficha vieja | activacion atomica por puntero |
| P4 | firma/hash invalido sin version anterior | la escuela queda sin material | estado explicito y alerta en panel de Valeria |
| P5 | RETIRADO olvidado | temas viejos visibles para siempre; disco lleno | manifiesto es lista autoritativa completa |
| P6 | timestamp tomado al enviar | avances duplicados en cada reintento | timestamp congelado al crear el evento |
| P7 | Lima aplica el evento pero no guarda el event_id | duplicado en el reintento | aplicar y registrar en la misma transaccion |
| P8 | la cola crece sin limite | disco lleno; se pierden eventos nuevos | tope de cola, prioridad y alerta |
| P9 | colision de hash | contenido falso aceptado como valido | SHA-256 + firma del manifiesto + id compuesto |
| P10 | se asume que habra conexion durante la clase | el sistema no sirve para el caso real | offline-first: el nodo responde siempre |
| P11 | manifiesto como delta encadenado | escuela atrasada no puede recuperarse | manifiesto de estado completo |
| P12 | manifiesto describe solo su semana | Diego no ve el material de semanas sin senal | el manifiesto lista todo lo vigente |
| P13 | descargar versiones en orden s10, s11, s12 | 184 MB desperdiciados en versiones ya reemplazadas | comparar contra el manifiesto mas nuevo |
| P14 | atraso permanente invisible | escuela congelada y nadie se entera | indicador de semanas de atraso en panel de Valeria |
| P15 | activar copiando archivos encima | corte deja guia nueva con ficha vieja | cada version en su directorio; se mueve un puntero |
| P16 | mover el puntero antes de verificar | la escuela sirve material corrupto | verificar siempre antes de activar |
| P17 | borrar la version anterior antes de activar | si la activacion falla, no hay a que volver | se borra despues, solo si la nueva quedo activa |
| P18 | salto de reloj por NTP entre crear y reenviar | el id cambia y el duplicado se cuela | contador local monotono ademas del timestamp |
| P19 | ordenar auditoria por hora del nodo | avances desordenados o en el futuro | ordenar por received_at de Lima |
| P20 | sincronizar sin limite durante la clase | Rosa no puede abrir material que ya esta en el nodo | tope de ancho de banda en horario de clase |
| P21 | todas las escuelas sincronizan a la misma hora | pico de carga sobre almacenamiento central | espera aleatoria por escuela |
| P22 | borrar la cola para liberar espacio | se pierden avances que no existen en otro lado | la cola se envia, nunca se borra sin confirmacion |
| P23 | nodo dimensionado a 4 GB | la activacion atomica nunca puede ejecutarse | minimo de 8 GB por nodo |
| P24 | disco al 100% | no se puede registrar ni el fallo | alerta al 85% y freno de descarga opcional |
| P25 | el Clarification Gate invoca al modelo para preguntar | se gastan tokens en el paso que existe para no gastarlos | las preguntas salen de la plantilla, no del modelo |
| P26 | entregar resultado de 2026 porque no hay red | Rosa ensena con contenido obsoleto; error silencioso | la huella vieja se encola, nunca se entrega |
| P27 | huella de cache sin version curricular | todo pedido repetido devuelve contenido viejo para siempre | curriculum_version es parte de la huella |
| P28 | adjuntar el temario completo "por si acaso" | se pierde el 55% del ahorro; meta del 40% fuera de alcance | solo entran fragmentos etiquetados |
| P29 | arrastrar toda la conversacion anterior | el costo crece en cada pedido aunque el pedido sea simple | el archivo intermedio guarda intencion y referencias, no historial |
| P30 | avisar de la cuota agotada al final | Rosa completa todo y choca con un muro que existia desde el inicio | la cuota se evalua antes de la primera pregunta |
| P31 | controlar solo los tokens de entrada | la respuesta se desborda y el costo real duplica lo estimado | presupuesto de entrada y de salida |
| P32 | no registrar las llamadas fallidas | el gasto real supera al reportado y la meta del 40% miente | el ledger registra toda invocacion, exitosa o no |
| P33 | medir contra una linea base no comparable | el 40% es un numero inventado | la linea base fija tarea, modelo y version curricular |
| P34 | el prompt vive en el chat del docente | no se puede reutilizar, versionar ni auditar el gasto de 2026 | biblioteca de prompts con plantillas versionadas |

---

## Guion del recorrido — PD-1 (para explicar al profesor)

Este guion es la base del diagrama de arquitectura de PD-1. Cada escena es un grupo de cajas.

**Personajes:** Valeria (Lima), el Nodo Local (escuela), Rosa (docente)

**Escena 1 — Valeria publica**
Valeria termina de cargar el material de la semana 3. El CMS genera un manifiesto: una lista con cada archivo, su hash SHA-256 y su tamano. Firma el manifiesto y lo sube al servidor HTTPS junto con los archivos.

**Escena 2 — El nodo despierta**
El Sync Agent del nodo escolar se activa (por horario o porque recupero Internet). No sabe que cambio. Lo primero que hace es pedir el manifiesto remoto por HTTPS.

**Escena 3 — El cruce**
El agente pone lado a lado el manifiesto remoto y el manifiesto local. De ese cruce salen exactamente 4 casos: NUEVO, EDITADO, SIN CAMBIO, RETIRADO.

**Escena 4 — El plan**
El agente escribe un plan de descarga en la base de datos local: una fila por archivo con accion y estado. Guia y actividad van primero; video va al final.

**Escena 5 — La descarga**
El agente descarga en bloques reanudables. Si se cae la red, guarda hasta donde llego. Cuando vuelve la red, pide solo los rangos que faltan.

**Escena 6 — La verificacion**
Al completar cada archivo, calcula el hash y lo compara con el del manifiesto. Si coincide, marca LISTO. Si no coincide, descarta el archivo y deja la version anterior intacta.

**Escena 7 — La activacion**
Cuando todos los archivos NUEVO y EDITADO estan en LISTO, el agente mueve el puntero de version activa. Es una operacion atomica: Rosa nunca ve una mezcla de la version vieja y la nueva.

**Escena 8 — Rosa ensena**
Rosa abre la app. El nodo le sirve el material desde la cache local por WiFi. No necesita Internet en ese momento.

---

## Archivos creados y modificados

| Archivo | Que es |
| --- | --- |
| `Lab4/Architecture.md` | Diseno REDALE completo con flujos, modelo de datos y componentes |
| `Lab4/README.md` | Indice de entregables y orden de lectura |
| `Lab4/Diagrams/00-contexto-diagrama.md` | Documento vivo con los 12 PD resueltos, 34 peores casos y frases para el diagrama (959 lineas) |
| `Lab4/Diagrams/01-topdown-remoteschooly.excalidraw` | Top Down Design original (resumen) |
| `Lab4/Diagrams/02-topdown-remoteschooly-v2.excalidraw` | Top Down Design por iteraciones con frases numeradas |
| `Lab4/Diagrams/03-arquitectura-remoteschooly.excalidraw` | Arquitectura por zonas con P-codes y narrativa en 10 escenas |
| `Prompts/casos-posibles.md` | Metodo reutilizable de enumeracion exhaustiva de casos |
| `.gitignore` | Lab2/POC excluido del repositorio |

---

## Conceptos tecnicos clave

### Hash SHA-256: tres usos distintos

| Uso | Pregunta que responde | Momento |
| --- | --- | --- |
| Integridad | llego igual a como salio? | despues de descargar |
| Comparacion | esto es lo mismo que ya tengo? | antes de descargar (manifiesto) |
| Identidad | ya vi esto antes? | event_id de la cola, huella de cache |

La misma diferencia de hash significa cosas opuestas segun contra que se compare:
- Mi version vieja vs la nueva de Lima: hay contenido nuevo, hay que bajar (buena noticia).
- Lo que baje vs el manifiesto de esa misma version: se corrompio, hay que rechazar (mala noticia).

### Clave idempotente

```
event_id = school_id + seq + hash(contenido)
```

Se fija al *crear* el evento, nunca al enviar. El mismo event_id enviado dos veces produce un solo registro. El seq es un contador local monotono que no depende del reloj.

### Activacion atomica

```
POSIX rename("/cache/s12/", "/cache/ACTIVE")
```

Una sola operacion del sistema de archivos. No existe un instante en que apunte a media version. Si se corta la luz, el puntero esta en s11 o en s12, nunca en el medio.

### Reduccion de tokens

Linea base: 2,000 tokens por solicitud.
Con Gateway: 842 tokens (58% de reduccion, meta era 40%).
El 55% del ahorro sale del caso ACOTABLE: enviar fragmentos etiquetados en lugar del temario completo.

---

## Pendientes identificados

### Cambios por aplicar a otros documentos

| Documento | Que falta | Origen |
| --- | --- | --- |
| `Architecture.md` | declarar el manifiesto como estado completo | PD-4 |
| `Architecture.md` | fijar orden: descargar, verificar, activar, borrar; y activacion por puntero | PD-5 |
| `Architecture.md` entidades | `outbox_events` necesita `seq`, `created_at` y `received_at` | PD-6 |
| `Architecture.md` estimaciones | minimo de 8 GB por nodo escolar | PD-8 |
| `Architecture.md` entidades | `ai_generations` necesita `curriculum_version` dentro de `request_hash` | PD-10 |
| `Requirements/NonFunctional.md` | tope de ancho de banda en horario de clase; umbral de disco al 85% | PD-7, PD-8 |
| `Requirements/Functional.md` | evaluar la cuota antes de pedir aclaraciones | PD-9 |

### PDs candidatos para una siguiente pasada

- **PD-13** Rotacion de llaves de firma: que pasa cuando Lima rota la llave y la escuela estuvo meses sin red.
- **PD-14** Escuela dividida o fusionada: cambia el school_id y con el la identidad de los eventos en cola.
- **PD-15** Solicitud de IA encolada que caduca: un PENDING_NETWORK creado con curriculum 2026.2 que sale cuando ya rige la 2027.1.

---

## Diagrama ASCII del flujo PD-1 (boceto del usuario)

```
LIMA / NUBE
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Valeria                                                    │
│      │                                                      │
│      ▼                                                      │
│ ┌─────────────┐       genera       ┌────────────────────┐   │
│ │     CMS     │ ─────────────────► │ Manifest + SHA-256 │   │
│ └──────┬──────┘                    └─────────┬──────────┘   │
│        │ archivos                            │              │
│        └──────────────────┬──────────────────┘              │
│                           ▼                                 │
│                 ┌──────────────────────┐                    │
│                 │ Servidor HTTPS       │                    │
│                 │ Archivos + Manifest  │                    │
│                 └──────────┬───────────┘                    │
└────────────────────────────┼────────────────────────────────┘
                             │
                   HTTPS / Internet intermitente
                             │
                             ▼
ESCUELA / NODO LOCAL
┌─────────────────────────────────────────────────────────────┐
│                  ┌─────────────────────┐                    │
│                  │     Sync Agent      │                    │
│                  └──────────┬──────────┘                    │
│                             │                               │
│               descarga manifest remoto                      │
│                             ▼                               │
│                ┌────────────────────────┐                   │
│                │ Comparador de Manifest │                   │
│                └────────────┬───────────┘                   │
│                             │                               │
│          ┌──────────────────┼───────────────────┐           │
│          │                  │                   │           │
│          ▼                  ▼                   ▼           │
│       NUEVO              EDITADO           SIN CAMBIO       │
│       BAJAR               BAJAR              OMITIR         │
│                                                             │
│                     RETIRADO → BORRAR                       │
│                             │                               │
│                             ▼                               │
│                ┌─────────────────────────┐                  │
│                │ Plan de sincronizacion  │                  │
│                │ DB Local                │                  │
│                │ PENDIENTE / LISTO       │                  │
│                └────────────┬────────────┘                  │
│                             ▼                               │
│                ┌─────────────────────────┐                  │
│                │ Gestor de Descargas     │                  │
│                │ bloques reanudables     │                  │
│                └────────────┬────────────┘                  │
│                             ▼                               │
│                ┌─────────────────────────┐                  │
│                │ Verificador SHA-256     │                  │
│                └────────────┬────────────┘                  │
│                   hash coincide?                            │
│                      /             \                        │
│                    Si               No                      │
│                    │                │                       │
│                    ▼                ▼                       │
│                 LISTO          DESCARTAR                    │
│                    │       (mantener version anterior)      │
│                    ▼                                        │
│            ┌─────────────────────┐                          │
│            │ Activador de version│                          │
│            │ cambio atomico      │                          │
│            └──────────┬──────────┘                          │
│                       ▼                                     │
│               ┌───────────────┐                             │
│               │ Cache Local   │                             │
│               │ version activa│                             │
│               └───────┬───────┘                             │
└───────────────────────┼─────────────────────────────────────┘
                        │ WiFi local
                        ▼
                     Rosa (docente)
```
