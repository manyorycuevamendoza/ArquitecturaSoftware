# Histórico de Requerimientos

Este documento conserva la línea base de la **iteración 1**, antes de la reevaluación que generó los requisitos vigentes de `ReqFunc.md` y `ReqNoFunc.md`. No debe usarse como especificación de implementación; se mantiene para trazabilidad del cambio y comparación con la iteración 2.

## Requerimientos funcionales — Iteración 1

| ID | Requerimiento anterior | Prioridad | Persona |
| --- | --- | --- | --- |
| RF-TUR-01 | El sistema debe permitir la asignación de horarios para médicos y enfermeras, validando automáticamente que no existan cruces o solapamientos. | Alta | Claudia |
| RF-DIA-01 | El sistema debe garantizar que el diagnóstico del médico saliente esté disponible de forma inmediata para el médico del turno entrante al iniciar sesión. | Alta | Pablo |
| RF-EME-01 | El sistema debe proveer un mecanismo de contacto rápido para emergencias nocturnas, con un protocolo de escalamiento automático si el médico encargado no responde. | Alta | Claudia |
| RF-NOT-01 | El sistema debe enviar notificaciones push simultáneas a médicos y enfermeras ante cambios críticos en el estado del paciente o actualizaciones de diagnóstico. | Alta | Pablo, Claudia |
| RF-ADM-01 | El sistema debe permitir la configuración y el despliegue centralizado de parámetros para hospitales a nivel regional (Lima) y nacional. | Media | Roberto |
| RF-AUD-01 | El sistema debe registrar un log inalterable de todos los diagnósticos y cambios de turno realizados para asegurar la trazabilidad del cuidado. | Media | Elena |

## Requerimientos no funcionales — Iteración 1

| ID | Requerimiento anterior | Métrica objetivo anterior |
| --- | --- | --- |
| RNF-PER-01 | Tiempo de inicio de la aplicación | < 1 s |
| RNF-PER-02 | Tiempo de configuración de la aplicación | < 5 s |
| RNF-DIS-01 | Disponibilidad del sistema | 99.9% |
| RNF-DIS-02 | Tiempo de recuperación ante caída (RTO) | < 5 min |
| RNF-DIS-03 | Pérdida máxima de datos (RPO) | Cercano a 0 segundos (Garantizar que los diagnósticos estén disponibles en todo momento) |
| RNF-ESC-01 | Hospitales soportados al lanzamiento | 1K |
| RNF-ESC-02 | Hospitales soportados a 6 meses | 100K |
| RNF-ESC-03 | Hospitales soportados a 2 años | 10M |
| RNF-SEG-01 | Protección de datos de salud (UCI) | Cifrado de extremo a extremo para diagnósticos y datos sensibles de pacientes |
| RNF-USA-01 | Facilidad de uso para personal rotativo | Curva de aprendizaje < 15 min debido a la alta rotación de médicos internistas |
| RNF-OBS-01 | Monitoreo de notificaciones críticas | Latencia de entrega < 2 segundos para notificaciones push de emergencia |

## Relación con la iteración 2

| Línea base | Estado en la iteración 2 |
| --- | --- |
| RF-TUR-01, RF-DIA-01, RF-EME-01, RF-NOT-01, RF-ADM-01 y RF-AUD-01 | Ampliados con criterios de aceptación y personas adicionales en [ReqFunc.md](ReqFunc.md). |
| RNF-PER-01/02, RNF-DIS-01/02/03, RNF-ESC-01/02/03, RNF-SEG-01, RNF-USA-01 y RNF-OBS-01 | Precisados con umbral, alcance y método de verificación en [ReqNoFunc.md](ReqNoFunc.md). |
| Gaps de la iteración 1 | Incorporados como nuevos requisitos `RF-DIA-02`, `RF-EME-02`, `RF-NOT-02`, `RF-CON-01`, `RF-ACC-01`, `RF-REP-01`, `RF-FAM-01`, `RNF-PER-03`, `RNF-CON-01`, `RNF-SEG-02`, `RNF-USA-02` y `RNF-OBS-02`. |
