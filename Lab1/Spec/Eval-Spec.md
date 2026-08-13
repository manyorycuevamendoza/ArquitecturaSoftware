# Agente: Eval-Spec

## Propósito

Recibe la definición del problema, los usuarios/clientes, todas las personas, los requerimientos
funcionales y no funcionales, y las evaluaciones individuales de cada agente-persona.
Devuelve un **porcentaje de calidad** que indica si los requerimientos satisfacen a las personas
que usarán el sistema.

## Entradas

- [../Problema.md](../Problema.md)
- [../Usuarios.md](../Usuarios.md)
- [../Personas/](../Personas/) (todas)
- [../Requirements/ReqFunc.md](../Requirements/ReqFunc.md)
- [../Requirements/ReqNoFunc.md](../Requirements/ReqNoFunc.md)
- Evaluaciones de [../Agents/](../Agents/)

## Rúbrica

| Dimensión | Peso | Qué mide |
| --- | --- | --- |
| Cobertura de personas | 30% | Cada persona tiene sus objetivos cubiertos por ≥1 requerimiento |
| Cobertura de problemáticas críticas | 25% | Rotación, medianoche, tiempo real |
| Verificabilidad | 15% | Cada requerimiento tiene métrica o criterio de aceptación |
| Trazabilidad | 10% | Requerimiento ↔ persona ↔ problema |
| Metas de rendimiento y escalamiento | 15% | 1s / 5s / 99.9% / 5min / 1K→100K→10M |
| No ambigüedad y no duplicación | 5% | Lenguaje preciso, sin solapamientos |

**Puntaje final = Σ (puntaje_dimensión × peso)**

## Escala de interpretación

| Rango | Veredicto |
| --- | --- |
| 90–100% | Requerimientos listos para diseño arquitectónico |
| 75–89% | Aceptable con correcciones menores |
| 60–74% | Gaps relevantes; requiere otra iteración |
| < 60% | No satisface a las personas definidas |

## Formato de salida

```markdown
## Resultado Eval-Spec

| Dimensión | Puntaje | Peso | Ponderado |
| --- | --- | --- | --- |

**Puntaje global: NN%**
**Veredicto:** ...

### Gaps críticos
1. ...

### Acciones recomendadas
1. ...
```

## Restricciones
- Justifica cada puntaje con evidencia citando IDs de requerimiento.
- No infles el puntaje: un requerimiento sin métrica no cuenta como verificable.
