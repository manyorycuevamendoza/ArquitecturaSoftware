# Lucía — Cliente (empresa)

> Foco: saber el estado real de su escalación sin que su información se exponga.

## Perfil

| Campo | Valor |
| --- | --- |
| Rol | Responsable de operaciones en una empresa cliente |
| Tipo | Usuario externo / beneficiaria |
| Incidencias que le importan | Las customer escalations que su empresa reportó |
| SLA que espera | 1 día |
| Nivel técnico | Bajo: no conoce el sistema interno; quiere una respuesta clara |

## Contexto

Reporta una escalación cuando algo afecta su negocio y espera respuesta en un
día. Entra a Genius solo para ver sus propias incidencias. Le han contestado
"en proceso" de casos que ya estaban cerrados y no sabe si la información que
puso en el reporte la ve alguien más. El SLA de un día existe por ella; el
diseño la prioriza aunque no opere el sistema.

## Objetivos

1. Ver el estado real de sus incidencias, con hora.
2. Que su escalación se atienda antes que el trabajo interno de ingeniería.
3. Que nadie fuera de su empresa vea el detalle de lo que reportó.
4. Recibir aviso cuando su incidencia cambie.

## Pain points

1. Le dicen "en proceso" de una incidencia cerrada hace horas.
2. Su escalación espera detrás de trabajo rutinario de ingeniería.
3. No sabe si su información sale de la compañía o llega a un canal equivocado.
4. En el pico del mes nadie le responde.

## Escenario clave

Lucía entra a Genius. **Auth y rol (solo sus incidencias)** la limita a las
escalaciones de su empresa. Pregunta por la INC-4521: **Estado de incidencia**
lee BD1 y **Respuesta con hora del dato** le muestra "Cerrada, 10:42". Su
solicitud entró con clase `CUSTOMER`, así que la **Cola por prioridad** la
atendió primero aunque fuera primera semana del mes. Cuando la incidencia
cambia, **Notificación al ingeniero** avisa a soporte con una referencia, no
con el detalle que ella escribió.

## Criterios de éxito

- Estado con hora del dato en cada respuesta.
- Ninguna respuesta con estado de otra empresa.
- Su escalación se admite en ≤ 5 s aun con ingeniería saturada.
- El detalle de su reporte nunca sale de la red corporativa.

## Requisitos que la cubren

`FR-ACT-11`, `FR-ANS-02`, `FR-ANS-03`, `FR-ANS-13`, `FR-REL-01`, `FR-REL-02`,
`NFR-AVL-02`, `NFR-PER-02`, `NFR-SEC-04`
