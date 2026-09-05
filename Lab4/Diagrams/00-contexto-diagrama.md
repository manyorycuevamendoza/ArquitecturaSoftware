# Contexto del diagrama de arquitectura — RemoteSchooly

Documento vivo. Cada vez que se resuelve un punto de decisión con el método de
casos posibles ([../../Prompts/casos-posibles.md](../../Prompts/casos-posibles.md)),
se agrega aquí. El lienzo
[02-topdown-remoteschooly-v2.excalidraw](02-topdown-remoteschooly-v2.excalidraw)
se dibuja **desde** este archivo, no al revés.

El diagrama se cuenta como una historia y nombra los peores casos. Un diagrama
que solo muestra el camino feliz no es una arquitectura: es un folleto.

## Estado de los puntos de decisión

| # | Punto de decisión | Estado |
| --- | --- | --- |
| PD-1 | ¿Qué archivos transferir? (comparación de manifiestos) | resuelto |
| PD-2 | ¿El archivo llegó bien? (verificación de integridad) | resuelto |
| PD-3 | ¿Este evento ya lo procesé? (idempotencia del retorno) | resuelto |
| PD-4 | ¿Qué pasa si la escuela saltó varias versiones? | resuelto |
| PD-5 | ¿Qué pasa si se corta la luz durante la activación? | resuelto |
| PD-6 | ¿Qué pasa si el reloj del nodo está desincronizado? | resuelto |
| PD-7 | ¿Sincronizar ahora o esperar? (red, horario, energía) | resuelto |
| PD-8 | ¿Qué hacer cuando el disco del nodo se llena? | resuelto |
| PD-9 | ¿Se puede construir el prompt o hay que preguntar? (Clarification Gate) | resuelto |
| PD-10 | ¿Reutilizar de caché o invocar al modelo? | resuelto |
| PD-11 | ¿Este dato entra al prompt o se queda fuera? (archivo intermedio) | resuelto |
| PD-12 | ¿Qué se hace si no cabe en el presupuesto? | resuelto |

---

## El hilo de la historia

Seis escenas. Cada una tiene su camino feliz y su peor caso. El diagrama se
recorre en este orden.

| # | Escena | Camino feliz | Peor caso |
| --- | --- | --- | --- |
| 1 | Lima publica la semana | manifiesto firmado, hash por archivo | el manifiesto se publica sin firma o con un hash mal calculado: nadie puede confiar en el paquete |
| 2 | El nodo decide qué bajar | compara listas, baja solo lo que cambió | detecta mal el cambio y baja 3 GB en un enlace de 1 Mbps: la ventana no alcanza y no baja nada |
| 3 | La transferencia se corta | reanuda desde el último bloque validado | pierde el índice de bloques y reinicia desde cero cada vez: nunca termina |
| 4 | El nodo verifica y activa | hash y firma correctos, activación atómica | activa una versión a medias: Rosa enseña con la guía nueva y la ficha vieja |
| 5 | La clase ocurre sin red | el nodo sirve la última versión READY por LAN | la escuela se queda sin material porque el diseño asumió que habría conexión |
| 6 | Lo hecho sin red vuelve a Lima | cola idempotente, se envía una sola vez | el avance de Diego se registra dos veces, o se pierde para siempre |
| 7 | Rosa entra y pide material con IA | el login le da identidad, escuela y cuota | un pedido anónimo: no se puede presupuestar ni auditar |
| 8 | Se arma el archivo intermedio | entra lo necesario, se descarta el resto | se copia el temario completo "por si acaso" y el ahorro desaparece |
| 9 | El Gateway decide si invocar | aclara, reutiliza o bloquea antes de gastar | se llama al modelo para preguntar: se gastan tokens en no gastar tokens |
| 10 | Valeria mide la reducción | contra una línea base comparable | se mide contra una base distinta y el 40% es un número inventado |

---

## PD-1 — ¿Qué archivos transferir?

**Quién decide:** el Sync Agent del Nodo Escolar Local.
**Cuándo:** apenas hay señal, después de descargar el manifiesto (unos KB).
**Con qué información:** su manifiesto local y el manifiesto que publicó Lima.

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿el archivo está en mi manifiesto local? | sí / no |
| B | ¿el archivo está en el manifiesto de Lima? | sí / no |
| C | si está en ambos, ¿el hash coincide? | igual / distinto |

### Cruce exhaustivo (2 x 2 = 4 celdas, la celda "en ambos" se parte en 2)

| A | B | C | Caso | Acción |
| --- | --- | --- | --- | --- |
| no | sí | no aplica | **NUEVO** | bajar |
| sí | sí | distinto | **EDITADO** | bajar |
| sí | sí | igual | **SIN CAMBIO** | no bajar |
| sí | no | no aplica | **RETIRADO** | quitar de la caché |
| no | no | no aplica | *imposible: el archivo no existe* | descartado |

### Hallazgo de diseño

El caso NUEVO **no se detecta por hash**: no hay hash previo con qué comparar.
Se detecta por el identificador del archivo. El hash de un archivo nuevo se usa
después, en PD-2, para verificar la descarga. Confundir esto lleva a diseñar un
Sync Agent que no puede descubrir contenido nuevo.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **RETIRADO olvidado** | la escuela sigue mostrando temas de semanas viejas para siempre; la caché crece sin límite hasta llenar el disco | el manifiesto es la lista completa y autoritativa: lo que no está en él se elimina |
| Falso "SIN CAMBIO" | Valeria corrige un error en la guía, el hash no se recalcula y la corrección nunca llega | el hash se calcula en la publicación, siempre, sobre el contenido real |
| Falso "EDITADO" masivo | un cambio de formato recalcula todos los hashes y se intentan bajar 3 GB en 1 Mbps: la ventana no alcanza | prioridad por recurso: lo esencial baja primero y queda READY antes que lo opcional |

### Frases para el diagrama

- "Compara dos listas, no dos archivos: por eso viajan 300 MB y no 3 GB."
- "Lo que no está en el manifiesto de Lima, se borra de la escuela."
- "Un tema nuevo se descubre por su nombre; un tema editado, por su hash."

---

## PD-2 — ¿El archivo llegó bien?

**Quién decide:** el nodo, antes de publicar nada en la LAN.
**Cuándo:** al terminar de descargar cada archivo, y también bloque por bloque.

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿el hash del archivo descargado coincide con el del manifiesto? | sí / no |
| B | ¿la firma del manifiesto es válida? | sí / no |
| C | ¿existe una versión anterior en estado READY? | sí / no |

### Cruce exhaustivo (2 x 2 x 2 = 8 filas)

| A hash | B firma | C hay anterior | Caso | Acción |
| --- | --- | --- | --- | --- |
| sí | sí | sí | **OK con respaldo** | activar la versión nueva |
| sí | sí | no | **OK primera carga** | activar; es la primera versión de la escuela |
| sí | no | sí | **firma inválida** | rechazar; conservar la anterior |
| sí | no | no | **firma inválida sin respaldo** | rechazar; la escuela queda sin material y se alerta a Lima |
| no | sí | sí | **archivo corrupto** | rechazar ese archivo; conservar la anterior; reintentar el bloque |
| no | sí | no | **corrupto sin respaldo** | rechazar; la escuela queda sin material y se alerta a Lima |
| no | no | sí | **paquete no confiable** | rechazar todo; conservar la anterior |
| no | no | no | **paquete no confiable sin respaldo** | rechazar; escalar a soporte regional |

### Hallazgo de diseño

Hash y firma responden preguntas distintas y las dos hacen falta:

- el **hash** prueba *integridad*: "esto no se rompió en el camino"
- la **firma** prueba *procedencia*: "esto lo publicó Lima, no un impostor"

Un archivo puede tener hash correcto y firma inválida: significa que alguien
armó un paquete coherente pero no es Lima.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **Activación parcial** | Rosa enseña con la guía de la semana 12 y la ficha de la semana 11: los ejercicios no corresponden a la lectura | la activación es atómica: se mueve un puntero de versión al final, no se copian archivos encima |
| **Sin versión anterior** (primera carga fallida) | escuela nueva que nunca llega a tener material y no hay a qué volver | estado explícito de escuela sin versión válida, visible en el panel de Valeria |
| **Colisión de hash** | contenido distinto se acepta como válido | ver la sección de colisiones más abajo |

### Frases para el diagrama

- "Verifica antes de publicar: Rosa nunca ve un archivo sin verificar."
- "El hash dice que llegó completo; la firma dice que salió de Lima."
- "O entra la versión completa, o no entra ninguna."
- "Si algo falla, la escuela sigue con la última versión READY: nadie se queda sin clase."

---

## PD-3 — ¿Este evento ya lo procesé?

**Quién decide:** la API de sincronización en Lima, al recibir la cola del nodo.
**Cuándo:** cada vez que llega un evento de retorno (avance, incidencia, solicitud).

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿ya tengo un evento con este `event_id`? | sí / no |
| B | ¿el nodo recibió mi confirmación anterior? | sí / no / no se sabe |

La variable B casi siempre vale "no se sabe": ese es exactamente el problema
que resuelve la idempotencia.

### Cruce exhaustivo

| A ya lo tengo | B confirmó | Caso | Acción |
| --- | --- | --- | --- |
| no | no aplica | **evento nuevo** | procesar y guardar el `event_id` |
| sí | no | **reintento** | no reprocesar; responder OK otra vez |
| sí | sí | **duplicado real** | no reprocesar; registrar como anomalía |

### Cómo se construye el identificador

```
event_id = school_id + timestamp + hash(contenido)

PE-AYA-041 - 2026-09-11T10:15:33Z - 1f045c4e79d4
   escuela        segundo exacto        hash
```

El hash es solo un tercio del identificador. Para que dos eventos distintos
choquen tendrían que coincidir la misma escuela, el mismo segundo y un hash
colisionado.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **El timestamp se calcula al enviar, no al crear** | el reintento genera un `event_id` distinto y el duplicado se cuela: Diego aparece con la actividad hecha dos veces | el timestamp se congela al crear el evento en la cola local, nunca al transmitirlo |
| **Reloj del nodo desincronizado** | dos eventos distintos de la misma escuela caen en el mismo segundo y pueden confundirse | el `event_id` incluye el hash del contenido, que los separa aunque el reloj falle |
| **Lima procesa y muere antes de guardar el `event_id`** | al reintentar, lo procesa otra vez: duplicado | guardar el `event_id` y aplicar el evento en la misma transacción |
| **Corte muy largo** | la cola crece hasta llenar el disco del nodo y se empiezan a perder eventos nuevos | límite de tamaño de la cola, prioridad por tipo de evento y alerta al administrador regional |
| **El nodo se reinstala con la cola sin enviar** | se pierden semanas de avances de los estudiantes | la cola vive en almacenamiento persistente, fuera del ciclo de vida de la aplicación |

### Frases para el diagrama

- "Lo hecho sin red no se pierde: espera en la cola local."
- "Cuando vuelve la red, la cola se envía una sola vez."
- "El reintento es seguro: mismo identificador, un solo registro."

---

## PD-4 — ¿Qué pasa si la escuela saltó varias versiones?

**Quién decide:** el Sync Agent del nodo.
**Cuándo:** al recuperar señal después de un corte largo.
**Situación:** la escuela quedó en la semana 9. Lima ya publicó s10, s11 y s12.

### La decisión de diseño que había que declarar

El diseño no decía si un manifiesto describe **solo su semana** o **el estado
completo del curso a esa fecha**. De eso depende todo lo demás.

| Opción | Qué dice el manifiesto de s12 | Consecuencia |
| --- | --- | --- |
| Delta encadenado | "respecto de s11 cambió esto" | para llegar a s12 hay que aplicar s10 y s11 antes, en orden |
| **Estado completo** | "esto es todo lo que la escuela debe tener al llegar s12" | se puede saltar directo a s12 desde cualquier versión previa |

**Se elige estado completo.** Con conectividad intermitente, saltarse versiones
no es la excepción: es el caso normal. Un diseño encadenado convierte cada
semana perdida en un eslabón obligatorio.

**Restricción que impone:** los archivos deben viajar completos, no como parches
binarios contra la versión anterior. Un parche reintroduce el encadenamiento por
la puerta de atrás.

**Costo aceptado:** el manifiesto lista todos los archivos vigentes, no solo los
que cambiaron. Son kilobytes; el ahorro está en los megabytes que no se
transfieren.

### Medición sobre el caso concreto

Escuela en s9, con s10, s11 y s12 pendientes:

| Estrategia | Qué descarga | Volumen | Tiempo a 1 Mbps |
| --- | --- | ---: | ---: |
| Delta encadenado | guía v2, v3 y v4; video v1 y v2; fichas A, B y C | 369 MB | 49 min |
| **Estado completo** | guía **v4**; video **v2**; fichas A, B y C | **185 MB** | **25 min** |

**50% menos.** La guía se descarga una sola vez en su versión final: nunca
viajan las versiones v2 y v3, que s12 ya reemplazó. Y el video tampoco viaja dos
veces.

Obsérvese que `ficha-A.pdf`, publicada en s10, **sí se descarga**: sigue vigente
en el manifiesto de s12. Diego no pierde el material de las semanas que la
escuela estuvo sin señal.

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿Lima publicó versiones nuevas desde mi última sincronización? | sí / no |
| B | ¿el atraso es de una versión o de varias? | una / varias |
| C | ¿la ventana de conexión alcanza para todo lo esencial? | sí / no |

### Cruce exhaustivo

Nominalmente 2 x 2 x 2 = 8 filas. Cuando A = no, las variables B y C no aplican
y sus cuatro combinaciones colapsan en un solo caso. Quedan 1 + 4 = **5 casos**.

| A | B | C | Caso | Acción |
| --- | --- | --- | --- | --- |
| no | no aplica | no aplica | **AL DÍA** | no se transfiere nada |
| sí | una | sí | **ATRASO NORMAL** | bajar la diferencia, verificar y activar |
| sí | una | no | **VENTANA CORTA** | bajar lo esencial, quedar PAUSED, continuar en la siguiente ventana |
| sí | varias | sí | **SALTO DE VERSIONES** | comparar contra el manifiesto más nuevo, bajar el acumulado, activar directo a la última |
| sí | varias | no | **SALTO CON VENTANA CORTA** | igual, por prioridad; la escuela sigue con su versión anterior hasta completar lo esencial |

### Hallazgo de diseño

**PD-4 se disuelve dentro de PD-1.** Si el manifiesto describe el estado
completo, "saltar versiones" deja de ser un caso especial: es el mismo algoritmo
de comparación de listas. El nodo que está en s9 y el que está en s11 leen el
**mismo** manifiesto de s12 y descargan cosas distintas, sin una sola línea de
lógica adicional.

Las semanas perdidas aparecen simplemente como archivos en el caso **NUEVO** de
PD-1. Eso es lo que hace buena a la decisión: elimina un caso en vez de agregar
código para manejarlo.

En ninguno de los cinco casos se activa una versión intermedia. Se activa la más
nueva, una sola vez, cuando todo lo esencial de su manifiesto está verificado.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **Delta encadenado** | a la escuela con tres semanas de atraso le falta un eslabón y no puede aplicar nada; nunca se recupera | manifiesto de estado completo |
| **El manifiesto describe solo su semana** | Diego nunca ve el material de s10 y s11: hueco pedagógico silencioso, nadie se entera | el manifiesto lista todo lo vigente, no solo lo que cambió |
| **Descargar en orden s10, s11, s12** | se gasta la ventana bajando versiones que s12 ya reemplazó: 184 MB desperdiciados de 369 | se compara contra el manifiesto más nuevo, no contra el siguiente |
| **Atraso permanente invisible** | la escuela nunca junta ventana suficiente, queda congelada y nadie lo detecta | indicador de semanas de atraso por escuela en el panel de Valeria |
| **Activar una versión intermedia** | se publica s10 y al rato s12: dos activaciones, trabajo y ventana desperdiciados | se activa solo la versión más nueva disponible |

### Frases para el diagrama

- "Si la escuela estuvo tres semanas sin señal, no baja tres versiones: baja la diferencia contra la última."
- "El manifiesto no dice qué cambió esta semana; dice qué debe tener la escuela hoy."
- "Nadie pierde el material de las semanas sin señal: sigue vigente en el manifiesto."
- "Saltar versiones no es un caso especial; es el mismo algoritmo de comparar dos listas."

---

## PD-5 — ¿Qué pasa si se corta la luz durante la activación?

**Quién decide:** el nodo, al cambiar de versión activa.
**Cuándo:** cuando todo lo esencial del manifiesto nuevo está verificado.

### Qué significa "atómico" en la práctica

El diseño afirmaba que la activación es atómica, pero no explicaba cómo. Aquí
está: **activar no es copiar archivos, es mover un puntero.**

```
/cache/s11/          <- version anterior, intacta
/cache/s12/          <- version nueva, ya descargada y verificada
/cache/ACTIVE  --->  s11        activar = que apunte a s12
```

Cambiar el puntero es una sola operación del sistema de archivos (`rename`, que
es atómica en POSIX). No existe un instante en que apunte a media versión.

Si en algún momento el diseño copiara los archivos nuevos **encima** de los
viejos, la atomicidad se pierde: un corte a la mitad deja la guía de s12 junto a
la ficha de s11.

### Variables observables al reiniciar tras el corte

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿los archivos esenciales de la versión nueva están completos y verificados en su directorio? | sí / no |
| B | ¿el puntero ya apunta a la versión nueva? | sí / no |

### Cruce exhaustivo (2 x 2 = 4 filas)

| A archivos | B puntero | Caso | Qué ve la escuela | Acción al reiniciar |
| --- | --- | --- | --- | --- |
| no | no | **corte durante la descarga** | versión anterior | reanudar desde el último bloque validado |
| sí | no | **corte entre verificar y activar** | versión anterior | mover el puntero; la operación es idempotente |
| sí | sí | **corte después de activar** | versión nueva | nada, ya está |
| no | sí | ***imposible si el orden es correcto*** | versión nueva sin verificar | si ocurre, es un defecto grave: se movió el puntero antes de verificar |

### Hallazgo de diseño

La cuarta fila es la que **demuestra** que el diseño es correcto. Solo puede
ocurrir si el orden de operaciones está mal. El orden obligatorio es:

```
1. descargar a un directorio propio de la versión
2. verificar hash y firma de todo lo esencial
3. mover el puntero
4. recién entonces, considerar borrar la versión anterior
```

Invertir los pasos 2 y 3 produce esa fila imposible. Adelantar el paso 4 deja a
la escuela sin nada a qué volver.

En los tres casos posibles la escuela **siempre está sirviendo una versión
completa y verificada**. No existe un estado observable a medias.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **Activar copiando encima** | un corte deja guía de s12 con ficha de s11: los ejercicios no corresponden a la lectura | cada versión vive en su directorio; se mueve un puntero |
| **Mover el puntero antes de verificar** | la escuela sirve material corrupto o no firmado | el puntero se mueve al final, nunca antes |
| **Borrar la versión anterior antes de activar** | si la activación falla, no hay a qué volver | se borra después, y solo si la nueva quedó activa |
| **Guardar el puntero con una escritura no atómica** | el archivo de puntero queda truncado y el nodo no sabe qué versión servir | se escribe en un temporal y se hace `rename` |

### Frases para el diagrama

- "Activar no es copiar archivos: es mover un puntero."
- "El corte solo puede encontrarte antes o después del cambio, nunca en medio."
- "Primero verificar, después activar, y solo al final borrar lo viejo."

---

## PD-6 — ¿Qué pasa si el reloj del nodo está desincronizado?

**Quién decide:** el nodo, al crear un evento en la cola de retorno.
**Por qué importa:** el `timestamp` es parte del `event_id`, y el `event_id` es
lo que sostiene la idempotencia de PD-3.

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿el reloj del nodo coincide con el de Lima? | sí / no |
| B | ¿es el primer envío o un reintento? | primero / reintento |

### Cruce exhaustivo (2 x 2 = 4 filas)

| A reloj | B envío | Caso | Riesgo | Por qué no rompe |
| --- | --- | --- | --- | --- |
| sí | primero | **normal** | ninguno | — |
| sí | reintento | **reintento limpio** | ninguno | mismo `event_id` |
| no | primero | **reloj desviado** | la hora del evento queda mal en la auditoría | Lima guarda además su propia hora de recepción |
| no | reintento | **reloj desviado en reintento** | si el `timestamp` se recalculara al enviar, el `event_id` cambiaría y el duplicado se colaría | el `timestamp` se congela al **crear** el evento, no al transmitirlo |

### Hallazgo de diseño

Un reloj desviado **no rompe la idempotencia**, siempre que el identificador se
fije en el momento de creación. Lo que sí rompe es la **auditoría**: el orden y
la hora de los eventos dejan de ser confiables.

Por eso se guardan **dos tiempos distintos**:

| Campo | Quién lo pone | Para qué sirve |
| --- | --- | --- |
| `created_at` | el nodo | contexto pedagógico: cuándo ocurrió en la escuela |
| `received_at` | Lima | orden y auditoría confiables |

**Mejora que sale de este análisis:** apoyar el identificador en un **contador
local monótono** además del tiempo.

```
event_id = school_id + seq + hash(contenido)
```

El contador nunca retrocede, aunque el reloj salte hacia atrás por una
sincronización NTP. El `timestamp` pasa a ser un dato del evento, no parte de su
identidad. Con esto el identificador deja de depender del reloj por completo.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **El `timestamp` se toma al enviar** | cada reintento genera un `event_id` distinto: el avance de Diego se registra dos y tres veces | se congela al crear el evento |
| **Salto de reloj por sincronización NTP** | dos eventos distintos caen en el mismo segundo | el `event_id` incluye el hash del contenido y el contador local |
| **Nodo sin reloj de respaldo** | tras un corte largo de energía el reloj arranca en una fecha por defecto y toda la semana queda mal fechada | `received_at` de Lima como referencia autoritativa |
| **Confiar en `created_at` para ordenar el reporte** | los avances aparecen desordenados o en el futuro | los reportes ordenan por `received_at` |

### Frases para el diagrama

- "El evento nace con su identificador y ya no lo cambia, aunque se reenvíe."
- "La hora de la escuela cuenta la historia; la hora de Lima ordena la auditoría."

---

## PD-7 — ¿Sincronizar ahora o esperar?

**Quién decide:** el Sync Agent del nodo.
**Cuándo:** de forma continua, cada vez que evalúa si conviene abrir la transferencia.

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿hay señal utilizable? | sí / no |
| B | ¿es horario de clase? | sí / no |
| C | ¿hay energía suficiente para sostener la transferencia? | sí / no |

### Cruce exhaustivo

Nominalmente 2 x 2 x 2 = 8 filas. Cuando A = no no se puede transferir sin
importar B y C, así que esas cuatro combinaciones colapsan en una. Quedan
1 + 4 = **5 casos**.

| A red | B clase | C energía | Caso | Acción |
| --- | --- | --- | --- | --- |
| no | no aplica | no aplica | **SIN SEÑAL** | esperar; la clase sigue corriendo contra el nodo |
| sí | no | sí | **VENTANA IDEAL** | sincronizar a fondo, incluido lo opcional |
| sí | no | no | **SIN ENERGÍA** | no iniciar; el progreso se conserva pero se gasta ventana en vano |
| sí | sí | sí | **HAY CLASE** | sincronizar con ancho de banda limitado: servir la clase tiene prioridad |
| sí | sí | no | **CLASE Y POCA ENERGÍA** | no sincronizar; toda la energía va a servir la LAN |

### Hallazgo de diseño

La prioridad no es "aprovechar toda ventana de red". Es **no degradar la clase
que está ocurriendo**. Una sincronización agresiva a mediodía puede saturar el
enlace y la LAN, y hacer que Rosa no pueda abrir una guía que **ya está en el
nodo**. El sistema se rompería a sí mismo con su propia tarea de fondo.

**Riesgo de escala:** si las 500 escuelas sincronizan al mismo horario nocturno,
el pico cae entero sobre el almacenamiento central. Se distribuye con una espera
aleatoria dentro de la ventana, distinta por escuela.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **Sincronizar sin límite durante la clase** | Rosa no puede abrir material que ya está en el nodo: el sistema se estorba a sí mismo | tope de ancho de banda y de uso de disco en horario de clase |
| **Nunca sincronizar por "siempre hay clase"** | la escuela queda congelada indefinidamente | ventana nocturna garantizada, aunque sea reducida |
| **Todas las escuelas a la misma hora** | pico de carga sobre el almacenamiento central y todas fallan juntas | espera aleatoria por escuela dentro de la ventana |
| **Iniciar sin energía** | corte a mitad; recuperable, pero la ventana se desperdicia | umbral mínimo de energía antes de abrir la transferencia |

### Frases para el diagrama

- "La sincronización cede el paso a la clase: primero enseñar, después actualizar."
- "Cada escuela entra a la ventana en un momento distinto, para no caerle todas juntas a Lima."

---

## PD-8 — ¿Qué hacer cuando el disco del nodo se llena?

**Quién decide:** el nodo, antes de iniciar la descarga de una versión.

### El requisito de capacidad que faltaba

La activación atómica de PD-5 necesita **las dos versiones en disco a la vez**.
Eso impone un mínimo que las estimaciones no declaraban:

| Concepto | Espacio |
| --- | ---: |
| Versión activa | 3.0 GB |
| Versión nueva descargándose | 3.0 GB |
| Cola de eventos e índice de bloques | 0.5 GB |
| Sistema operativo y margen | 1.5 GB |
| **Mínimo por nodo** | **8.0 GB** |

Dimensionar el nodo con 4 GB "porque el paquete pesa 3 GB" hace la activación
atómica imposible: no hay dónde poner la versión nueva.

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿cabe la versión nueva? | sí / no |
| B | ¿hay versiones antiguas que se puedan liberar? | sí / no |
| C | ¿hay eventos sin enviar en la cola? | sí / no |

### Cruce exhaustivo

Nominalmente 2 x 2 x 2 = 8. Cuando A = sí no hay que liberar nada y B y C no
inciden en la decisión: esas cuatro filas colapsan en una. Cuando A = no y
B = sí, basta con liberar y C no incide: dos filas colapsan en una. Quedan
1 + 1 + 2 = **4 casos**.

| A cabe | B antiguas | C cola | Caso | Acción |
| --- | --- | --- | --- | --- |
| sí | no aplica | no aplica | **ESPACIO SUFICIENTE** | descargar normalmente |
| no | sí | no aplica | **LIBERAR Y SEGUIR** | borrar versiones antiguas, nunca la activa, y descargar |
| no | no | no | **DISCO LLENO** | descargar solo lo esencial; alertar al administrador regional |
| no | no | sí | **DISCO LLENO CON COLA PENDIENTE** | la cola tiene prioridad: enviarla antes de liberar; jamás borrarla para hacer espacio |

### Jerarquía de borrado

Qué se sacrifica, en orden. Lo de abajo no se toca nunca.

1. Multimedia opcional de versiones antiguas
2. Versiones antiguas completas, excepto la activa
3. **Nunca:** la versión activa, la cola de eventos sin enviar, el índice de bloques validados

### Hallazgo de diseño

El disco lleno no es un problema de almacenamiento: es un problema de
**prioridades**. La regla que ordena todo es que **los datos que solo existen en
la escuela valen más que los datos que Lima puede volver a enviar**. Una versión
borrada se vuelve a descargar; el avance de Diego, si se borra, no existe en
ningún otro lugar del mundo.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **Borrar la cola para hacer espacio** | se pierden semanas de avances e incidencias de forma irrecuperable | la cola es lo último; primero se envía, nunca se borra sin confirmar |
| **Borrar la versión activa** | la escuela se queda sin clase por liberar espacio | la versión activa está protegida por el puntero |
| **Nodo dimensionado a 4 GB** | la activación atómica nunca puede ejecutarse | mínimo de 8 GB en el requisito de capacidad |
| **Disco al 100%** | no se puede escribir ni el registro del fallo: falla silenciosa | umbral de alerta al 85%, se detiene la descarga opcional |
| **Borrar el índice de bloques** | cada corte reinicia la descarga desde cero | el índice está protegido junto con la cola |

### Frases para el diagrama

- "Se borra el contenido que Lima puede reenviar, nunca lo que solo existe en la escuela."
- "El nodo necesita espacio para dos versiones: esa es la condición de la activación atómica."

---

## PD-9 — ¿Se puede construir el prompt o hay que preguntar?

**Quién decide:** el Clarification Gate, dentro del nodo.
**Cuándo:** al recibir el formulario de Rosa, antes de tocar el modelo.
**Regla que lo gobierna:** este paso no invoca al modelo. Cuesta 0 tokens externos.

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿están completos los campos obligatorios? | sí / no |
| B | ¿existe una plantilla vigente para ese tipo de recurso y año? | sí / no |
| C | ¿Rosa está dentro de su cuota? | sí / no |

### Cruce exhaustivo

Nominalmente 2 x 2 x 2 = 8. Si B = no, no se sabe **cuáles** son los campos
obligatorios (los define la plantilla), así que A no es observable y sus cuatro
combinaciones colapsan en una. Quedan 1 + 4 = **5 casos**.

| B plantilla | A campos | C cuota | Caso | Acción |
| --- | --- | --- | --- | --- |
| no | no observable | no aplica | **SIN PLANTILLA VIGENTE** | no se puede construir el prompt; se avisa a Valeria; 0 tokens |
| sí | no | sí | **FALTAN CAMPOS** | máximo tres preguntas concretas; 0 tokens externos |
| sí | no | no | **FALTAN CAMPOS Y SIN CUOTA** | se avisa de la cuota **antes** de pedirle que complete nada |
| sí | sí | sí | **LISTO PARA GENERAR** | se arma el prompt canónico y pasa al presupuesto |
| sí | sí | no | **CUOTA AGOTADA** | no se invoca; la solicitud queda lista y en espera de cuota |

### Hallazgo de diseño

El orden de evaluación importa más que las reglas. **La cuota se revisa antes de
pedir aclaraciones, no después.** Si Rosa contesta tres preguntas y recién ahí se
entera de que no tiene cuota, el sistema le hizo perder el tiempo por un dato que
conocía desde el primer instante.

Y el caso SIN PLANTILLA VIGENTE demuestra por qué el Gate depende de la
biblioteca de prompts: sin plantilla no sabe qué preguntar. No inventa las
preguntas, las lee.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **El Gate invoca al modelo para formular las preguntas** | se gastan tokens en el paso cuyo propósito es no gastarlos: el ahorro se autodestruye | las preguntas salen de los campos obligatorios de la plantilla, no del modelo |
| **Avisar de la cuota al final** | Rosa completa todo y choca contra un muro que existía desde el principio | la cuota se evalúa antes de la primera pregunta |
| **Preguntar sin límite** | el docente abandona y vuelve al pedido libre, que es lo caro | tope de tres preguntas; si con eso no alcanza, se genera con lo que hay y se marca |
| **Plantilla vencida sin reemplazo** | nadie puede generar ese tipo de recurso y no hay señal de por qué | alerta a Valeria; una plantilla vencida siempre tiene sucesora o se mantiene vigente |

### Frases para el diagrama

- "El Gate no inventa las preguntas: lee de la plantilla qué campos exige."
- "Preguntar cuesta cero; adivinar cuesta una llamada al modelo."
- "La cuota se avisa antes de escribir, no después."

---

## PD-10 — ¿Reutilizar de caché o invocar al modelo?

**Quién decide:** el AI Gateway.
**Cuándo:** con el prompt canónico ya armado, justo antes de salir a Internet.

**La huella:**

```
huella = hash(prompt_id + version + valores de campos + IDs de fragmentos
              + modelo + curriculum_version)
```

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿existe esta huella en la caché? | sí / no |
| B | ¿la versión curricular de la huella es la vigente? | sí / no |
| C | ¿hay red para llegar al proveedor? | sí / no |

### Cruce exhaustivo

Nominalmente 2 x 2 x 2 = 8. Si A = no no hay huella cuya versión comparar y B no
aplica (2 filas colapsan). Si A = sí y B = sí el resultado sirve con o sin red
(2 filas colapsan). Quedan **5 casos**.

| A huella | B vigente | C red | Caso | Acción |
| --- | --- | --- | --- | --- |
| sí | sí | no aplica | **ACIERTO DE CACHÉ** | devolver el `generationId` guardado; 0 tokens; funciona sin red |
| sí | no | sí | **HUELLA VIEJA** | no se devuelve; se regenera contra la versión curricular vigente |
| sí | no | no | **HUELLA VIEJA SIN RED** | se encola `PENDING_NETWORK`; **no** se entrega el resultado viejo |
| no | no aplica | sí | **SIN CACHÉ CON RED** | invocar al proveedor una vez y guardar el resultado |
| no | no aplica | no | **SIN CACHÉ SIN RED** | se encola `PENDING_NETWORK` |

### Hallazgo de diseño

Aquí vive la respuesta a la pregunta del profesor sobre 2026 y 2027. La versión
curricular es parte de la huella, así que un pedido idéntico hecho en 2027 **no
encuentra** la huella de 2026: encuentra una huella vieja y la descarta.

Nótese que el ACIERTO DE CACHÉ **funciona sin red**. Es la única forma de
producir material con IA durante un corte, y sale gratis.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **Entregar la respuesta de 2026 porque no hay red** | Rosa enseña con contenido curricularmente obsoleto y nadie se entera: es peor que no entregar nada, porque el error es silencioso | la huella vieja nunca se entrega; se encola y se avisa |
| **Huella sin la versión curricular** | todo pedido repetido devuelve contenido viejo para siempre | `curriculum_version` es parte de la huella |
| **Huella sin el modelo** | se reutiliza la salida de otro modelo y la comparación con la línea base deja de ser válida | el identificador del modelo entra en la huella |
| **Caché sin fecha de expiración** | contenido de hace años se sigue sirviendo aunque nadie lo revise | la caché se invalida al publicarse una nueva versión curricular |

### Frases para el diagrama

- "Si la huella ya existe, se devuelve lo guardado: cero llamadas."
- "Un resultado de 2026 no se entrega en 2027, ni aunque no haya red."
- "La caché es lo único que produce material con IA durante un corte."

---

## PD-11 — ¿Este dato entra al prompt o se queda fuera?

**Quién decide:** el Normalizador y el Context Builder, al armar el archivo intermedio.
**Cuándo:** entre el formulario de Rosa y el prompt canónico.
**Por qué es el punto más importante:** el archivo intermedio **es la frontera de
costo**. Todo lo que entra ahí se paga; todo lo que se queda fuera es gratis para
siempre.

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿el dato es necesario para producir la respuesta? | sí / no |
| B | ¿ya viaja por otro campo estructurado del formulario? | sí / no |
| C | ¿se puede enviar solo el fragmento pertinente en vez del documento completo? | sí / no |

### Cruce exhaustivo

Nominalmente 2 x 2 x 2 = 8. Si A = no el dato se descarta sin evaluar nada más
(4 filas colapsan). Si B = sí ya es redundante y C no incide (2 filas colapsan).
Quedan **4 casos**.

| A necesario | B redundante | C acotable | Caso | Qué se hace | Ejemplo |
| --- | --- | --- | --- | --- | --- |
| no | no aplica | no aplica | **RUIDO** | se elimina | "Hola, ojalá puedas ayudarme, mil gracias" |
| sí | sí | no aplica | **REDUNDANTE** | se elimina; ya viaja como campo | "para cuarto de primaria" escrito en el texto libre |
| sí | no | sí | **ACOTABLE** | entran solo los fragmentos etiquetados | el temario completo de Comunicación |
| sí | no | no | **IMPRESCINDIBLE** | entra literal y cuenta contra el presupuesto | el objetivo pedagógico específico |

### De dónde sale la reducción

Desglose de una solicitud típica de Rosa, en tokens de entrada:

| Concepto | Clase | Libre | Con Gateway |
| --- | --- | ---: | ---: |
| Saludo y cortesías | RUIDO | 80 | 0 |
| Repite grado y curso ya puestos en el formulario | REDUNDANTE | 120 | 0 |
| Pega el temario completo de Comunicación | ACOTABLE | 1,100 | 352 |
| Objetivo pedagógico y restricciones | IMPRESCINDIBLE | 400 | 280 |
| Instrucciones de formato escritas a mano | IMPRESCINDIBLE | 300 | 210 |
| **Total** | | **2,000** | **842** |

Reducción del 58%, contra una meta del 40%. **El 55% del ahorro sale de un solo
caso: ACOTABLE.** Enviar dos fragmentos etiquetados en lugar del temario entero
es la decisión que sostiene la meta; lo demás es complemento.

### Hallazgo de diseño

Los casos RUIDO y REDUNDANTE juntos aportan 200 tokens: el 10% del ahorro. Si el
diseño solo limpiara saludos y repeticiones, **no llegaría nunca al 40%**. La
meta se gana en la selección de contexto, no en la limpieza de texto.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **Adjuntar el temario completo "por si acaso"** | se pierde el 55% del ahorro de una sola vez y la meta del 40% queda fuera de alcance | solo entran fragmentos etiquetados, con sus IDs registrados |
| **Arrastrar toda la conversación anterior** | el costo crece en cada pedido aunque el pedido sea igual de simple | el archivo intermedio guarda intención y referencias, no historial |
| **Descartar como RUIDO algo imprescindible** | la respuesta sale genérica, Rosa la rechaza y vuelve a pedir: se paga dos veces | solo se descarta lo que no aporta restricción; ante la duda, se pregunta |
| **Enviar los fragmentos como texto y además sus IDs** | se paga el contenido dos veces | los IDs son para el registro y la auditoría, no para el prompt |

### Frases para el diagrama

- "El archivo intermedio es la frontera de costo: lo que entra ahí, se paga."
- "El ahorro no está en quitar saludos; está en no mandar el temario completo."
- "Se envían dos fragmentos etiquetados, no el curso entero."

---

## PD-12 — ¿Qué se hace si no cabe en el presupuesto?

**Quién decide:** el Budget Guard, con el prompt canónico ya armado.
**Cuándo:** el último control antes de que el Gateway salga a Internet.

### Variables observables

| Var | Pregunta | Valores |
| --- | --- | --- |
| A | ¿el prompt cabe en el presupuesto de entrada? | sí / no |
| B | ¿se puede recortar el contexto sin perder el objetivo? | sí / no |
| C | ¿la salida estimada cabe en el presupuesto de salida? | sí / no |

### Cruce exhaustivo

Nominalmente 2 x 2 x 2 = 8. Si A = no la entrada se resuelve antes de estimar la
salida, así que C todavía no es observable (2 filas colapsan). Si A = sí no hay
nada que recortar y B no incide (2 filas colapsan). Quedan **4 casos**.

| A entrada | B reducible | C salida | Caso | Acción |
| --- | --- | --- | --- | --- |
| sí | no aplica | sí | **DENTRO DE PRESUPUESTO** | invocar una vez, con máximos de entrada y salida |
| sí | no aplica | no | **SALIDA EXCEDIDA** | recortar el formato pedido (menos preguntas, menos palabras) y recalcular |
| no | sí | no observable aún | **ENTRADA EXCEDIDA REDUCIBLE** | quitar los fragmentos menos pertinentes y volver a evaluar |
| no | no | no observable aún | **BLOQUEO** | no se invoca; se le explica a Rosa qué recortar |

### Hallazgo de diseño

El bloqueo **no es un error del sistema**: es el sistema funcionando. Un pedido
que no cabe en el presupuesto y no se puede recortar es un pedido que costaría
más que lo que la escuela tiene asignado. Bloquearlo antes de enviarlo cuesta
cero; enviarlo y recibir un cobro no.

El caso SALIDA EXCEDIDA es el que más se olvida: se controla el tamaño del
prompt y se ignora el de la respuesta, que en muchas tareas pedagógicas es la
parte cara.

### Peores casos

| Peor caso | Qué provoca | Mitigación en el diseño |
| --- | --- | --- |
| **Controlar solo la entrada** | la respuesta se desborda y el costo real duplica lo estimado | presupuesto de entrada **y** de salida, ambos obligatorios |
| **Recortar el objetivo para que quepa** | la respuesta ya no sirve, Rosa vuelve a pedir y se paga dos veces | se recorta contexto, nunca el objetivo |
| **Reintentar automáticamente tras el bloqueo** | cada reintento cuesta y ninguno cabe | el bloqueo devuelve el control al docente, no reintenta solo |
| **No registrar las llamadas fallidas** | el gasto real es mayor que el reportado y la meta del 40% miente | el ledger registra toda invocación, exitosa o fallida, con consumo |

### Frases para el diagrama

- "Si excede el presupuesto, se bloquea antes de enviar: bloquear cuesta cero."
- "Se recorta el contexto, nunca el objetivo."
- "Se presupuesta lo que entra y también lo que sale."

---

## Los tres trabajos del hash

El mismo cálculo resuelve tres problemas distintos. Distinguirlos es lo que
evita confundir "el archivo cambió" con "el archivo se rompió".

| Trabajo | Pregunta que responde | Dónde aparece |
| --- | --- | --- |
| **Integridad** | ¿llegó igual a como salió? | verificación de archivos y de bloques descargados |
| **Comparación** | ¿esto es lo mismo que ya tengo? | comparación de manifiestos, detección de cambio en fragmentos curriculares |
| **Identidad** | ¿ya vi esto antes? | `event_id` de la cola, huella de caché del AI Gateway |

La misma diferencia de hash significa cosas opuestas según contra qué se compare:

| Comparación | Momento | Distinto significa |
| --- | --- | --- |
| mi versión vieja contra la nueva de Lima | antes de bajar | hay contenido nuevo, hay que bajar (buena noticia) |
| lo que bajé contra el manifiesto de esa misma versión | después de bajar | se corrompió, hay que rechazar (mala noticia) |

---

## El peor caso del hash: colisiones

**Pregunta:** ¿cómo se garantiza que el sistema no genere dos hashes iguales para
contenidos distintos?

**No se garantiza.** Las colisiones existen por el principio del palomar: la
salida es de tamaño fijo (256 bits) y las entradas posibles son infinitas. La
garantía es probabilística, no lógica. Se sostiene en tres capas.

### Capa 1 — la magnitud

| Magnitud | Valor |
| --- | ---: |
| Archivos distintos en 10 años a escala nacional | 5,200,000 |
| Espacio de SHA-256 | 1.16 x 10^77 |
| Probabilidad de colisión accidental | 1.17 x 10^-64 |
| Ganar una lotería de 1 en 14 millones tres veces seguidas | 3.6 x 10^-22 |

La colisión es unos 40 órdenes de magnitud menos probable que la lotería
triple. Deja de ser el riesgo dominante: antes fallan los discos, la energía o
la memoria del nodo.

### Capa 2 — accidental no es lo mismo que intencional

| Algoritmo | Estado |
| --- | --- |
| MD5 | roto: se generan colisiones en segundos |
| SHA-1 | roto: ataque SHAttered, 2017 |
| SHA-256 | sin ataque práctico conocido |

Por eso el diseño especifica `sha256` y no `md5`. Es una decisión de
arquitectura, no un detalle de implementación.

### Capa 3 — el sistema no depende solo del hash

- El manifiesto va **firmado**: fabricar una colisión no basta, haría falta la
  llave privada de Lima.
- El `event_id` es **compuesto**: escuela, segundo y hash. El hash es un tercio.

**Postura defendible:** no se afirma que sea imposible. Se afirma que es
despreciable frente a los demás riesgos del sistema, y que aun así el diseño no
descansa en una sola barrera.

---

## Catálogo consolidado de peores casos

Lo que el diagrama debe nombrar explícitamente.

| # | Peor caso | Escena | Consecuencia si no se diseña | Cómo se ataja |
| --- | --- | --- | --- | --- |
| P1 | La ventana de conexión no alcanza | 2 | la escuela nunca actualiza | solo viajan diferencias; lo esencial tiene prioridad |
| P2 | Se pierde el índice de bloques validados | 3 | la descarga reinicia desde cero cada corte y nunca termina | el índice de bloques es persistente, no vive en memoria |
| P3 | Activación parcial | 4 | Rosa enseña con guía nueva y ficha vieja | activación atómica por puntero de versión |
| P4 | Firma o hash inválido sin versión anterior | 4 | la escuela queda sin material y nadie se entera | estado explícito y alerta en el panel de Valeria |
| P5 | RETIRADO olvidado | 4 | temas viejos visibles para siempre; disco lleno | el manifiesto es la lista autoritativa completa |
| P6 | El timestamp se toma al enviar | 6 | los avances se duplican en cada reintento | el timestamp se congela al crear el evento |
| P7 | Lima aplica el evento pero no guarda el `event_id` | 6 | duplicado en el reintento | aplicar y registrar en la misma transacción |
| P8 | La cola crece sin límite | 6 | disco lleno; se pierden eventos nuevos | tope de cola, prioridad y alerta |
| P9 | Colisión de hash | transversal | contenido falso aceptado como válido | SHA-256, firma del manifiesto e identificador compuesto |
| P10 | Se asume que habrá conexión durante la clase | 5 | el sistema no sirve para el caso real del enunciado | offline-first: el nodo responde siempre, la red es opcional |
| P11 | Manifiesto como delta encadenado | 2 | a la escuela atrasada le falta un eslabón y nunca se recupera | manifiesto de estado completo |
| P12 | El manifiesto describe solo su semana | 2 | Diego nunca ve el material de las semanas sin señal | el manifiesto lista todo lo vigente |
| P13 | Descargar las versiones en orden | 2 | 184 MB de 369 desperdiciados en versiones ya reemplazadas | se compara contra el manifiesto más nuevo |
| P14 | Atraso permanente invisible | 2 | la escuela queda congelada y nadie se entera | indicador de semanas de atraso en el panel de Valeria |
| P15 | Activar copiando archivos encima | 4 | un corte deja guía nueva con ficha vieja | cada versión en su directorio; se mueve un puntero |
| P16 | Mover el puntero antes de verificar | 4 | la escuela sirve material corrupto o no firmado | verificar siempre antes de activar |
| P17 | Borrar la versión anterior antes de activar | 4 | si la activación falla, no hay a qué volver | se borra después, y solo si la nueva quedó activa |
| P18 | Salto de reloj por sincronización NTP entre crear y reenviar | 6 | el identificador cambia y el duplicado se cuela | contador local monótono además del tiempo |
| P19 | Ordenar la auditoría por la hora del nodo | 6 | avances desordenados o fechados en el futuro | se ordena por `received_at` de Lima |
| P20 | Sincronizar sin límite durante la clase | 5 | Rosa no puede abrir material que ya está en el nodo | tope de ancho de banda en horario de clase |
| P21 | Todas las escuelas sincronizan a la misma hora | 2 | pico de carga sobre el almacenamiento central | espera aleatoria por escuela |
| P22 | Borrar la cola para liberar espacio | 6 | se pierden avances que no existen en ningún otro lado | la cola se envía, nunca se borra sin confirmación |
| P23 | Nodo dimensionado a 4 GB | 4 | la activación atómica nunca puede ejecutarse | mínimo de 8 GB por nodo |
| P24 | Disco al 100% | 4 | no se puede registrar ni el fallo: falla silenciosa | alerta al 85% y freno de la descarga opcional |
| P25 | El Clarification Gate invoca al modelo para preguntar | 9 | se gastan tokens en el paso que existe para no gastarlos | las preguntas salen de la plantilla, no del modelo |
| P26 | Entregar el resultado de 2026 porque no hay red | 9 | Rosa enseña con contenido obsoleto y el error es silencioso | la huella vieja se encola, nunca se entrega |
| P27 | Huella de caché sin la versión curricular | 9 | todo pedido repetido devuelve contenido viejo para siempre | `curriculum_version` es parte de la huella |
| P28 | Adjuntar el temario completo "por si acaso" | 8 | se pierde el 55% del ahorro y la meta del 40% queda fuera de alcance | solo entran fragmentos etiquetados |
| P29 | Arrastrar toda la conversación anterior | 8 | el costo crece en cada pedido aunque el pedido sea simple | el archivo intermedio guarda intención y referencias, no historial |
| P30 | Avisar de la cuota agotada al final | 7 | Rosa completa todo y choca con un muro que existía desde el inicio | la cuota se evalúa antes de la primera pregunta |
| P31 | Controlar solo los tokens de entrada | 9 | la respuesta se desborda y el costo real duplica lo estimado | presupuesto de entrada y de salida |
| P32 | No registrar las llamadas fallidas | 10 | el gasto real supera al reportado y la meta del 40% miente | el ledger registra toda invocación, con o sin éxito |
| P33 | Medir contra una línea base no comparable | 10 | el 40% es un número inventado; distinta tarea o distinto modelo | la línea base fija tarea, modelo y versión curricular |
| P34 | El prompt vive en el chat del docente | 8 | no se puede reutilizar, versionar ni auditar el gasto de 2026 | la biblioteca de prompts guarda plantillas versionadas |

---

## Pendientes

Los doce puntos de decisión identificados están resueltos: PD-1 a PD-8 cubren la
distribución (iteración #2) y PD-9 a PD-12 la gobernanza de tokens (iteración #3).

### Cambios que este análisis obliga a llevar a otros documentos

| Documento | Qué falta actualizar | Origen |
| --- | --- | --- |
| `Architecture.md` | declarar el manifiesto como estado completo | PD-4 |
| `Architecture.md` | fijar el orden descargar, verificar, activar, borrar, y la activación por puntero | PD-5 |
| `Architecture.md`, entidades | `outbox_events` necesita `seq`, `created_at` y `received_at` | PD-6 |
| `Architecture.md`, estimaciones | mínimo de 8 GB por nodo escolar | PD-8 |
| `Architecture.md`, entidades | `ai_generations` necesita `curriculum_version` dentro de `request_hash` | PD-10 |
| `Requirements/NonFunctional.md` | tope de ancho de banda en horario de clase; umbral de disco al 85% | PD-7, PD-8 |
| `Requirements/Functional.md` | evaluar la cuota antes de pedir aclaraciones | PD-9 |

### Candidatos para una siguiente pasada

1. **PD-13 Rotación de llaves de firma.** Qué pasa con una escuela que estuvo
   meses sin red cuando Lima ya rotó la llave con la que firma los manifiestos.
2. **PD-14 Escuela dividida o fusionada.** Cambia el `school_id` y con él la
   identidad de los eventos en cola.
3. **PD-15 Solicitud de IA encolada que caduca.** Una solicitud `PENDING_NETWORK`
   creada contra la versión curricular 2026.2 que recién sale cuando ya rige la
   2027.1.

## Diagramas que salen de este contexto

| Archivo | Qué muestra |
| --- | --- |
| [02-topdown-remoteschooly-v2.excalidraw](02-topdown-remoteschooly-v2.excalidraw) | Top Down Design: personas, requerimientos y las tres iteraciones acumulativas |
| [03-arquitectura-remoteschooly.excalidraw](03-arquitectura-remoteschooly.excalidraw) | Arquitectura por zonas con sus bases de datos, los peores casos P1 a P34 sobre el componente que los ataja, y la historia en diez escenas |

## Registro

| Fecha | Cambio |
| --- | --- |
| 2026-09-03 | Versión inicial: PD-1, PD-2, PD-3, trabajos del hash, colisiones y catálogo de peores casos |
| 2026-09-03 | PD-4 resuelto: manifiesto de estado completo. Se declara la propiedad que faltaba, se mide el ahorro (50%) y se agregan P11 a P14 |
| 2026-09-03 | PD-5 a PD-8 resueltos. Se define la activación por puntero, el identificador de evento independiente del reloj, la prioridad de la clase sobre la sincronización y la jerarquía de borrado. Se agregan P15 a P24 |
| 2026-09-03 | Diagrama de arquitectura `03-arquitectura-remoteschooly.excalidraw` generado desde este contexto. Se corrige P18, que duplicaba a P6 |
| 2026-09-03 | PD-9 a PD-12 resueltos (iteración #3). Se define el orden de evaluación del Gate, la huella con versión curricular, la clasificación del archivo intermedio y el doble presupuesto. Se agregan P25 a P34 |
