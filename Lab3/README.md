# Caso de Estudio #3 - SendIt

Arquitectura de Software - UTEC - 2026-II

## Que es una remesa

Una remesa es el dinero que una persona envia a otra persona, normalmente a un familiar, que vive en otro pais. En SendIt, el remitente inicia el envio, el sistema valida su identidad y disponibilidad de fondos, convierte la moneda si corresponde y coordina la entrega al beneficiario. El dinero no debe aparecer como enviado hasta que la operacion quede confirmada de forma consistente.

## Entregables

| Entregable | Archivo |
| --- | --- |
| Problema, alcance y supuestos | [Problema.md](Problema.md) |
| Usuario modelo y actores | [Usuarios.md](Usuarios.md) |
| Personas | [Personas/](Personas/) |
| Requerimientos funcionales | [Requirements/Functional.md](Requirements/Functional.md) |
| Requerimientos no funcionales | [Requirements/NonFunctional.md](Requirements/NonFunctional.md) |
| SPEC template | [SPEC-TEMPLATE.md](SPEC-TEMPLATE.md) |
| Resultado de EVAL | [Spec/Results.md](Spec/Results.md) |
| R.E.D.A.L.E. e iteraciones | [Architecture.md](Architecture.md) |
| Diagramas por iteracion | [Architecture.md](Architecture.md#iteraciones-de-diseño-de-menos-a-más) |
| Diagrama Top Down Design (entregable principal) | [Diagrams/06-topdown-sendit.excalidraw](Diagrams/06-topdown-sendit.excalidraw) |
| Diagrama consolidado R.E.D.A.L.E. | [Diagrams/05-redale-completo.excalidraw](Diagrams/05-redale-completo.excalidraw) |

## Como se conecta el trabajo

El contexto no se concatena directamente dentro de una caja de arquitectura. Se transforma paso a paso:

```text
Problema y alcance
	↓
Personas y pain points
	↓
Requerimientos funcionales y no funcionales
	↓
R.E.D.A.L.E.: requerimientos → estimaciones → servicios → datos → componentes → escala
	↓
Diagramas Excalidraw y decisión final
```

Usa `06-topdown-sendit.excalidraw` para exponer: es un solo lienzo con el formato del profesor, donde los requerimientos nacen de Ana, Luis, Marta y Cumplimiento, y las tres iteraciones crecen de forma acumulativa. Usa `05-redale-completo.excalidraw` si necesitas el recorrido por letras de R.E.D.A.L.E.

## Usuario modelo

El usuario modelo es el **remitente**, porque inicia el caso de uso principal y necesita saber con claridad cuanto paga, cuanto recibe el beneficiario y en que estado se encuentra la remesa. El beneficiario recibe el dinero, pero no opera el flujo principal.

## Como abrir el diagrama

En Excalidraw, usa **Open** y selecciona `Diagrams/06-topdown-sendit.excalidraw`. El archivo es editable y contiene los requerimientos por persona, las tres iteraciones acumulativas y la leyenda de colores.

## Lectura recomendada

1. [Problema](Problema.md)
2. [Personas](Personas/)
3. [Requerimientos](Requirements/)
4. [Evaluacion](Spec/Results.md)
5. [R.E.D.A.L.E.](Architecture.md)