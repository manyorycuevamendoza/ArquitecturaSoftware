# Problema 2: el gasto excesivo de tokens

Un solo lienzo: `problema2.excalidraw`. Cubre los cuatro puntos de decisión de la
gobernanza de tokens (PD-9 a PD-12) y sus 18 casos.

El detalle de cada cruce está en [../Contexto/00-contexto-diagrama.md](../Contexto/00-contexto-diagrama.md);
el cruce completo del AI Gateway —las 16 filas y los 9 casos que sobreviven— en
[../Contexto/01-decision-ai-gateway.md](../Contexto/01-decision-ai-gateway.md). El lienzo se dibuja
**desde** esos dos archivos, no al revés.

## El recorrido

Ocho escenas, de izquierda a derecha, escalonadas: el hilo marrón las une y va
descendiendo hasta cerrar abajo a la derecha, igual que en el Problema 1.

| # | Escena | Punto de decisión | Casos |
| --- | --- | --- | ---: |
| 1 | La docente entra | login e identidad | — |
| 2 | ¿Se puede armar el prompt? | PD-9 | 5 |
| 3 | ¿Qué entra al prompt? | PD-11 | 4 |
| 4 | ¿Ya existe esta respuesta? | PD-10 | 5 |
| 5 | ¿Cabe en el presupuesto? | PD-12 | 4 |
| 6 | La llamada | — | — |
| 7 | Sin red, la solicitud espera | — | — |
| 8 | ¿Se logró el 40%? | medición | — |
| | | **TOTAL** | **18** |

Abajo a la izquierda, el bloque **El cruce completo del Gateway** vuelve a contar
la misma decisión de una sola vez: el producto cartesiano `2 × 2 × 2 × 2 = 16`
filas, el colapso justificado de las ocho primeras y los **9 casos** que
sobreviven.

## Por qué ese orden de escenas

No es el orden de numeración de los puntos de decisión, es el orden del gasto.
Cada escena descarta una razón para llamar al modelo, y la llamada —la escena
6— es la última que queda:

1. **Se pregunta antes de gastar** (PD-9): si falta un campo o no hay cuota, no
   hay nada que enviar. Cuesta 0 tokens externos.
2. **Se acota el contexto** (PD-11): el archivo intermedio es la frontera de
   costo. Aquí se gana el 55% del ahorro, mandando dos fragmentos etiquetados en
   vez del temario completo.
3. **Se busca en la caché** (PD-10) **antes** que en el presupuesto: un resultado
   que ya existe es gratis, y cobrárselo a una docente sin cuota la dejaría sin
   algo que no cuesta nada.
4. **Se presupuesta** (PD-12): entrada y salida, las dos. Bloquear cuesta cero.

PD-11 va antes que PD-10 en el lienzo aunque su número sea mayor: sin el prompt
canónico armado no hay huella que buscar.

## Cómo leerlo

- El **título suelto** de cada escena marca dónde empieza; el tamaño crece con el
  peso de la escena, y `LA LLAMADA` es el más grande porque es el único paso que
  cuesta dinero.
- Debajo de cada escena va su **cruce de casos** completo, en fichas de color, y
  el **guion numerado** del 1 al 13, que se lee mientras se señalan las cajas.
  El guion apunta una idea por punto: lo que no cabe en dos líneas vive en
  `Contexto/00-contexto-diagrama.md`, no en el lienzo.
- En rojo, junto al componente que los ataja, los peores casos `P25` a `P34` del
  catálogo consolidado.
- El **hilo marrón** entre escenas nunca es recto: es el mismo recurso del
  Problema 1 para que el recorrido se lea como una historia y no como una
  rejilla.

## Convención visual

La misma del Problema 1, definida en
[../Problema1/generadores/_lib.py](../Problema1/generadores/_lib.py).

- Fondo transparente en todas las figuras. El color vive en el borde.
- Azul: personas. Rojo: servicios que mueven datos. Morado: componentes que
  deciden. Cyan y elipse: bases de datos y almacenes.
- Verde: el resultado bueno. Naranja: degradado pero recuperable. Rojo: rechazo
  o fallo.
- Borde punteado: una zona, o un caso imposible.
- Monoespaciada: identificadores, tablas de cruce y órdenes de operación.
- Sin marcos de zona alrededor de las escenas: el lienzo se ordena por
  proximidad y por el hilo, como el del Problema 1.

## Regenerar

El lienzo se genera con código, no se dibuja a mano: así se puede verificar antes
de abrirlo.

```bash
cd generadores
python gen_problema2.py     # escribe ../problema2.excalidraw
python check.py             # solapes de cajas y textos fuera de su recuadro
python preview.py           # PNG aproximado para revisar la composición
```

`gen_problema2.py` importa la paleta y las figuras compuestas de
`../../Problema1/generadores/_lib.py`. Cambiar un color ahí lo cambia en los seis
lienzos a la vez.
