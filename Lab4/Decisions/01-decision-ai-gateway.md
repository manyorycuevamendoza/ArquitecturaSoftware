# Enumeración de casos — Punto de decisión del AI Gateway

Documento previo al diagrama. No se dibujan cajas hasta saber **cuántas ramas
tiene la decisión y por qué son exactamente esas**. La enumeración es
exhaustiva y verificable: el producto cartesiano se cuenta, y toda combinación
descartada lleva su razón escrita.

El punto de decisión de sincronización (manifiesto local contra manifiesto de
Lima) ya está resuelto en [../Architecture.md](../Architecture.md). Este
documento cubre el punto de decisión que faltaba: el del AI Gateway, corazón
del capítulo 2 del diagrama narrativo.

---

## Punto de decisión

| | |
| --- | --- |
| **Quién decide** | El AI Gateway, en su parte local (Nodo Escolar Local). |
| **Con qué información** | La solicitud intermedia enviada + la plantilla vigente de la biblioteca de prompts + la identidad de Rosa (login) + el estado del enlace. |
| **En qué momento** | Después del submit del formulario y **antes** de cualquier token facturado. |

---

## 1. Variables observables

| Var | Pregunta | Valores | Por qué es observable aquí |
| --- | --- | --- | --- |
| **A** | ¿Están completos los campos obligatorios que exige la plantilla? | sí / no | La plantilla (`prompt_templates.required_fields`) está en la biblioteca local; comparar es una operación de texto, 0 tokens. |
| **B** | ¿La huella de la solicitud ya existe en caché con un resultado aprobado? | sí / no | La huella es `hash(prompt_id + version + valores de campos + chunkIds + modelo + curriculum_version)`; se calcula sin red. |
| **C** | ¿El presupuesto alcanza para la llamada estimada? | sí / no | Cuota del docente (`users.token_quota`) + tope de la plantilla (`budget`) contra la estimación local de tokens. |
| **D** | ¿Hay conectividad hacia Lima en este instante? | sí / no | Estado del enlace que ya mantiene el Sync Agent. |

### Declaradas y descartadas por no ser observables en ese instante

| Variable candidata | Por qué se descarta |
| --- | --- |
| Calidad pedagógica de la respuesta | No existe todavía; solo se observa después de generar. |
| Tokens realmente facturados | Antes de enviar solo hay estimación; el valor real llega en `ai_generations`. |
| Si el proveedor responderá con error | Se observa en la respuesta, no en la decisión. |
| Si Rosa aceptará el resultado | Es un evento posterior; no puede condicionar la rama. |

**Nota sobre B.** Solo es calculable si A = sí: sin los valores de los campos
no hay huella que hashear. Esto no invalida el cruce; hace que las ocho filas
con A = no colapsen, y ese colapso se justifica en el paso 3.

---

## 2. Producto cartesiano

Cálculo: 2 × 2 × 2 × 2 = **16 filas**. La tabla las tiene todas.

| # | A: campos | B: caché | C: presupuesto | D: red | Estado |
| ---: | --- | --- | --- | --- | --- |
| 1 | no | sí | sí | sí | colapsa |
| 2 | no | sí | sí | no | colapsa |
| 3 | no | sí | no | sí | colapsa |
| 4 | no | sí | no | no | colapsa |
| 5 | no | no | sí | sí | colapsa |
| 6 | no | no | sí | no | colapsa |
| 7 | no | no | no | sí | colapsa |
| 8 | no | no | no | no | colapsa |
| 9 | sí | sí | sí | sí | **vive** |
| 10 | sí | sí | sí | no | **vive** |
| 11 | sí | sí | no | sí | **vive** |
| 12 | sí | sí | no | no | **vive** |
| 13 | sí | no | sí | sí | **vive** |
| 14 | sí | no | sí | no | **vive** |
| 15 | sí | no | no | sí | **vive** |
| 16 | sí | no | no | no | **vive** |

---

## 3. Descarte, con razón escrita

| Filas | Descarte | Razón |
| --- | --- | --- |
| 1–8 | Colapsan en **un solo caso** | Con A = no la huella no existe (B es indefinida: no hay valores que hashear), la estimación de tokens no es fiable (C es indefinida) y no hay nada que enviar (D es irrelevante). El Gateway ni siquiera llega a evaluar B, C ni D. Las ocho filas producen la misma acción por la misma causa. |
| 10, 12 | **Condicionadas a un supuesto que hay que declarar** | Un acierto de caché sin red solo existe si la caché de resultados vive en el Nodo Escolar Local. Si viviera solo en Lima, B no sería observable con D = no y ambas filas serían imposibles. **Ningún requisito lo dice**: `FR-AI-06` exige reusar, no dice dónde. Se resuelve a favor del nodo local por coherencia con offline-first, y queda como supuesto explícito, no como hecho del enunciado. |

Sobreviven **9 casos**: uno por colapso, más los ocho con A = sí.

---

## 4. Casos finales

| # | Caso | Cómo se detecta | Acción del sistema | Estado resultante | Qué ve Rosa |
| ---: | --- | --- | --- | --- | --- |
| 1 | **FALTA DATO** | `required_fields` de la plantilla vigente contra los campos enviados | Devuelve máximo tres preguntas concretas; no crea registro en `ai_generations` | `NEEDS_CLARIFICATION` | Tres preguntas cortas y su formulario con lo ya escrito. Ningún costo |
| 2 | **REUSO** (fila 9) | Huella idéntica en caché, con red | Devuelve el `generationId` existente | `REUSED` | Su ficha, al instante. «Reutilizado, sin costo» |
| 3 | **REUSO OFFLINE** (fila 10) | Huella idéntica en la caché local, sin red | Devuelve el resultado guardado en el nodo | `REUSED_OFFLINE` | Su ficha, sin Internet. Prueba de que el nodo responde solo |
| 4 | **REUSO SIN CUOTA** (fila 11) | Huella en caché, consultada **antes** de mirar el presupuesto | Devuelve el resultado; no descuenta cuota | `REUSED` + marca `quota_exhausted` | Recibe su material aunque su cuota esté agotada |
| 5 | **REUSO SIN CUOTA NI RED** (fila 12) | Igual que el caso 4, con el enlace caído | Devuelve el resultado de la caché local | `REUSED_OFFLINE` + marca | Lo mismo, en el peor escenario posible |
| 6 | **GENERAR** (fila 13) | Sin huella, el presupuesto alcanza, hay red | Invoca al proveedor una sola vez, con topes de entrada y salida | `GENERATED` | Su ficha nueva. **Único paso que cuesta dinero** |
| 7 | **PENDIENTE DE RED** (fila 14) | Sin huella, el presupuesto alcanza, sin red | Encola la solicitud ya normalizada y **reserva** la cuota | `PENDING_NETWORK` | «Lista y en cola: se genera cuando vuelva Internet» |
| 8 | **PRESUPUESTO EXCEDIDO** (fila 15) | Sin huella, la estimación supera el tope, hay red | Bloquea antes de enviar y propone reducir alcance o salida | `BUDGET_BLOCKED` | «Reduce la duración o el formato», con el número que se pasó |
| 9 | **BLOQUEO SIN RED** (fila 16) | Sin huella, la estimación supera el tope, sin red | Bloquea y **no encola** | `BUDGET_BLOCKED` | El mismo mensaje. No se le promete algo que sería rechazado después |

### Casos con la misma acción que se mantienen separados

- **2 y 3**, **4 y 5** hacen lo mismo —devolver la caché— pero solo 3 y 5
  demuestran `NFR-AVL-01`: la clase no depende de la red. En el diagrama son la
  evidencia visual del offline-first.
- **8 y 9** bloquean igual, pero 9 además decide **no encolar**. Fundirlos
  produce el bug de la cola envenenada: solicitudes que esperan horas para ser
  rechazadas al llegar.

### Orden de evaluación que impone el cruce

```
A (campos) → B (caché) → C (presupuesto) → D (red)
```

Los casos 4 y 5 demuestran que **la caché va antes que el Budget Guard**. El
orden natural al diseñar es «primero valido que pueda gastar»; con ese orden,
una docente sin cuota queda bloqueada de un resultado que es gratuito. El
diagrama de flujo de IA en [../Architecture.md](../Architecture.md) hoy dibuja
`Presupuesto → Caché`: esta enumeración dice que hay que invertirlo.

---

## 5. Caso crítico: PENDIENTE DE RED (caso 7)

Es el que más se olvida al diseñar y el que rompe el sistema en producción, por
dos razones.

**Se olvida porque no aparece si desarrollas con Internet.** En un ambiente
conectado D siempre vale sí, y las filas 10, 12, 14 y 16 nunca se ejecutan. Se
descubren en la escuela, no en el laboratorio.

**Rompe el sistema porque la solicitud sobrevive a la versión curricular.** Una
solicitud encolada bajo `curriculum_version = 2026.2` puede drenarse días
después, cuando el nodo ya activó `2027.1`. Si la cola se envía tal cual, o se
gastan tokens sobre `selectedChunkIds` que ya no existen, o se devuelve una
ficha que cita fragmentos retirados. La huella se calculó contra un currículo
muerto.

> **Regla que sale de aquí:** al drenar la cola, el Gateway recalcula la huella
> contra la versión curricular vigente y vuelve a pasar por A, B y C antes de
> enviar. Un elemento encolado no es un permiso de gasto; es una intención que
> se revalida.

**Corolario sobre la cuota.** Si el caso 7 no reserva presupuesto al encolar,
veinte solicitudes en cola pueden drenarse juntas y romper la cuota mensual en
un minuto. Por eso la acción del caso 7 dice «reserva la cuota», no solo
«encola».

---

## 6. Frases para el diagrama

Una por caso, en presente, listas para pegar como etiqueta en el lienzo.

| Caso | Frase |
| ---: | --- |
| 1 | Falta un dato: el sistema pregunta tres cosas concretas y no gasta nada. |
| 2 | Alguien ya pidió esto mismo: se devuelve el resultado guardado, sin costo. |
| 3 | No hay Internet, pero la respuesta ya estaba en la escuela: se entrega igual. |
| 4 | La cuota de Rosa está agotada; como el resultado ya existe, se le entrega sin cobrarle. |
| 5 | Sin cuota y sin Internet, el nodo local todavía responde con lo que guardó. |
| 6 | Es una petición nueva y todo está en orden: se llama al modelo una sola vez. **Este es el único paso que cuesta dinero.** |
| 7 | Está lista pero no hay red: queda en cola y se revalida contra el currículo vigente antes de enviarse. |
| 8 | La petición pide más de lo permitido: se detiene antes de gastar y se propone recortarla. |
| 9 | Se pasa del presupuesto y además no hay red: se rechaza ahora y no se encola. |

---

## 7. Lo que la enumeración destapó y falta en la documentación

Declarado, no inventado: son huecos reales, no requisitos nuevos que este
documento se conceda a sí mismo.

1. **Dónde vive la caché de resultados.** `FR-AI-06` exige reutilizar pero no
   ubica la caché. Los casos 3 y 5 solo existen si está en el Nodo Escolar
   Local. Requiere una línea explícita en `FR-AI-06` o un `NFR` propio.
2. **Revalidación al drenar la cola.** Ningún requisito obliga a recalcular la
   huella contra la versión curricular vigente. Es lo que impide que
   `PENDING_NETWORK` se convierta en gasto sobre contenido muerto.
3. **Reserva de cuota al encolar.** `FR-AI-05` aplica topes por llamada, no por
   cola pendiente. Sin reserva, el presupuesto se controla por solicitud pero no
   por lote.

---

## Referencia: el punto de decisión ya resuelto (sincronización)

Se incluye para que ambos puntos de decisión queden en un mismo lugar antes de
dibujar.

**Punto de decisión:** el Nodo Escolar Local compara su manifiesto local contra
el manifiesto que acaba de publicar Lima, para decidir qué transferir.

**Variables observables:** A, ¿el archivo está en mi manifiesto local?;
B, ¿el archivo está en el manifiesto de Lima?; C, si está en ambos, ¿el hash
coincide?

| A: en mi lista | B: en Lima | C: hash | Caso | Acción |
| --- | --- | --- | --- | --- |
| no | sí | — (no hay previo) | NUEVO | bajar |
| sí | sí | distinto | EDITADO | bajar |
| sí | sí | igual | SIN CAMBIO | no bajar |
| sí | no | — | RETIRADO | quitar de la caché |
| no | no | — | *imposible: el archivo no existe* | descartado |

Nota de diseño que sale del cruce: el caso NUEVO **no se detecta por hash** —no
hay hash previo con qué comparar—, se detecta por el identificador del archivo.
El hash de un archivo nuevo se usa después, para verificar la descarga.
