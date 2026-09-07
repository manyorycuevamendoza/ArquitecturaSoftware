# Prompt para requisitos: del usuario nace el requerimiento

Un requisito sin usuario detrás no es un requisito, es una decisión técnica
buscando excusa.

Este archivo es el método que usamos en el Lab 4 para corregir los
requerimientos después de tener los diagramas. Sirve para copiar y pegar.

El método hermano, para construir los diagramas, está en
[estructura-diagramas.md](estructura-diagramas.md) y
[casos-posibles.md](casos-posibles.md).

---

## El orden que funcionó

Los requisitos no se escriben una vez. Se corrigen en tres pasadas, y cada una
responde a una pregunta distinta.

| Pasada | Pregunta que responde | De dónde saca la respuesta |
| --- | --- | --- |
| 1 | ¿Dice el requisito lo mismo que dibujé? | del diagrama |
| 2 | ¿De quién nace este requisito? | de las personas |
| 3 | ¿Qué me van a preguntar que el diagrama no contesta? | del patrón de preguntas del profesor |

Saltarse la pasada 1 produce requisitos que suenan bien y no describen el
sistema. Saltarse la 2 produce requisitos cuyo responsable es "Plataforma".
Saltarse la 3 produce una sustentación en la que improvisás.

---

## Pasada 1. Alinear los requisitos con el diagrama

```
Tengo los diagramas en [RUTA] y los requerimientos en [RUTA].

Los requisitos se escribieron ANTES que los diagramas, así que los lienzos
declaran decisiones que los requisitos no recogen. Auditalos.

Para cada requisito existente:
- ¿Su texto dice lo mismo que el diagrama? Si el diagrama es más específico,
  el requisito está incompleto.
- ¿Su criterio de aceptación es verificable, o es una intención?

Para cada decisión que aparece en el diagrama:
- ¿Existe un requisito que la exija? Si no, falta.

Reglas al corregir:
- Conservá los IDs existentes y su significado, para no romper la trazabilidad
  con los demás documentos. Afiná su redacción y agregá IDs nuevos al final.
- Cada requisito lleva una columna que dice de qué punto de decisión sale.
- Al terminar, actualizá los rangos de IDs citados en los otros documentos.

Decime primero qué encontraste, antes de escribir nada.
```

**Lo que esto encontró en el Lab 4.** `FR-DIS-02` decía "descargar solo archivos
nuevos o modificados" y nunca decía que hay que borrar los retirados. Sin ese
requisito, la caché crece hasta llenar el disco mostrando temas de semanas
viejas para siempre. `FR-DIS-05` pedía verificar antes de activar, pero no decía
**cómo** se activa: la activación atómica por puntero estaba dibujada y no
exigida en ningún lado.

De 14 requisitos pasamos a 42.

---

## Pasada 2. Cada requisito declara de qué usuario nace

```
Cada requisito tiene que declarar el usuario responsable: la persona cuya
necesidad lo justifica, NO el componente que lo implementa.

- "Plataforma", "Sistema", "Backend" y "Nodo Local" no son usuarios. Son
  componentes. Si un requisito tiene un componente como responsable, buscá a
  quién le sirve y ponelo a él.
- Los sistemas externos (un proveedor, una pasarela) tampoco son responsables:
  no tienen necesidad propia dentro del caso.

Después construí la tabla al revés: por cada persona, qué necesita y qué
requisitos nacen de ahí.

Al terminar decime:
- ¿Quedó algún requisito sin persona? Ese es una decisión técnica sin
  necesidad que la justifique.
- ¿Quedó alguna persona sin requisitos? Esa no es una persona del caso.
- ¿El reparto tiene sentido, o hay una persona con el 80%?
```

**Por qué la tabla inversa importa más que la columna.** La columna la mirás vos
al escribir. La tabla inversa es la que usás en la sustentación, porque el
profesor no pregunta "¿de quién nace FR-DIS-07?", pregunta "¿y a Rosa esto en
qué le sirve?".

En el Lab 4 quedó: Valeria 19 requisitos, Rosa 12, Diego 8, Administrador
regional 3.

---

## Pasada 3. Las preguntas que el diagrama no contesta solo

Un profesor no pregunta al azar. Repite seis formas de la misma auditoría.

| # | Arquetipo | Cómo suena | Qué está buscando |
| --- | --- | --- | --- |
| 1 | Propósito de una caja | "¿Qué hace el register service?" | una caja con nombre vago que nadie sabe explicar |
| 2 | Camino alterno | "¿Qué pasa cuando el remitente va a la oficina?" | un flujo que existe y no dibujaste |
| 3 | Paso sin validación | "¿En el retiro no se valida nada?" | un paso donde entra algo y nadie lo revisa |
| 4 | Origen de un identificador | "¿Dónde se genera el código único?" | un ID que aparece de la nada |
| 5 | Propósito de una pieza de soporte | "¿Para qué es la reconciliación?" | una caja que pusiste porque quedaba bien |
| 6 | Multiplicidad | "¿Qué pasa con múltiples bancos en cada país?" | un uno que en realidad son muchos |

### Prompt

```
Auditá mi diseño contra estos seis arquetipos de pregunta:

1. PROPÓSITO. Por cada caja del diagrama: ¿su nombre dice lo que hace? Las
   cajas con nombre en inglés o genérico son las primeras que preguntan.
2. CAMINO ALTERNO. ¿Qué flujos existen y no dibujé? El primer uso, el alta de
   un elemento nuevo, el caso sin historial previo.
3. VALIDACIÓN. Recorré cada flecha que entra a una caja: ¿alguien revisa lo
   que llega, o solo se procesa?
4. IDENTIFICADORES. Listá cada ID del sistema y decime dónde nace, quién lo
   genera y en qué momento. El que no tenga respuesta es un hueco.
5. PIEZAS DE SOPORTE. Por cada base de datos, cola o registro: ¿qué pregunta
   responde? Si no responde ninguna, sobra.
6. MULTIPLICIDAD. Por cada actor y componente: ¿qué pasa si hay dos, o
   quinientos? ¿Al mismo tiempo?

Para cada hueco decime si lo cubre un requisito existente, y si no, escribí el
que falta.

Los diagramas ya están cerrados: la cobertura va en los requisitos.

Al final armá una tabla de preguntas previsibles con el requisito que responde
a cada una, para tenerla a mano en la sustentación.
```

**Lo que esto encontró en el Lab 4.** El hueco grande fue el login. `FR-AI-09`
exigía autenticación pero no decía **cómo entra la docente cuando no hay
Internet**. Si la sesión se resuelve contra la central, el login se cae justo
durante el corte, que es el escenario para el que se diseñó todo lo demás. Es el
arquetipo 2 y el 5 juntos, y en el tema que al profesor le importaba.

También salió que la central deduplicaba eventos por identificador pero no
validaba su contenido (arquetipo 3), que `requestId` y `generationId` no tenían
lugar de origen declarado (arquetipo 4), y que un nodo nuevo no tenía forma de
obtener la llave con la que verifica firmas (arquetipo 2).

De 42 pasamos a 49.

---

## Verificación por código

No se entrega sin correr esto. Cada pasada agrega una comprobación.

```python
import re, io
fn = io.open("Requirements/Functional.md", encoding="utf-8").read()
nf = io.open("Requirements/NonFunctional.md", encoding="utf-8").read()
personas = ("Rosa", "Diego", "Valeria", "Administrador regional")
filas = re.findall(r'^\| ((?:N?FR)-[A-Z]+-\d+) \|(.+)$', fn + "\n" + nf, re.M)
definidos = {f for f, _ in filas}

print("Requisitos:", len(filas))
print("Sin usuario responsable:",
      [f for f, r in filas if not any(p in r for p in personas)] or "ninguno")
print("Con un componente como responsable:",
      [f for f, r in filas if re.search(r'\| (Plataforma|Sistema|Backend) \|', r)] or "ninguno")
```

Y sobre la tabla inversa: ningún ID citado que no exista, ningún requisito que
ninguna persona reclame.

| Comprobación | Qué detecta |
| --- | --- |
| requisitos sin usuario responsable | decisiones técnicas sin necesidad detrás |
| responsables que son componentes | el error que el profesor señala |
| IDs citados que no existen | trazabilidad rota al renumerar |
| requisitos que nadie reclama | requisitos huérfanos que sobran |
| rangos citados en otros documentos | `FR-AI-01..08` que quedó viejo al agregar el 09 |

---

## Errores que ya costaron una pasada

**Reescribir una tabla y perder una columna.** Al alinear los requisitos con el
diagrama se cambió la columna Responsable por una columna PD, y se perdió el
usuario. La corrección del profesor fue exactamente sobre eso. Si reescribís una
tabla, comparala con la anterior columna por columna antes de guardar.

**Poner "Plataforma" como responsable.** Es cómodo y no significa nada. Un
componente no tiene necesidades, solo implementa las de alguien.

**Escribir el requisito antes que el diagrama y no volver.** El diagrama obliga
a decidir cosas que el requisito dejaba abiertas. Después de dibujar, siempre
hay una pasada de corrección pendiente.

**Confundir dos fallos parecidos.** En el Lab 4, "no hay red en la escuela" y
"el proveedor no responde" se veían como un solo caso. Son distintos: en el
segundo la petición sí salió, y puede haber facturado tokens antes de fallar.

**Dar por cubierto lo que no está dibujado.** Antes de decir que el diagrama
contesta una pregunta, buscá el texto en el lienzo. Reconocer que algo está en
el requisito y no en el dibujo vale más que fingir que está en los dos.
