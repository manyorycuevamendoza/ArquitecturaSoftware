# Paola — Incident Manager

> Foco: aprobar lo que puede hacer daño, cumplir el SLA por clase y reconstruir qué pasó.

## Perfil

| Campo | Valor |
| --- | --- |
| Rol | Incident Manager del área de manejo de incidentes |
| Tipo | Usuario directo (operador): aprueba, no ejecuta |
| Responsabilidad | SLA de customer (1 día) y engineering (3 días); aprobación de acciones y de cambios al conocimiento |
| Nivel técnico | Medio-alto: entiende impacto, no ejecuta consultas |

## Contexto

Es la única persona que puede aprobar una acción que cambie o borre datos, y la
que responde cuando algo sale mal. El mes pasado no pudo reconstruir qué pasó el
día del borrado porque no había registro. En el pico de la primera semana
necesita ver de un vistazo qué clase de incidencias está sufriendo y decidir a
quién sacrificar antes de que el sistema lo decida por orden de llegada.

## Objetivos

1. Aprobar o rechazar cada acción destructiva viendo su impacto antes.
2. Cortar todas las acciones con un solo botón si algo huele mal.
3. Ver métricas por clase y recibir la alerta antes de que el usuario note la degradación.
4. Reconstruir cualquier acción desde la auditoría.
5. Aprobar qué conocimiento entra al LLM.

## Pain points

1. No puede reconstruir qué ocurrió el día del borrado.
2. Una consulta rutinaria de ingeniería retrasa una escalación de cliente con SLA de un día.
3. Corrigen lo mismo todas las semanas y nada queda aprendido.
4. Se entera de la saturación cuando los ingenieros ya se quejan.
5. Slack se cae y con él la única vía de aprobación.
6. No tiene forma de detener al LLM sin apagar todo Genius.

## Escenario clave

Paola recibe "hay una acción esperando tu aprobación": Camila pidió borrar la
INC-4530. **Aprobación de la acción** le muestra la vista previa (1 registro,
borrado lógico, reversible). Aprueba; **Borrado de incidencia** se ejecuta,
queda en **Auditoría** y la incidencia deja de aparecer como similar. Media hora
después ve en **Métricas y dashboard** que la cola de ingeniería está al 80% y
el cortacircuito del LLM semiabierto: el descarte por prioridad ya protege a
customer. Al final del día revisa el **Eval set** de un cambio de conocimiento
propuesto por Martín y lo aprueba en **Aprobación de cambios al conocimiento**.

## Criterios de éxito

- 100% de acciones destructivas con vista previa, aprobador distinto y registro.
- Cero customer escalations críticas descartadas en el pico.
- Alerta al 80% de cualquier umbral, antes de la queja.
- El incidente del borrado se reconstruye solo con la auditoría.

## Requisitos que la cubren

`FR-ACT-01`, `FR-ACT-02`, `FR-ACT-04`, `FR-ACT-06`, `FR-ACT-09`, `FR-ACT-12`,
`FR-ANS-12`, `FR-REL-01`, `FR-REL-02`, `FR-REL-06`, `FR-REL-08`, `FR-REL-10`,
`FR-REL-11`, `FR-REL-12`, `NFR-AVL-02`, `NFR-AVL-03`, `NFR-PER-02`,
`NFR-CAP-02`, `NFR-CAP-03`, `NFR-SEC-02`, `NFR-SEC-03`, `NFR-REC-01`,
`NFR-REC-02`, `NFR-AUD-01`, `NFR-AUD-02`, `NFR-OBS-01`, `NFR-OBS-02`
