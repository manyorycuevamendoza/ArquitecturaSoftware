# Requerimientos No Funcionales

Formato de ID: `RNF-<atributo>-<n>`

## Rendimiento

| ID | Requerimiento | Métrica objetivo |
| --- | --- | --- |
| RNF-PER-01 | Tiempo de inicio de la aplicación | < 1 s |
| RNF-PER-02 | Tiempo de configuración de la aplicación | < 5 s |

## Disponibilidad y recuperación

| ID | Requerimiento | Métrica objetivo |
| --- | --- | --- |
| RNF-DIS-01 | Disponibilidad del sistema | 99.9% |
| RNF-DIS-02 | Tiempo de recuperación ante caída (RTO) | < 5 min |
| RNF-DIS-03 | Pérdida máxima de datos (RPO) | Cercano a 0 segundos (Garantizar que los diagnósticos estén disponibles en todo momento) |

## Escalabilidad

| ID | Requerimiento | Métrica objetivo |
| --- | --- | --- |
| RNF-ESC-01 | Hospitales soportados al lanzamiento | 1K |
| RNF-ESC-02 | Hospitales soportados a 6 meses | 100K |
| RNF-ESC-03 | Hospitales soportados a 2 años | 10M |

## Seguridad y privacidad

| ID | Requerimiento | Métrica objetivo |
| --- | --- | --- |
| RNF-SEG-01 | Protección de datos de salud (UCI) | Cifrado de extremo a extremo para diagnósticos y datos sensibles de pacientes |

## Usabilidad

| ID | Requerimiento | Métrica objetivo |
| --- | --- | --- |
| RNF-USA-01 | Facilidad de uso para personal rotativo | Curva de aprendizaje < 15 min debido a la alta rotación de médicos internistas |

## Observabilidad y mantenibilidad

| ID | Requerimiento | Métrica objetivo |
| --- | --- | --- |
| RNF-OBS-01 | Monitoreo de notificaciones críticas | Latencia de entrega < 2 segundos para notificaciones push de emergencia |
