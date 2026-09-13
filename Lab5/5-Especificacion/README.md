# Especificación y evaluación

Carpeta para que un agente de IA evalúe los requerimientos del Lab 5 contra las
personas y el diagrama, como se hizo en [../../Lab1/Spec/](../../Lab1/Spec/).

| Archivo | Qué es |
| --- | --- |
| [Eval-Spec.md](Eval-Spec.md) | Definición del agente evaluador: entradas, evaluación por persona, rúbrica global y formato de salida. |
| [Results.md](Results.md) | Salida de cada ejecución del agente, una sección por iteración. |

## Cómo ejecutarlo

Abrir un agente (Claude Code, Codex o similar) en la raíz del repositorio y darle
este prompt:

```text
Actúa como el agente definido en Lab5/5-Especificacion/Eval-Spec.md.
Lee todas sus entradas (problema, personas, requerimientos funcionales y no
funcionales, y el diagrama Lab5/Diagrams/diagramaLab5.excalidraw).
Ejecuta el Paso 1 para las cinco personas y el Paso 2 con la rúbrica.
Antes de puntuar, verifica mecánicamente: (a) que todo ID citado en personas y
requerimientos exista, (b) que cada requisito sea reclamado por al menos una
persona, (c) que cada componente que un requisito nombra esté en el diagrama.
Escribe el resultado como una nueva iteración al final de
Lab5/5-Especificacion/Results.md siguiendo el formato de salida.
No modifiques los requerimientos: solo evalúa.
```

## Ciclo

1. Ejecutar el agente → nueva iteración en `Results.md`.
2. Corregir los gaps en `3-Requerimientos/` o en el diagrama.
3. Volver a ejecutar hasta alcanzar ≥ 90% o justificar los gaps que se conservan.
