# Método: del punto de decisión al diagrama

Cómo se construyó el diagrama de PD-1 (`Lab4/Diagrams/04-pd1-iteraciones.excalidraw`).
Seis pasos. El primero es el prompt de casos posibles; los otros cinco son lo que
vino después.

---

## Paso 1. Enumerar todos los casos posibles

Este es el prompt raíz. Sirve para cualquier decisión de arquitectura.

### Prompt

```
Tengo un punto de decisión en mi arquitectura: [DESCRIBIR LA DECISIÓN].

Quiero enumerar TODOS los casos posibles, no los que se me ocurran.

Hazlo así:

1. Declara las variables observables en el momento de decidir. Solo lo que
   el sistema puede ver ahí, no lo que sabría después. Nómbralas A, B, C
   y dime qué valores toma cada una.

2. Calcula el producto cartesiano completo. Si son tres variables binarias,
   son ocho filas y quiero ver las ocho.

3. Colapsa las filas que no aportan:
   - imposibles: explica por qué no pueden ocurrir
   - no observables: cuando una variable no se puede evaluar porque otra
     lo impide
   - equivalentes: cuando dos filas llevan a la misma acción
   Di cuántas filas quedan y por qué.

4. Asigna una acción a cada caso que sobreviva.

5. Dime qué hallazgo de diseño sale de este cruce. Sobre todo si hay una
   fila imposible: esa fila suele demostrar que el orden de operaciones
   es correcto.

6. Lista los peores casos: qué pasa si el diseño NO contempla cada uno,
   y cómo lo ataja la arquitectura.

No inventes casos para llenar la tabla. Si son cuatro, son cuatro, y
quiero saber por qué no hay un quinto.
```

### Por qué funciona

La pregunta "¿qué casos hay?" produce una lista incompleta y no verificable.
La pregunta "¿cuántas combinaciones tienen estas variables?" produce un número
demostrable. Si son tres variables binarias son ocho filas, y cualquiera puede
comprobar que están las ocho.

El colapso es la parte que enseña. Cuando una fila se descarta hay que explicar
por qué, y esa explicación casi siempre es una propiedad del diseño que no se
había declarado.

**Ejemplo de PD-1.** Tres variables: está en local, está en remoto, coinciden
los hashes. La fila "no está en local y no está en remoto" se descarta porque
un archivo que no está en ninguna lista no existe. De ahí sale el hallazgo: el
caso NUEVO no se detecta por hash sino por ruta, porque un archivo nuevo no
tiene hash previo con qué compararse.

**Ejemplo de PD-5.** Dos variables: archivos verificados, puntero movido. La
fila "puntero movido pero archivos sin verificar" es imposible solo si el orden
es descargar, verificar, activar. Esa fila imposible es la prueba de que el
orden está bien.

---

## Paso 2. Consolidar en un catálogo de peores casos

Cada punto de decisión deja tres o cuatro peores casos. Al resolver doce puntos
salieron treinta y cuatro. Se numeran P1 a P34 y se guardan en una sola tabla
con tres columnas: qué provoca, en qué escena ocurre, cómo lo ataja el diseño.

El código sirve para dos cosas: poner `P5` sobre la caja que lo resuelve, y
responder en la sustentación sin buscar.

Archivo: `Lab4/Diagrams/00-contexto-diagrama.md`

---

## Paso 3. Escribir el guion antes de dibujar

Este paso es el que faltaba y lo cambió todo.

Un diagrama que nace de cajas técnicas queda como cajas técnicas. Un diagrama
que nace de un guion se lee como una historia.

### Prompt

```
Antes de dibujar nada, escribe el guion del recorrido.

Reglas:
- Empieza por una persona, no por un componente. Una arquitectura arranca
  cuando alguien hace algo.
- Una escena por paso. Cada escena en dos o tres oraciones, en lenguaje
  corriente, no de infraestructura.
- Termina en la persona que recibe el beneficio.
- Numera las escenas corrido.

Después de escribir el guion, dime qué escena corresponde a cada caja del
diagrama.
```

Del guion de PD-1 salieron ocho escenas, de Valeria a Rosa. El diagrama se
dibujó desde ahí, no al revés.

---

## Paso 4. Fijar una referencia visual

Mostrar una imagen del estilo que se espera y pedir la estructura, no el
contenido.

Lo que se pidió: cajas simples con borde de color, flechas etiquetadas, sin
relleno de fondo, elipses para las bases de datos, zonas punteadas.

Lo que se descartó: rellenos de color en las cajas, porque hacen que el
diagrama se vea recargado.

---

## Paso 5. Cortar en iteraciones acumulativas

Un diagrama con treinta cajas no se puede sustentar. Tres diagramas de diez
cajas sí.

| Iteración | Qué muestra | Qué agrega |
| --- | --- | --- |
| #1 | El sistema como una sola caja | quién lo usa y qué promete |
| #2 | El nodo decide qué bajar | manifiesto, comparador, los cuatro casos |
| #3 | Se descarga, verifica y activa | plan, bloques, hash, puntero, caché |

Cada iteración conserva la anterior. Las flechas punteadas entre iteración 2 y
3 muestran que es la misma historia y no tres diagramas distintos.

El guion numerado va en la columna izquierda de cada iteración, así se lee de
arriba a abajo mientras se señalan las cajas.

---

## Paso 6. Generar el diagrama con código

El `.excalidraw` es un JSON. Escribirlo a mano da cajas descuadradas y textos
encimados.

Se genera con un script de Python que define funciones `box`, `dbox`, `arw`,
`txt`, y se llama con coordenadas explícitas. Ventajas:

- Mover una fila entera es cambiar un número.
- Se puede verificar antes de abrir el archivo: contar elementos, buscar
  solapamientos, comprobar que ninguna caja tiene relleno.
- Regenerar es instantáneo cuando cambia el guion.

En la generación de PD-1 esa verificación encontró que el guion de la
iteración 1 se cruzaba con la línea divisoria. Se corrigió antes de abrir
Excalidraw.

---

## Resumen del recorrido

```
1. Prompt de casos posibles  ->  tabla exhaustiva por punto de decisión
2. Consolidar                ->  catálogo P1..P34 con códigos
3. Escribir el guion         ->  escenas numeradas, de persona a persona
4. Fijar referencia visual   ->  qué estilo, qué se descarta
5. Cortar en iteraciones     ->  tres capas acumulativas
6. Generar con código        ->  JSON verificable, no cajas a mano
```

El orden importa. Los pasos 1 y 2 dan el rigor; el 3 da la narrativa; los
pasos 4 a 6 dan la ejecución. Saltarse el paso 3 es lo que produce diagramas
que nadie sabe explicar.
