# Requerimientos No Funcionales

Formato de ID: `RNF-<atributo>-<n>`. Todos los porcentajes y tiempos se medirán mediante la prueba indicada —automatizada cuando aplique y con participantes para usabilidad— y su evidencia se conservará en `RF-AUD-01` y `RF-REP-01`. La columna **Rol responsable** identifica el único rol propietario de cada requisito.

## Rendimiento

| ID | Requerimiento | Métrica y condición de verificación | Rol responsable |
| --- | --- | --- | --- |
| RNF-PER-01 | Inicio de la aplicación | El percentil 95 del tiempo hasta mostrar la lista de pacientes asignados será < 1 s, medido desde una red hospitalaria disponible y con sesión autenticada. | Médico internista |
| RNF-PER-02 | Configuración de aplicación | El percentil 95 de aplicar una plantilla de sede será < 5 s por sede, sin contar la carga inicial del archivo de lote. | Administrador de red regional |
| RNF-PER-03 | Consulta de información clínica | El percentil 95 de abrir el último handoff y su historial autorizado será ≤ 1 s. | Médico internista |

## Disponibilidad, recuperación y conectividad

| ID | Requerimiento | Métrica y condición de verificación | Rol responsable |
| --- | --- | --- | --- |
| RNF-DIS-01 | Disponibilidad del sistema | Disponibilidad mensual ≥ 99.9% para consulta, registro de handoff y creación de alertas, medida por región y excluyendo solo mantenimientos anunciados con al menos 7 días de anticipación. | Administrador de red regional |
| RNF-DIS-02 | Recuperación ante caída (RTO) | El servicio clínico prioritario se recuperará en < 5 min desde una caída total simulada, verificado mediante simulacro trimestral. | Administrador de red regional |
| RNF-DIS-03 | Pérdida máxima de datos (RPO) | RPO = 0 s para handoffs, diagnósticos, turnos y alertas confirmados por el sistema. Los registros offline deben cumplir `RF-CON-01` y no se consideran confirmados hasta sincronizarse. | Administrador de red regional |
| RNF-CON-01 | Operación degradada | Una sede sin conexión debe conservar la capacidad local de registrar eventos durante al menos 30 min y mostrar que el dato está pendiente de sincronización. | Enfermera de UCI |

## Escalabilidad

| ID | Requerimiento | Métrica y condición de verificación | Rol responsable |
| --- | --- | --- | --- |
| RNF-ESC-01 | Capacidad al lanzamiento | Soportar 1,000 hospitales registrados, 10,000 usuarios concurrentes y 100 alertas críticas por segundo, cumpliendo `RNF-PER-01`, `RNF-OBS-01` y `RNF-DIS-01`. | Administrador de red regional |
| RNF-ESC-02 | Capacidad a 6 meses | Soportar 100,000 hospitales registrados, 100,000 usuarios concurrentes y 1,000 alertas críticas por segundo, cumpliendo los mismos RNF. | Administrador de red regional |
| RNF-ESC-03 | Capacidad a 2 años | Soportar 10,000,000 hospitales registrados, 1,000,000 usuarios concurrentes y 10,000 alertas críticas por segundo, cumpliendo los mismos RNF. | Administrador de red regional |

## Seguridad y privacidad

| ID | Requerimiento | Métrica y condición de verificación | Rol responsable |
| --- | --- | --- | --- |
| RNF-SEG-01 | Protección de datos de salud | Los datos clínicos se cifrarán en tránsito y en reposo; el acceso requerirá autenticación y autorización según `RF-ACC-01`. En pruebas de control de acceso, 100% de intentos no autorizados debe ser denegado y auditado. | Administrador de red regional |
| RNF-SEG-02 | Protección de sesiones privilegiadas | Las cuentas administrativas deberán usar segundo factor de autenticación y las sesiones deberán expirar tras 15 min de inactividad. | Administrador de red regional |

## Usabilidad

| ID | Requerimiento | Métrica y condición de verificación | Rol responsable |
| --- | --- | --- | --- |
| RNF-USA-01 | Aprendizaje del personal rotativo | Al menos 90% de médicos internistas de prueba completa las tareas de consultar un handoff, registrar uno y crear una alerta crítica tras ≤ 15 min de inducción, sin asistencia. | Médico internista |
| RNF-USA-02 | Uso a pie de cama | Al menos 90% de enfermeras de UCI de prueba crea una alerta crítica en ≤ 30 s y ≤ 2 acciones, usando una tablet. | Enfermera de UCI |

## Observabilidad y mantenibilidad

| ID | Requerimiento | Métrica y condición de verificación | Rol responsable |
| --- | --- | --- | --- |
| RNF-OBS-01 | Entrega de notificaciones críticas | El percentil 95 de entrega de una alerta crítica será < 2 s desde su registro hasta el dispositivo del destinatario disponible; se medirá por sede y región. | Administrador de red regional |
| RNF-OBS-02 | Monitoreo operativo | El tablero deberá mostrar cada 1 min disponibilidad, latencia, errores, alertas pendientes de confirmación y estado de sincronización por sede y región. | Administrador de red regional |
