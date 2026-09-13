# Camila — Ingeniera de soporte

> Foco: atender escalaciones de cliente sin que una instrucción suya cause daño, y con el estado vigente.

## Perfil

| Campo | Valor |
| --- | --- |
| Rol | Ingeniera de soporte, turno diurno |
| Tipo | Usuario directo |
| Incidencias que atiende | Customer escalations y support escalations |
| SLA que la presiona | 1 día (customer) |
| Nivel técnico | Medio: conoce el producto y el cliente; no escribe SQL |

## Contexto

Atiende entre 15 y 25 escalaciones por día, la mayoría con un cliente esperando
respuesta. Le pregunta a Genius en lenguaje natural: "¿en qué estado está la
INC-4521?", "¿qué pasó con casos parecidos?", "cierra la INC-4521 como
resuelta". Fue una instrucción suya la que el LLM interpretó como "borrar la
base de datos" el mes pasado.

## Objetivos

1. Preguntar el estado de una incidencia y que la respuesta sea la de ahora, con hora.
2. Pedir una acción sabiendo que alguien más la revisa antes de que toque datos.
3. Que la misma pregunta le dé siempre la misma respuesta.
4. Poder decir "esta respuesta estuvo mal" y que sirva de algo.

## Pain points

1. Dio una instrucción y el LLM borró la base de datos.
2. Genius le dijo "abierta" de una incidencia cerrada hace horas.
3. Cada día la misma pregunta frecuente da una respuesta distinta.
4. El texto que escribió el cliente en la incidencia puede terminar mandando sobre el sistema.
5. En la primera semana del mes Genius no le responde cuando más lo necesita.
6. No sabe si lo que le contestó Genius es dato real o invención.

## Escenario clave

Camila pregunta "¿estado de la INC-4521?". Auth y rol la identifica como
soporte; la pregunta se clasifica como *estado* y va a **Estado de incidencia**,
que lee BD1 sin pasar por el LLM. Recibe "Cerrada, dato de las 10:42". Luego
pide "cierra la INC-4530". La consulta es de escritura: pasa por **Vista previa
de impacto** (1 registro), **Bloqueo de escritura** la detiene y Paola recibe
"hay una acción esperando tu aprobación". Aprobada, **Ejecución** la aplica con
los permisos de Camila y queda en **Auditoría**. Camila califica la respuesta con
**Score y motivo**.

## Criterios de éxito

- Cero acciones de escritura ejecutadas sin aprobación de otra persona.
- Estado con hora del dato en el 100% de las respuestas.
- Misma pregunta frecuente, misma respuesta, veinte veces seguidas.
- Respuesta de estado en ≤ 2 s aunque el LLM esté saturado.

## Requisitos que la cubren

`FR-ACT-03`, `FR-ACT-04`, `FR-ACT-05`, `FR-ACT-07`, `FR-ANS-01`, `FR-ANS-02`,
`FR-ANS-03`, `FR-ANS-04`, `FR-ANS-06`, `FR-ANS-10`, `FR-ANS-13`, `FR-REL-05`,
`NFR-PER-01`, `NFR-FRE-01`, `NFR-FRE-02`, `NFR-DET-01`, `NFR-DET-03`,
`NFR-SEC-01`, `NFR-USA-01`
