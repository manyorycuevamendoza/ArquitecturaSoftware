# Andrés — Ingeniero de desarrollo

> Foco: que Genius responda durante el pico y que las pruebas E2E nunca toquen producción.

## Perfil

| Campo | Valor |
| --- | --- |
| Rol | Ingeniero de desarrollo, rota como ingeniero de guardia |
| Tipo | Usuario directo |
| Incidencias que atiende | Engineering escalations y las que soporte le escala |
| SLA que lo presiona | 3 días (engineering), 1 día si viene de un cliente |
| Nivel técnico | Alto: lee logs, consultas y resultados de E2E |

## Contexto

Recibe incidencias ya escaladas: llegan con el contexto de soporte, las
incidencias similares del histórico y, cuando aplica, el resultado de una
prueba E2E. En la primera semana de cada mes tiene tres veces más incidencias y
Genius deja de responder o responde tarde. Necesita saber rápido si algo ya
pasó antes y cómo se resolvió.

## Objetivos

1. Abrir una incidencia escalada con todo el contexto cargado.
2. Encontrar incidencias similares del histórico y cómo se resolvieron.
3. Correr una prueba E2E sin riesgo de tocar producción.
4. Que Genius le diga "no sé" en lugar de inventar.

## Pain points

1. La primera semana del mes Genius no responde justo cuando más lo necesita.
2. Cuando falla, falla entero: no hay respuesta parcial ni explicación.
3. El modelo afirma cosas que no puede sustentar y pierde una hora comprobándolas.
4. Una prueba E2E podría correr contra producción y nadie lo impediría.
5. Una consulta lenta a la base de datos histórica cuelga toda la respuesta.
6. Un reintento de una acción puede ejecutarla dos veces.

## Escenario clave

Primera semana del mes, 11:00. Andrés abre una engineering escalation. La
solicitud entra por **Auth y rol**, recibe clase `ENGINEERING` y va a la **Cola
por prioridad**, donde se atiende después de las de cliente. **Incidencia
escalada** le entrega el contexto; **Incidencias similares** consulta BD2 (solo
lectura) y el LLM propone una hipótesis. Andrés pide una prueba E2E: el
**Orquestador** la ejecuta en el **Entorno de pruebas** con la **Réplica
anonimizada**, nunca contra producción. A las 11:20 el LLM se satura: el
cortacircuito abre y **Modo degradado** le sigue respondiendo estado y ficha de
la incidencia, marcados como "sin modelo". Cuando no hay dato, **Abstención** se
lo dice.

## Criterios de éxito

- Cero pruebas E2E ejecutadas contra producción.
- Respuesta útil (aunque degradada) en el 100% de las consultas durante el pico.
- Abstención explícita cuando no hay dato, nunca una afirmación sin fuente.
- Ningún reintento produce una acción duplicada.

## Requisitos que lo cubren

`FR-ACT-08`, `FR-ACT-10`, `FR-ANS-05`, `FR-ANS-08`, `FR-ANS-09`, `FR-REL-03`,
`FR-REL-04`, `FR-REL-05`, `FR-REL-06`, `FR-REL-07`, `FR-REL-09`, `NFR-AVL-01`,
`NFR-AVL-04`, `NFR-PER-03`, `NFR-PER-04`, `NFR-CAP-01`, `NFR-USA-02`
