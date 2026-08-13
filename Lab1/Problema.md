# Definición del Problema

## Contexto

EsSalud iniciará en Lima un piloto de una plataforma para apoyar la gestión operativa y clínica de las Unidades de Cuidados Intensivos (UCI). La plataforma debe centralizar los horarios de médicos y enfermeras, así como los diagnósticos y novedades relevantes de los pacientes.

En una UCI los cambios de turno son frecuentes y los médicos internistas rotan con alta regularidad. La información clínica debe pasar de un turno al siguiente de forma completa, oportuna y trazable: una omisión o una demora puede afectar la continuidad de la atención. A la vez, ante un deterioro nocturno de un paciente, el personal debe poder identificar y contactar rápidamente al profesional responsable, y contar con una ruta de escalamiento si este no está disponible.

## Problema central

EsSalud no cuenta con un mecanismo integrado y confiable que coordine los turnos de su personal de UCI, preserve el diagnóstico actualizado entre relevos y active de forma inmediata al profesional adecuado ante una urgencia. Este desorden genera riesgo de cruces de horario, pérdida o retraso de información clínica, demoras en la atención y falta de claridad sobre quién debe responder ante un evento crítico.

Se requiere una plataforma regional que permita gestionar horarios sin conflictos, registrar y consultar diagnósticos actualizados durante todo el ciclo de atención, y emitir notificaciones con escalamiento a los responsables disponibles. La solución debe operar con alta disponibilidad y crecer desde el piloto en Lima hasta una red nacional de gran escala.

## Problemáticas críticas

### 1. Rotación de médicos

El médico o enfermera que termina su turno debe dejar disponible para el equipo entrante el diagnóstico vigente, las observaciones y las acciones pendientes del paciente. El sistema debe evitar que el relevo dependa de comunicaciones informales o de registros dispersos, y debe permitir identificar qué información fue registrada, por quién y cuándo.

### 2. Problema de medianoche

Si un paciente se agrava durante el turno nocturno, el personal debe saber de inmediato cuál es el médico responsable de acuerdo con el horario vigente y poder contactarlo. Si ese profesional no responde o no está disponible, el sistema debe escalar la alerta a un responsable alterno definido, sin perder tiempo ni dejar la situación sin atención.

### 3. Actualizaciones en tiempo real

Los cambios clínicos relevantes, modificaciones de turno y alertas de urgencia deben notificarse oportunamente a los médicos y enfermeras involucrados, incluso cuando existan varios destinatarios. Los diagnósticos y actualizaciones deben persistirse de forma segura y estar disponibles para consulta cuando sean necesarios, evitando información desactualizada o inconsistente entre turnos.

## Metas de escalamiento

| Hito        | Hospitales |
| ----------- | ---------- |
| Lanzamiento | 1K         |
| 6 meses     | 100K       |
| 2 años      | 10M        |

## Metas de rendimiento

| Métrica                        | Objetivo |
| ------------------------------ | -------- |
| Tiempo de inicio de aplicación | < 1 s    |
| Configuración de aplicación    | < 5 s    |
| Disponibilidad                 | 99.9%    |
| Recuperación ante caída        | < 5 min  |
