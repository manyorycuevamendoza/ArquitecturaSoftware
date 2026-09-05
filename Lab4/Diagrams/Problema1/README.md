# Problema 1: distribución con Internet intermitente

Cinco lienzos. Cuatro cubren un bloque cada uno, el quinto los junta.

Los 36 casos salen de aplicar el método de casos posibles
([../../../Prompts/casos-posibles.md](../../../Prompts/casos-posibles.md)) a los
ocho puntos de decisión. El detalle de cada cruce está en
[../00-contexto-diagrama.md](../00-contexto-diagrama.md).

## Los lienzos

| Archivo | Bloque | Puntos de decisión | Casos |
| --- | --- | --- | ---: |
| `A-que-bajar.excalidraw` | ¿Qué archivos transferir? | PD-1 | 4 |
| `B-integridad-y-activacion.excalidraw` | ¿Puedo confiar en lo que llegó? | PD-2 + PD-5 | 11 |
| `C-retorno-idempotente.excalidraw` | Lo hecho sin red vuelve una sola vez | PD-3 + PD-6 | 7 |
| `D-cuando-sincronizar.excalidraw` | ¿Conviene sincronizar ahora? | PD-7 + PD-4 + PD-8 | 14 |
| `E-problema1-completo.excalidraw` | El recorrido completo | los ocho | 36 |

## Cómo se agruparon

La agrupación no es por orden de numeración, es por lo que cada par de
decisiones comparte.

**B junta PD-2 y PD-5** porque las dos protegen lo mismo: la versión que Rosa
está usando en ese momento. Una verifica que lo que llegó sea confiable, la otra
que el cambio de versión no deje un estado a medias.

**C junta PD-3 y PD-6** porque las dos sostienen el `event_id`. Una define qué
hace Lima cuando lo reconoce, la otra por qué ese identificador no puede
depender del reloj del nodo.

**D junta PD-7, PD-4 y PD-8** porque son las tres preguntas que se responden
antes de abrir la transferencia: si conviene ahora, cuánto hay que traer y si
cabe en el disco.

## Cómo leerlos

Cada lienzo tiene la misma estructura:

- **Columna izquierda:** el guion numerado. Se lee de arriba a abajo mientras se
  señalan las cajas de la derecha.
- **Tres iteraciones acumulativas:** la primera plantea la pregunta, la segunda
  abre el cruce de casos, la tercera agrega la capa que faltaba. Ninguna
  reemplaza a la anterior.
- **Leyenda al pie:** los peores casos que ese diagrama ataja, con su código
  `P1` a `P24` del catálogo consolidado.

El guion está numerado corrido dentro de cada lienzo. En `E` la numeración va
del 1 al 10 y cubre el recorrido entero.

## Convención visual

- Fondo transparente en todas las figuras. El color vive en el borde.
- Azul: personas. Rojo: servicios que mueven datos. Morado: componentes que
  deciden. Cyan y elipse: bases de datos y almacenes.
- Verde: el resultado bueno. Naranja: degradado pero recuperable. Rojo: rechazo
  o fallo.
- Borde punteado: una zona, o un caso imposible.
- Monoespaciada: identificadores, tablas de cruce y órdenes de operación.

## Regenerar

Los lienzos se generan con código, no se dibujan a mano. El JSON de Excalidraw
sale de un script, así se puede verificar antes de abrirlo: contar elementos,
buscar cajas superpuestas y comprobar que ningún texto se sale de su recuadro.

```bash
cd generadores && for d in B C D E; do python3 gen_$d.py; done
```

`_lib.py` define la paleta y las figuras compuestas. Cambiar un color ahí lo
cambia en los cinco lienzos a la vez.
