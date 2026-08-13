# Requerimientos Funcionales

Formato de ID: `RF-<módulo>-<n>`

## 1. Gestión de turnos
| ID | Requerimiento | Prioridad | Persona |
| --- | --- | --- | --- |
| RF-TUR-01 | El sistema debe permitir la asignación de horarios para médicos y enfermeras, validando automáticamente que no existan cruces o solapamientos. | Alta | Claudia |

## 2. Handoff de diagnóstico (rotación de médicos)
| ID | Requerimiento | Prioridad | Persona |
| --- | --- | --- | --- |
| RF-DIA-01 | El sistema debe garantizar que el diagnóstico del médico saliente esté disponible de forma inmediata para el médico del turno entrante al iniciar sesión. | Alta | Pablo |

## 3. Escalamiento de emergencias (problema de medianoche)
| ID | Requerimiento | Prioridad | Persona |
| --- | --- | --- | --- |
| RF-EME-01 | El sistema debe proveer un mecanismo de contacto rápido para emergencias nocturnas, con un protocolo de escalamiento automático si el médico encargado no responde. | Alta | Claudia |

## 4. Notificaciones en tiempo real
| ID | Requerimiento | Prioridad | Persona |
| --- | --- | --- | --- |
| RF-NOT-01 | El sistema debe enviar notificaciones push simultáneas a médicos y enfermeras ante cambios críticos en el estado del paciente o actualizaciones de diagnóstico. | Alta | Pablo, Claudia |

## 5. Administración y configuración regional
| ID | Requerimiento | Prioridad | Persona |
| --- | --- | --- | --- |
| RF-ADM-01 | El sistema debe permitir la configuración y el despliegue centralizado de parámetros para hospitales a nivel regional (Lima) y nacional. | Media | Roberto |

## 6. Auditoría y reportes
| ID | Requerimiento | Prioridad | Persona |
| --- | --- | --- | --- |
| RF-AUD-01 | El sistema debe registrar un log inalterable de todos los diagnósticos y cambios de turno realizados para asegurar la trazabilidad del cuidado. | Media | Elena |
