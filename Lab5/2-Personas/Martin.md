# Martín — Data Science

> Foco: que el LLM aprenda con conocimiento validado y que cada versión se pruebe antes de publicarse.

## Perfil

| Campo | Valor |
| --- | --- |
| Rol | Data scientist, dueño del LLM local y del pipeline de conocimiento |
| Tipo | Usuario interno; no opera incidencias |
| Responsabilidad | Ingesta de datos del cliente, curación, eval set, enriquecimiento del LLM |
| Nivel técnico | Alto |

## Contexto

Eligió el LLM local porque el detalle de las incidencias no puede salir de la
compañía. Recibe las quejas de que "el LLM no aprende" y de que cada versión
responde distinto. No puede reentrenar el modelo cada semana ni tiene GPU de
sobra: lo que sí puede hacer es controlar qué conocimiento entra, medirlo antes
de publicarlo y no gastar el modelo en preguntas que no lo necesitan.

## Objetivos

1. Ingestar datos del cliente y curarlos antes de que lleguen al LLM.
2. Saber si una versión nueva de conocimiento o prompt responde mejor o peor que la anterior.
3. Que las calificaciones de los ingenieros alimenten el conocimiento.
4. Probar con datos realistas sin exponer el detalle del cliente.

## Pain points

1. Un cambio de versión altera todas las respuestas y nadie lo nota hasta que hay quejas.
2. Las correcciones de los ingenieros se pierden; no hay dónde guardarlas.
3. La GPU no alcanza y no hay forma de decidir qué consultas la necesitan.
4. No puede usar datos reales para probar sin arriesgar la confidencialidad.
5. El dato crudo del cliente entra al modelo sin validar.

## Escenario clave

Los **Sistemas del cliente** entregan datos; **Ingesta de data del cliente** los
deja en **BD3** junto con los scores que dejaron Camila y Andrés. Martín corre
**Curación de conocimiento**: lo crudo se convierte en conocimiento validado con
autor, fecha y vigencia. **Enriquecimiento del LLM** prepara la versión nueva y
el **Eval set de respuestas conocidas** la compara con la vigente: exactitud,
abstención correcta y acciones indebidas. Pasa; la propuesta va a **Aprobación
de cambios al conocimiento** para Paola. Las pruebas del cambio corren sobre la
**Réplica anonimizada**.

## Criterios de éxito

- Cero cambios de conocimiento publicados sin pasar el eval set.
- Cada versión de modelo, prompt y conocimiento fechada y trazable.
- ≥ 60% de las consultas resueltas sin invocar al LLM.
- Ningún dato de cliente sin anonimizar en el entorno de pruebas.

## Requisitos que lo cubren

`FR-ANS-07`, `FR-ANS-10`, `FR-ANS-11`, `FR-ANS-12`, `FR-ACT-08`, `NFR-DET-02`,
`NFR-SEC-04`, `NFR-CAP-01`
