# Resultados de la Evaluación

## Iteración 1

### Evaluaciones por persona

| Persona | Puntaje de cobertura | Gaps principales |
| --- | --- | --- |
| Pablo | 62% | `RF-DIA-01` solo cubre el diagnóstico, no un handoff estructurado con decisiones, medicación y pendientes; `RF-NOT-01` no filtra alertas por paciente o turno. |
| Claudia | 51% | `RF-EME-01` no define plazo, acuse de recibo ni destinatarios alternos; faltan flujo de dos toques y registro/sincronización ante red inestable. |
| Roberto | 45% | `RF-ADM-01` no define alta masiva ni administración central de reglas; faltan modo degradado, métricas operativas por sede y criterios de capacidad para `RNF-ESC-01/02/03`. |
| Elena | 51% | `RF-AUD-01` no contempla accesos, tableros ni reportes comparables; faltan indicadores de handoff, escalamiento, disponibilidad y RTO por sede. |
| Manuel | 53% | El handoff de `RF-DIA-01` no incluye antecedentes, alergias, decisiones ni pendientes; falta comunicación consistente al familiar y control de acceso explícito. |

### Resultado Eval-Spec

| Dimensión | Puntaje | Peso | Ponderado |
| --- | --- | --- | --- |
| Cobertura de personas | 52% | 30% | 15.60% |
| Cobertura de problemáticas críticas | 53% | 25% | 13.25% |
| Verificabilidad | 55% | 15% | 8.25% |
| Trazabilidad | 65% | 10% | 6.50% |
| Metas de rendimiento y escalamiento | 75% | 15% | 11.25% |
| No ambigüedad y no duplicación | 40% | 5% | 2.00% |

**Puntaje global: 57%**
**Veredicto:** No satisface a las personas definidas; requiere otra iteración antes del diseño arquitectónico.

### Justificación del resultado Eval-Spec

- **Cobertura de personas (52%):** los seis RF atienden parcialmente el núcleo clínico (`RF-TUR-01`, `RF-DIA-01`, `RF-EME-01`, `RF-NOT-01`, `RF-ADM-01` y `RF-AUD-01`), pero no cubren objetivos esenciales de las cinco personas. Faltan el handoff completo y focalización de alertas para Pablo, la confirmación y operación sin red para Claudia, la administración/observabilidad regional para Roberto, los indicadores para Elena y la comunicación a Rosa.
- **Problemáticas críticas (53%):** la rotación queda cubierta solo para el diagnóstico con `RF-DIA-01`, no para información clínica completa; el problema de medianoche cuenta con escalamiento en `RF-EME-01`, pero sin tiempo máximo, acuse ni regla de alternos; las actualizaciones en tiempo real dependen de `RF-NOT-01` y `RNF-OBS-01`, sin garantía de destinatario pertinente, entrega confirmada o sincronización tras desconexión.
- **Verificabilidad (55%):** las metas de `RNF-PER-01/02`, `RNF-DIS-01/02`, `RNF-OBS-01` y `RNF-USA-01` son medibles. En contraste, los RF no tienen criterios de aceptación: «inmediata» (`RF-DIA-01`), «rápido» (`RF-EME-01`) y «tiempo real» (`RF-NOT-01`) no definen umbrales. `RNF-DIS-03` usa «cercano a 0» y los RNF de escala solo indican cantidad de hospitales, sin carga de referencia.
- **Trazabilidad (65%):** los RF identifican una persona principal y los módulos se relacionan con el problema, pero no existe una matriz explícita requerimiento–persona–objetivo–problemática. En particular, Manuel no figura como persona asociada a ningún RF y los objetivos institucionales de Elena no se trazan a métricas/reportes.
- **Rendimiento y escalamiento (75%):** están declaradas las metas de inicio (`RNF-PER-01`), configuración (`RNF-PER-02`), disponibilidad (`RNF-DIS-01`), recuperación (`RNF-DIS-02`) y crecimiento (`RNF-ESC-01/02/03`). Falta precisar el alcance de medición, usuarios/carga concurrente, datos por hospital y condiciones de prueba; por ello no demuestran capacidad real de 1K a 10M de hospitales.
- **No ambigüedad y no duplicación (40%):** no hay duplicaciones importantes, pero sí ambigüedades que afectan la seguridad: «disponible de forma inmediata» (`RF-DIA-01`), «contacto rápido» (`RF-EME-01`), «cambios críticos» (`RF-NOT-01`), «centralizado» (`RF-ADM-01`) y RPO «cercano a 0» (`RNF-DIS-03`).

### Gaps críticos

1. Definir un handoff estructurado obligatorio que incluya diagnóstico vigente, antecedentes, alergias, decisiones, medicación, resultados y pendientes; debe tener autor, hora y criterio de cierre por turno.
2. Especificar el flujo de emergencia: alerta en menos de 30 s, acuse visible, confirmación de lectura/respuesta, escalamiento automático a alternos a los 90 s y trazabilidad de cada intento.
3. Incorporar operación tolerante a conectividad intermitente: registro local a pie de cama, estado de sincronización, resolución de conflictos y sincronización segura al restablecer la red.
4. Incorporar control de acceso basado en roles y relación clínica, con auditoría de accesos, y definir qué información y canal recibe el familiar autorizado.
5. Definir administración masiva y reglas regionales, tableros y reportes por sede; completar las metas de escala con perfiles de carga, concurrencia y datos verificables.

### Acciones aplicadas tras la iteración
1. Se ejecutó la primera evaluación consolidada a partir de `Eval-Spec.md`, las cinco personas y los requerimientos vigentes; no se modificaron requerimientos en esta iteración.
2. Para la siguiente iteración, convertir los cinco gaps críticos en RF/RNF con IDs y criterios de aceptación medibles.
3. Añadir una matriz de trazabilidad que relacione cada requerimiento con la problemática, las personas, sus objetivos y una prueba de aceptación.
