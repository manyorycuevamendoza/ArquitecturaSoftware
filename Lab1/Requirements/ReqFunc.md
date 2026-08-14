# Requerimientos Funcionales

Formato de ID: `RF-<módulo>-<n>`. Los tiempos indicados se verifican bajo las condiciones de carga definidas en los RNF. La columna **Rol responsable** identifica el único rol que ejecuta, administra o es propietario principal de la función; no representa a una persona modelo.

## Gestión de turnos

| ID | Requerimiento | Criterio de aceptación | Rol responsable |
| --- | --- | --- | --- |
| RF-TUR-01 | El sistema debe permitir asignar médicos y enfermeras a una sede, servicio y rango horario, y rechazar antes de guardar cualquier solapamiento para el mismo profesional. | En una prueba con cruces totales o parciales, el 100% de los intentos se rechaza y se muestra el turno en conflicto. Para cada paciente activo se muestra el médico responsable vigente y su alterno. | Administrador de red regional |

## Continuidad clínica y handoff

| ID | Requerimiento | Criterio de aceptación | Rol responsable |
| --- | --- | --- | --- |
| RF-DIA-01 | Antes de cerrar un turno, el médico saliente debe registrar un handoff estructurado por paciente con diagnóstico vigente, antecedentes y alergias relevantes, decisiones, cambios de medicación, resultados, acciones pendientes, prioridad, autor y hora. El personal clínico entrante autorizado debe poder consultarlo. | El sistema impide cerrar el turno si falta un campo obligatorio. En el 100% de los handoffs de prueba, el profesional entrante autorizado consulta el último handoff y su historial en ≤ 1 s desde la pantalla de pacientes. | Médico internista |
| RF-DIA-02 | El sistema debe conservar versiones de los handoffs y diagnósticos; ninguna actualización puede sobrescribir la versión anterior. | En una prueba de actualización, se recuperan todas las versiones con contenido, autor y fecha/hora, en orden cronológico. | Médico internista |

## Emergencias y notificaciones

| ID | Requerimiento | Criterio de aceptación | Rol responsable |
| --- | --- | --- | --- |
| RF-EME-01 | La enfermera de UCI debe poder crear una alerta crítica para un paciente desde la pantalla a pie de cama en un máximo de dos acciones. El sistema debe enviarla al médico responsable vigente y mostrar el estado de entrega. | En una prueba de usabilidad, al menos 90% del rol Enfermera de UCI crea la alerta en ≤ 30 s y el evento registra paciente, emisor, responsable, hora y estado. | Enfermera de UCI |
| RF-EME-02 | Si el responsable no confirma lectura o respuesta en 90 s, el sistema debe escalar automáticamente la alerta al alterno y al jefe de guardia definidos para el turno. Cada intento y confirmación debe quedar registrado. | En el 100% de pruebas sin confirmación inicial, se generan los destinatarios de escalamiento a los 90 s ± 5 s y la bitácora contiene entrega, lectura/respuesta y destinatarios. | Enfermera de UCI |
| RF-NOT-01 | El sistema debe enviar notificaciones de cambios críticos solo a profesionales autorizados que estén asignados al paciente o que formen parte de la regla de escalamiento vigente. | En una prueba con pacientes y turnos distintos, el 100% de notificaciones llega únicamente a los destinatarios correspondientes; los demás no la reciben. | Médico internista |
| RF-NOT-02 | El sistema debe permitir clasificar una notificación como crítica, alta o informativa y mostrar en la alerta crítica el estado entregada, leída, respondida o escalada. | Cada estado se actualiza y queda disponible en la bitácora de la alerta; las alertas informativas no activan el protocolo de `RF-EME-02`. | Enfermera de UCI |

## Operación con conectividad intermitente

| ID | Requerimiento | Criterio de aceptación | Rol responsable |
| --- | --- | --- | --- |
| RF-CON-01 | La aplicación a pie de cama debe permitir registrar signos y eventos clínicos cuando la sede pierde conectividad, informar visiblemente el estado pendiente de sincronización y sincronizar los registros al restablecerla. | Tras una desconexión de 30 min, el 100% de registros locales de prueba permanece disponible localmente y se sincroniza una sola vez en ≤ 5 min tras recuperar conectividad, conservando autor y hora original. | Enfermera de UCI |

## Administración, acceso, auditoría y reportes

| ID | Requerimiento | Criterio de aceptación | Rol responsable |
| --- | --- | --- | --- |
| RF-ADM-01 | El administrador de red regional debe crear y aplicar plantillas de sede que incluyan servicios, roles, reglas de escalamiento y parámetros, a una o más sedes sin configuración manual individual. | Una plantilla se aplica por lote a 40 sedes de prueba; cada resultado de sede queda como exitoso o fallido con causa y puede revertirse sin alterar las demás. | Administrador de red regional |
| RF-ACC-01 | El administrador de red regional debe gestionar altas, bajas y cambios de rol. El sistema debe limitar la consulta y edición de datos clínicos al personal con rol autorizado y relación asistencial o de turno vigente. | Cuentas sin permiso, fuera de turno o sin relación asistencial no pueden consultar ni editar datos clínicos; los intentos se registran en auditoría. | Administrador de red regional |
| RF-AUD-01 | El sistema debe mantener una bitácora inalterable de creaciones, consultas, cambios y accesos a datos clínicos, handoffs, turnos y alertas. Debe permitir filtrar y exportar por sede, paciente, usuario, tipo de evento y periodo. | Cada evento de prueba registra actor, acción, objeto, fecha/hora, sede y resultado; una exportación reproduce los eventos filtrados sin omisiones. | Jefatura de gestión clínica |
| RF-REP-01 | El sistema debe ofrecer un tablero regional y reportes exportables por sede, servicio y turno con: porcentaje de handoffs cerrados, tiempos de entrega y escalamiento de alertas, disponibilidad, RTO y accesos auditados. | Con datos de prueba de dos sedes, el tablero calcula cada indicador por sede y periodo y su exportación coincide con la bitácora fuente. | Jefatura de gestión clínica |

## Información al familiar autorizado

| ID | Requerimiento | Criterio de aceptación | Rol responsable |
| --- | --- | --- | --- |
| RF-FAM-01 | El profesional autorizado debe poder registrar y compartir con el familiar autorizado un resumen de estado y del responsable de turno, sin exponer información clínica no autorizada. | Solo el familiar con autorización vigente puede visualizar el resumen; el acceso y cada publicación quedan auditados y el sistema no permite publicar campos restringidos. | Médico internista |

## Matriz resumida de trazabilidad

| Problemática | Requerimientos que la cubren |
| --- | --- |
| Rotación y continuidad clínica | RF-TUR-01, RF-DIA-01, RF-DIA-02, RF-AUD-01 |
| Emergencia nocturna | RF-TUR-01, RF-EME-01, RF-EME-02, RF-NOT-01, RF-NOT-02 |
| Actualizaciones en tiempo real y conectividad | RF-NOT-01, RF-NOT-02, RF-CON-01 |
| Gestión regional, cumplimiento y escala | RF-ADM-01, RF-ACC-01, RF-AUD-01, RF-REP-01 |
