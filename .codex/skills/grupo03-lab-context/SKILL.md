---
name: grupo03-lab-context
description: Inicia, desarrolla o revisa laboratorios de Arquitectura de Software del Grupo 03 usando aprendizajes verificados de laboratorios anteriores. Úsalo para nuevos labs del curso; no lo uses para tareas ajenas al repositorio.
---

# Contexto de laboratorios del Grupo 03

## Fuente de contexto

Lee completamente [Grupo03Brain.md](../../../Grupo03Brain.md) antes de tomar decisiones sobre un laboratorio.

Lee también el enunciado y los artefactos del laboratorio actual. El brain orienta, pero no reemplaza los requisitos actuales ni convierte una decisión de un laboratorio anterior en una regla universal.

## Forma de trabajo

1. Separa el texto del enunciado, las decisiones del equipo y las inferencias necesarias. Declara las inferencias que afecten alcance o arquitectura.
2. Define problema, usuarios, personas y pain points antes de seleccionar una arquitectura.
3. Traza cada requerimiento a una necesidad y exige criterios verificables antes de considerarlo cubierto.
4. Selecciona la alternativa arquitectónica más sencilla que satisfaga los atributos de calidad demostrados. No asumas microservicios, colas, varias aplicaciones o varias bases de datos sin evidencia.
5. Mantén una sola plataforma con vistas por rol cuando los usuarios participan en el mismo proceso y comparten la fuente de datos.
6. Para acciones críticas, verifica tiempos máximos, prioridad, confirmación, contingencia y auditoría.
7. Implementa el POC únicamente para el happy path pedido; identifica explícitamente lo que no representa una solución productiva.
8. Ejecuta la evaluación definida por el laboratorio y conserva gaps reales aunque el puntaje objetivo se alcance.

## Aprendizaje acumulativo

Actualiza `Grupo03Brain.md` al terminar una iteración solo con aprendizajes reutilizables respaldados por una decisión, error o evaluación observable. No agregues resúmenes extensos, datos pasajeros ni preferencias que solo correspondan al caso actual.

Cada aprendizaje nuevo debe indicar:

- qué decisión futura modifica;
- de qué laboratorio proviene;
- qué evidencia lo respalda;
- cuándo no debe aplicarse.

## Convenciones del repositorio

- Conserva un directorio independiente por laboratorio: `Lab1`, `Lab2`, etc.
- Mantén los entregables navegables desde el `README.md` del laboratorio.
- Escribe en el idioma solicitado por el enunciado.
- No hagas commit ni push salvo que el usuario lo pida explícitamente.
- Si el usuario solicita commits bajo la identidad de Jean, usa `jeanPROangeles <69778955+jeanPROangeles@users.noreply.github.com>`.
