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
1. Se agregó handoff estructurado y versionado en `RF-DIA-01/02`.
2. Se especificó la alerta crítica, acuse y escalamiento medible en `RF-EME-01/02`, `RF-NOT-01/02` y `RNF-OBS-01`.
3. Se agregaron modo degradado, control de acceso, reportes regionales, comunicación al familiar y métricas de escala verificables.

## Iteración 2

### Evaluaciones por persona

| Persona | Puntaje de cobertura | Evidencia y gap residual |
| --- | --- | --- |
| Pablo | 94% | El handoff completo/versionado (`RF-DIA-01/02`), alertas focalizadas (`RF-NOT-01`) y tiempos de consulta (`RNF-PER-01/03`) cubren su inicio de turno. Resta definir una taxonomía clínica detallada de «cambio crítico». |
| Claudia | 95% | Alerta en dos acciones y ≤ 30 s (`RF-EME-01`, `RNF-USA-02`), confirmación/escalamiento a 90 s (`RF-EME-02`) y modo degradado (`RF-CON-01`) cubren su escenario nocturno. |
| Roberto | 92% | Plantillas por lote (`RF-ADM-01`), acceso administrado (`RF-ACC-01`), tablero (`RF-REP-01`, `RNF-OBS-02`) y perfiles de capacidad (`RNF-ESC-01/02/03`) son verificables. Resta definir la política de resolución de conflictos de sincronización. |
| Elena | 94% | Auditoría de acciones y accesos (`RF-AUD-01`), indicadores comparables (`RF-REP-01`) y simulacros de RTO (`RNF-DIS-02`) entregan evidencia para gestión y cumplimiento. |
| Manuel | 91% | Continuidad clínica (`RF-DIA-01/02`), escalamiento (`RF-EME-02`), control de acceso (`RF-ACC-01`, `RNF-SEG-01`) y resumen autorizado (`RF-FAM-01`) cubren sus necesidades. Resta acordar periodicidad y contenido del reporte familiar. |

### Resultado Eval-Spec

| Dimensión | Puntaje | Peso | Ponderado |
| --- | --- | --- | --- |
| Cobertura de personas | 93% | 30% | 27.90% |
| Cobertura de problemáticas críticas | 93% | 25% | 23.25% |
| Verificabilidad | 96% | 15% | 14.40% |
| Trazabilidad | 94% | 10% | 9.40% |
| Metas de rendimiento y escalamiento | 91% | 15% | 13.65% |
| No ambigüedad y no duplicación | 90% | 5% | 4.50% |

**Puntaje global: 93.1%**
**Veredicto:** Requerimientos listos para diseño arquitectónico.

### Justificación del resultado Eval-Spec

- **Cobertura de personas (93%):** las cinco personas tienen objetivos críticos cubiertos: continuidad y alertas focalizadas para Pablo (`RF-DIA-01/02`, `RF-NOT-01`); operación y escalamiento para Claudia (`RF-EME-01/02`, `RF-CON-01`); administración y observabilidad para Roberto (`RF-ADM-01`, `RF-REP-01`, `RNF-OBS-02`); evidencia para Elena (`RF-AUD-01`, `RF-REP-01`); y continuidad, privacidad e información autorizada para Manuel (`RF-ACC-01`, `RF-FAM-01`).
- **Problemáticas críticas (93%):** la rotación tiene contenido obligatorio e historial (`RF-DIA-01/02`); el problema de medianoche establece dos acciones, entrega, acuse y escalamiento a los 90 s (`RF-EME-01/02`); las actualizaciones se dirigen a destinatarios pertinentes y su entrega se mide en `RNF-OBS-01`. `RF-CON-01` cubre la caída de conectividad.
- **Verificabilidad (96%):** cada RF nuevo indica una condición comprobable y los RNF definen percentil, umbral, alcance o frecuencia de prueba. Los únicos aspectos pendientes son acordar el catálogo de cambios clínicos críticos y la política de conflicto offline.
- **Trazabilidad (94%):** `RF-AUD-01` registra actor, acción, objeto, fecha/hora, sede y resultado; la matriz de `ReqFunc.md` vincula problemáticas con RF; `RF-REP-01` convierte los registros en indicadores por sede, servicio y turno.
- **Metas de rendimiento y escalamiento (91%):** `RNF-PER-01/02/03`, `RNF-DIS-01/02/03`, `RNF-OBS-01` y `RNF-ESC-01/02/03` indican umbrales y perfil de carga. Falta validar estos volúmenes con datos reales del piloto antes de comprometer la capacidad nacional.
- **No ambigüedad y no duplicación (90%):** se sustituyeron expresiones vagas por condiciones medibles, incluidos RPO = 0 (`RNF-DIS-03`) y escalamiento a 90 s (`RF-EME-02`). Persisten dos decisiones de negocio por concretar: catálogo de eventos críticos y periodicidad del resumen familiar.

### Gaps críticos

1. Acordar y versionar el catálogo clínico de eventos que se clasifican como críticos en `RF-NOT-01`.
2. Definir la política de resolución y revisión clínica de conflictos si dos registros offline modifican el mismo dato.
3. Acordar la periodicidad, responsable y contenido mínimo del resumen para el familiar de `RF-FAM-01`.

### Acciones recomendadas

1. Validar los criterios de aceptación con personal clínico, TI regional y representantes de familiares antes de diseñar.
2. Ejecutar pruebas de carga y simulacros de caída que evidencien los RNF definidos.
3. Incorporar las tres decisiones pendientes como reglas de negocio versionadas durante el diseño detallado.

## Iteración 3

### Evaluaciones por persona

| Persona | Puntaje de cobertura | Evidencia y gap residual |
| --- | --- | --- |
| Pablo | 94% | El rol Médico internista es responsable de continuidad, notificaciones y rendimiento en `RF-DIA-01/02`, `RF-NOT-01` y `RNF-PER-01/03`. Falta un catálogo clínico versionado de «cambio crítico». |
| Claudia | 95% | El rol Enfermera de UCI es responsable de la alerta, el aviso a otro responsable y el funcionamiento sin conexión en `RF-EME-01/02`, `RF-CON-01` y `RNF-USA-02`. Falta resolver formalmente conflictos de registros sin conexión. |
| Roberto | 94% | El rol Administrador de red regional concentra turnos, plantillas, acceso, disponibilidad, seguridad, monitoreo y escala en `RF-TUR-01`, `RF-ADM-01`, `RF-ACC-01` y los RNF asociados. |
| Elena | 93% | El rol Jefatura de gestión clínica es responsable de auditoría y reportes en `RF-AUD-01` y `RF-REP-01`, con indicadores comparables y exportables. |
| Manuel | 91% | `RF-DIA-01/02`, `RF-EME-02`, `RF-ACC-01`, `RNF-SEG-01` y `RF-FAM-01` cubren continuidad, respuesta, privacidad e información autorizada. Falta acordar la periodicidad del resumen familiar. |

### Resultado Eval-Spec

| Dimensión | Puntaje | Peso | Ponderado |
| --- | --- | --- | --- |
| Cobertura de personas | 94% | 30% | 28.20% |
| Cobertura de problemáticas críticas | 93% | 25% | 23.25% |
| Verificabilidad | 96% | 15% | 14.40% |
| Trazabilidad | 92% | 10% | 9.20% |
| Metas de rendimiento y escalamiento | 91% | 15% | 13.65% |
| No ambigüedad y no duplicación | 92% | 5% | 4.60% |

**Puntaje global: 93.3%**
**Veredicto:** Requerimientos listos para diseño arquitectónico.

### Justificación del resultado Eval-Spec

- **Cobertura de personas (94%):** los requisitos asignan la responsabilidad funcional al rol que opera o administra la capacidad: Administrador de red regional (`RF-TUR-01`, `RF-ADM-01`, `RF-ACC-01`), Médico internista (`RF-DIA-01/02`, `RF-NOT-01`), Enfermera de UCI (`RF-EME-01/02`, `RF-CON-01`), Jefatura de gestión clínica (`RF-AUD-01`, `RF-REP-01`) y familiar autorizado mediante `RF-FAM-01`.
- **Problemáticas críticas (93%):** la rotación está cubierta por el handoff obligatorio y versionado (`RF-DIA-01/02`); el problema de medianoche por alerta en dos acciones y aviso a otro responsable a los 90 s (`RF-EME-01/02`); y las actualizaciones oportunas por destinatarios autorizados y entrega < 2 s (`RF-NOT-01`, `RNF-OBS-01`).
- **Verificabilidad (96%):** los RF incluyen criterios de aceptación y los RNF establecen percentiles, umbrales, frecuencia y perfiles de carga, por ejemplo `RNF-DIS-01/02/03`, `RNF-ESC-01/02/03` y `RNF-USA-01/02`.
- **Trazabilidad (92%):** cada requisito vigente tiene un único rol responsable y la matriz de `ReqFunc.md` lo conecta con una problemática. `RF-AUD-01` y `RF-REP-01` entregan evidencia por sede, usuario y periodo. Falta una matriz explícita que conecte formalmente rol, persona modelo y objetivo de persona.
- **Metas de rendimiento y escalamiento (91%):** `RNF-PER-01/02/03`, `RNF-DIS-01/02/03`, `RNF-OBS-01` y `RNF-ESC-01/02/03` definen metas comprobables. Los perfiles nacionales aún deben validarse con datos reales del piloto.
- **No ambigüedad y no duplicación (92%):** la asignación de un rol responsable elimina la ambigüedad de propiedad; los tiempos de alerta, RPO y usabilidad tienen umbrales explícitos. Persisten reglas de negocio pendientes para eventos críticos, conflictos sin conexión y comunicación familiar.

### Gaps críticos

1. Definir y versionar el catálogo de eventos clínicos que activan una notificación crítica en `RF-NOT-01`.
2. Definir la política de resolución y revisión clínica de conflictos de sincronización para `RF-CON-01`.
3. Definir periodicidad, responsable y contenido mínimo del resumen compartido mediante `RF-FAM-01`.

### Acciones recomendadas

1. Crear una matriz rol–persona modelo–objetivo–requerimiento para completar la trazabilidad sin volver a asignar requisitos a personas individuales.
2. Validar los criterios de aceptación con usuarios de cada rol y ejecutar las pruebas de carga, caída y desconexión definidas.
3. Registrar los tres gaps como reglas de negocio antes del diseño detallado.

## Iteración 4

Corrige la lectura de la tabla de la iteración 3: cada requerimiento se atribuye ahora al **rol responsable** de ejecutarlo o administrarlo, y no a la persona modelo que se beneficia de él. Esto era especialmente confuso en el caso de Manuel, que es paciente/familiar y no opera el sistema. Los puntajes no cambian respecto de la iteración 3; solo cambia la forma de expresar la evidencia.

### Cómo leer la tabla

- **Persona / Tipo:** el usuario modelo evaluado y si opera el sistema o solo se beneficia de él.
- **Rol responsable de los requerimientos citados:** quién ejecuta o administra la capacidad. Es el único vínculo válido entre un `RF`/`RNF` y un actor: una persona solo se asocia a un requerimiento cuando es responsable de él. Una persona beneficiaria no tiene requerimientos asociados y su celda queda como «No aplica».
- **Necesidad de la persona que queda cubierta:** qué obtiene la persona modelo, descrito en términos de valor recibido y no de requerimientos que deba ejecutar.
- **Gap residual:** lo que aún debe definirse y es atribuible a esa persona por ser responsable; «ninguno» o «no aplica» significa que el pendiente pertenece a otro rol y se registra en Gaps críticos.

### Evaluaciones por persona

| Persona | Tipo | Rol responsable de los requerimientos citados | Necesidad de la persona que queda cubierta | Cobertura | Gap residual |
| --- | --- | --- | --- | --- | --- |
| Pablo | Usuario directo | Médico internista — `RF-DIA-01/02`, `RF-NOT-01`, `RNF-PER-01/03` | Recibe el handoff completo y versionado del turno anterior, y solo las notificaciones de sus pacientes, con consulta en ≤ 1 s | 94% | Falta un catálogo clínico versionado de «cambio crítico» para `RF-NOT-01` |
| Claudia | Usuario directo | Enfermera de UCI — `RF-EME-01`, `RF-CON-01`, `RNF-USA-02` | Crea la alerta crítica en ≤ 2 acciones, sabe que se escala automáticamente a los 90 s si nadie confirma y puede registrar a pie de cama sin conexión | 95% | Falta la política formal de resolución de conflictos de registros sin conexión (`RF-CON-01`) |
| Roberto | Usuario directo | Administrador de red regional — `RF-TUR-01`, `RF-ADM-01`, `RF-ACC-01`, `RNF-DIS-01/02`, `RNF-SEG-01/02`, `RNF-OBS-02`, `RNF-ESC-01/02/03` | Configura sedes por lote, administra roles y accesos, y monitorea disponibilidad y escala desde un solo tablero | 94% | Ninguno propio; depende de validar los perfiles de carga nacionales con datos del piloto |
| Elena | Cliente / stakeholder | Jefatura de gestión clínica — `RF-AUD-01`, `RF-REP-01` | Dispone de auditoría inalterable e indicadores comparables y exportables por sede, servicio y turno | 93% | Ninguno propio; requiere acordar la periodicidad de reporte institucional |
| Manuel | Beneficiario (no opera el sistema) | No aplica — no es responsable de ningún requerimiento | Su información clínica pasa completa entre turnos, alguien responde siempre ante un deterioro nocturno, sus datos están protegidos y su familiar autorizado recibe un resumen del estado | 91% | No aplica — los pendientes que lo afectan pertenecen a los roles responsables y se listan en Gaps críticos |

### Resultado Eval-Spec

Sin cambios respecto de la iteración 3, dado que la corrección es de redacción y atribución, no de contenido de los requerimientos.

| Dimensión | Puntaje | Peso | Ponderado |
| --- | --- | --- | --- |
| Cobertura de personas | 94% | 30% | 28.20% |
| Cobertura de problemáticas críticas | 93% | 25% | 23.25% |
| Verificabilidad | 96% | 15% | 14.40% |
| Trazabilidad | 92% | 10% | 9.20% |
| Metas de rendimiento y escalamiento | 91% | 15% | 13.65% |
| No ambigüedad y no duplicación | 92% | 5% | 4.60% |

**Puntaje global: 93.3%**
**Veredicto:** Requerimientos listos para diseño arquitectónico.

### Gaps críticos

1. Definir y versionar el catálogo de eventos clínicos que activan una notificación crítica en `RF-NOT-01`.
2. Definir la política de resolución y revisión clínica de conflictos de sincronización para `RF-CON-01`.
3. Definir periodicidad, responsable y contenido mínimo del resumen compartido mediante `RF-FAM-01`.

### Acciones aplicadas en esta iteración

1. Se separó en la tabla el **rol responsable** de la **persona beneficiada**: una persona solo se asocia a un requerimiento cuando es responsable de ejecutarlo o administrarlo.
2. Se retiró toda referencia a `RF`/`RNF` en la fila de Manuel, que es paciente/familiar y no opera el sistema; su cobertura se describe por el valor que recibe.
3. Se explicitó el tipo de cada persona (usuario directo, cliente/stakeholder, beneficiario) y se añadió una guía de lectura de la tabla.
