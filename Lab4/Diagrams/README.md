# Diagramas — RemoteSchooly

## Enlaces de Excalidraw

Se abren en el navegador, sin descargar nada.

### Problema 1: distribución con Internet intermitente

**https://excalidraw.com/#json=6NmtnSrpFmLvUKguJUbAN,mlAwlfJVLCijv9M1_9Sbkg**

Ocho puntos de decisión (PD-1 a PD-8), 36 casos, 24 peores casos. El recorrido
completo de Valeria a Valeria: publicación, ventana de sincronización, qué
archivos bajar, verificación, activación atómica, la clase sin red y el retorno
idempotente.

### Problema 2: el gasto excesivo de tokens

**https://excalidraw.com/#json=BmDh4K8AmVviYehGmCnEO,49CS3hPCLYUat6AmqW3C1g**

Cuatro puntos de decisión (PD-9 a PD-12), 18 casos, 10 peores casos. Ocho
escenas donde cada paso descarta una razón para llamar al modelo: se pregunta,
se acota el contexto, se busca en la caché y se presupuesta. La llamada es lo
último que queda.

---

## Qué hay dentro

Todo lo demás vive en [Contexto/](Contexto/): los lienzos y el análisis del que
salieron.

```
Diagrams/
├── README.md          este archivo, con los enlaces de arriba
└── Contexto/
    ├── Problema1/     los cinco lienzos de la distribución
    ├── Problema2/     el lienzo de la gobernanza de tokens
    ├── 00-contexto-diagrama.md
    ├── 01-decision-ai-gateway.md
    └── los tres lienzos previos
```

| Ruta | Qué contiene |
| --- | --- |
| [Contexto/Problema1/](Contexto/Problema1/README.md) | Cinco lienzos: cuatro por bloque y uno con el recorrido completo. Los 36 casos de la distribución. |
| [Contexto/Problema2/](Contexto/Problema2/README.md) | Un lienzo con las ocho escenas de la gobernanza de tokens y el cruce completo del Gateway. |
| [Contexto/00-contexto-diagrama.md](Contexto/00-contexto-diagrama.md) | Documento vivo. Los 12 puntos de decisión con su cruce exhaustivo, el catálogo de 34 peores casos y las frases para el diagrama. Los lienzos se dibujan **desde** aquí, no al revés. |
| [Contexto/01-decision-ai-gateway.md](Contexto/01-decision-ai-gateway.md) | El cruce completo del AI Gateway: 16 filas y los 9 casos que sobreviven. |
| [Contexto/02-topdown-remoteschooly-v2.excalidraw](Contexto/02-topdown-remoteschooly-v2.excalidraw) | Top Down Design con tres iteraciones acumulativas. Sirve para sustentar por qué está diseñado así. |
| [Contexto/01-topdown-remoteschooly.excalidraw](Contexto/01-topdown-remoteschooly.excalidraw) | Primera versión del Top Down, resumida. Se conserva como registro. |
| [Contexto/03-arquitectura-remoteschooly.excalidraw](Contexto/03-arquitectura-remoteschooly.excalidraw) | Arquitectura por zonas con sus bases de datos y los peores casos sobre el componente que los ataja. |

---

## Cómo leer un lienzo

Todos siguen la misma estructura:

- **Columna izquierda:** el guion numerado. Se lee de arriba a abajo mientras se
  señalan las cajas de la derecha.
- **Tres iteraciones acumulativas** en los lienzos del problema 1: la primera
  plantea la pregunta, la segunda abre el cruce de casos, la tercera agrega la
  capa que faltaba. Ninguna reemplaza a la anterior.
- **Leyenda al pie:** los peores casos que ese lienzo ataja, con su código `P1`
  a `P34` del catálogo consolidado.

### Convención visual

- Fondo transparente en todas las figuras. El color vive en el borde.
- Azul: personas. Rojo: servicios que mueven datos. Morado: componentes que
  deciden. Cyan y elipse: bases de datos y almacenes.
- Verde: el resultado bueno. Naranja: degradado pero recuperable. Rojo: rechazo
  o fallo.
- Borde punteado: una zona, o un caso imposible.
- Monoespaciada: identificadores, tablas de cruce y órdenes de operación.

La paleta y las figuras compuestas están en
[Contexto/Problema1/generadores/\_lib.py](Contexto/Problema1/generadores/_lib.py). Cambiar un color
ahí lo cambia en los seis lienzos a la vez.

---

## Regenerar

Los lienzos se generan con código, no se dibujan a mano: así se verifican antes
de abrirlos.

```bash
cd Contexto/Problema1/generadores && for d in B C D E; do python3 gen_$d.py; done
```

```bash
cd Contexto/Problema2/generadores && python3 gen_problema2.py && python3 check.py
```

Si se regenera un lienzo, hay que volver a subirlo a Excalidraw para que el
enlace de arriba muestre la versión nueva.
