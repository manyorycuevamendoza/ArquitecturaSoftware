# Prompt para diagramas de arquitectura

Estructura que funcionó para el Problema 1 del Lab 4. Pegar el prompt completo,
reemplazando lo que está entre corchetes.

El método detrás está en [casos-posibles.md](casos-posibles.md). Este archivo es
la versión lista para copiar y pegar.

---

## Prompt completo

```
Quiero armar los diagramas de arquitectura de [TEMA / PROBLEMA].

Contexto: [dos o tres líneas del caso, o la ruta del archivo donde está].

Seguí este método, en este orden, sin saltarte pasos.

PASO 1. ENUMERAR LOS CASOS
Para cada punto de decisión:
- Declara las variables observables en el momento de decidir. Solo lo que el
  sistema puede ver ahí. Nómbralas A, B, C.
- Calcula el producto cartesiano completo y muéstrame todas las filas.
- Colapsa las que no aportan (imposibles, no observables, equivalentes) y
  explica por qué. Di cuántas quedan.
- Asigna una acción a cada caso que sobreviva.
- Dime qué hallazgo de diseño sale del cruce.
- Lista los peores casos y cómo los ataja la arquitectura.
No inventes casos para llenar la tabla. Si son cuatro, quiero saber por qué no
hay un quinto.

PASO 2. CONSOLIDAR
Junta todos los peores casos en un catálogo numerado P1, P2, P3...
Cada uno con: qué provoca si no se diseña, y cómo lo ataja el diseño.

PASO 3. ESCRIBIR EL GUION, ANTES DE DIBUJAR
- Empieza por una persona, no por un componente.
- Una escena por paso, en dos o tres oraciones, en lenguaje corriente.
- Termina en la persona que recibe el beneficio.
- Numera las escenas corrido.
Después decime qué escena corresponde a cada caja.

PASO 4. AGRUPAR EN BLOQUES
Si hay más de tres o cuatro puntos de decisión, agrúpalos por lo que comparten,
no por su número. Cada bloque es un lienzo. Decime por qué agrupaste así.

PASO 5. CORTAR CADA BLOQUE EN TRES ITERACIONES ACUMULATIVAS
- Iteración 1: la pregunta. El sistema como una caja.
- Iteración 2: se abre la caja. Aparece el cruce de casos.
- Iteración 3: la capa que faltaba.
Ninguna reemplaza a la anterior. Las flechas punteadas entre iteraciones
muestran que es la misma historia.

PASO 6. GENERAR CON CÓDIGO
El .excalidraw es un JSON: genéralo con un script de Python, no a mano.
Antes de dármelo verifica: JSON válido, ninguna caja superpuesta, ningún texto
desbordando su recuadro, ningún bloque de guion pisándose con otro.

CONVENCIÓN VISUAL, obligatoria:
- Fondo transparente en TODAS las figuras. El color vive solo en el borde.
- Azul: personas. Rojo: servicios que mueven datos. Morado: componentes que
  deciden. Cyan y elipse: bases de datos y almacenes.
- Verde: resultado bueno. Naranja: degradado pero recuperable. Rojo: rechazo.
- Borde punteado: una zona, o un caso imposible.
- Monoespaciada: identificadores, tablas de cruce, órdenes de operación.
- El guion numerado va en la columna izquierda, el diagrama a la derecha.
- Leyenda de peores casos al pie de cada lienzo.

CÓMO ESCRIBIR LOS TEXTOS:
Es para exponer en la universidad y lo presento como mío. Nada de rayas largas.
Frases cortas, conectores naturales, que suene a alguien hablando.

AL FINAL:
Un lienzo más que junte todos los bloques, con un guion general numerado del 1
al 10 y una tabla que sume los casos de cada punto de decisión.
```

---

## Variante corta

Cuando el paso 1 y 2 ya están hechos y solo falta dibujar:

```
Ya tengo los casos enumerados en [ARCHIVO].

Armame los diagramas siguiendo la misma estructura de Lab4/Diagrams/Problema1:
guion numerado en la columna izquierda, tres iteraciones acumulativas por
lienzo, fondo transparente y color solo en el borde, leyenda de peores casos al
pie, generado con un script de Python y verificado antes de dármelo.

Reusá Lab4/Diagrams/Problema1/generadores/_lib.py.

Empezá escribiendo el guion, antes de dibujar nada.
```

---

## Qué revisar antes de darlo por bueno

| Revisión | Cómo se comprueba |
| --- | --- |
| Los casos son exhaustivos | el número sale del producto cartesiano, no de una lista |
| Cada colapso está justificado | hay una razón escrita por cada fila descartada |
| El guion empieza en una persona | la primera caja es un actor, no un servicio |
| Las iteraciones son acumulativas | la 3 conserva lo de la 2, no lo reemplaza |
| Ningún texto se sale de su caja | verificación por código antes de abrir el archivo |
| No hay rellenos de fondo | verificación por código: `backgroundColor` transparente |

---

## Errores que ya costaron una pasada

**Dibujar antes de escribir el guion.** El diagrama sale como cajas técnicas
sueltas y no se puede explicar. Si el guion no existe, el diagrama tampoco.

**Empezar por un componente.** Una arquitectura arranca cuando una persona hace
algo. Si la primera caja es un servicio, falta el principio de la historia.

**Rellenar las cajas de color.** Recarga el lienzo. El color en el borde alcanza
para clasificar y deja el fondo limpio.

**Meter todos los casos en un solo lienzo.** Treinta cajas no se sustentan.
Cuatro lienzos de diez sí.

**Escribir el JSON a mano.** Cajas descuadradas y textos encimados. Con script
se verifica antes de abrirlo.
