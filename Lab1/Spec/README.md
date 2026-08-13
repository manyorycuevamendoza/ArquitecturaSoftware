# Spec — Prompts de evaluación

## 1. Prompt por agente-persona

```text
Eres el agente definido en Agents/Agent-<NOMBRE>.md.
Contexto: Problema.md, Usuarios.md, Personas/<NOMBRE>.md.
Evalúa Requirements/ReqFunc.md y Requirements/ReqNoFunc.md desde la óptica de tu persona.
Para cada requerimiento indica: Satisface / Parcial / No satisface / No aplica, con justificación breve.
Luego lista los gaps (necesidades de tu persona no cubiertas) y los requerimientos ambiguos.
Termina con "Puntaje de cobertura: NN%".
Devuelve solo la tabla y las secciones pedidas, en Markdown.
```

## 2. Prompt del evaluador global

```text
Eres el agente definido en Spec/Eval-Spec.md.
Entradas: Problema.md, Usuarios.md, todas las Personas/, Requirements/ReqFunc.md,
Requirements/ReqNoFunc.md y las evaluaciones de los 5 agentes-persona.
Aplica la rúbrica ponderada de Eval-Spec.md y devuelve el puntaje global en %,
el veredicto, los gaps críticos y las acciones recomendadas.
```

## 3. Registro de ejecución

| Fecha | Modelo/Cliente | Iteración | Puntaje global |
| --- | --- | --- | --- |
| _(pendiente)_ | | | |

Resultados completos en [Resultados.md](Resultados.md).
