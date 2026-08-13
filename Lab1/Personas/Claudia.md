# Claudia — Enfermera de UCI

> Foco: Turnos y alertas de emergencia

## Perfil

| Campo | Valor |
| --- | --- |
| Nombre | Claudia Ríos Manrique |
| Rol | Enfermera asistencial de UCI (turno noche) |
| Edad | 33 años |
| Sede | Hospital Guillermo Almenara (Lima) |
| Nivel tecnológico | Medio; domina el equipo biomédico, prefiere interfaces simples y de pocos toques |
| Dispositivos | Smartphone Android personal, estación de enfermería compartida, tablet a pie de cama |

## Contexto diario
Cubre a 4–6 pacientes críticos por turno, casi siempre de noche, cuando la dotación médica es mínima.
Es la primera en detectar un deterioro y quien debe escalarlo. Trabaja con guantes, de pie y con las
manos ocupadas: cualquier flujo de más de dos o tres toques no lo usará. Su mayor riesgo es el
"problema de medianoche": avisa al médico de guardia y no obtiene respuesta, sin saber si el mensaje
llegó ni a quién avisar después.

## Objetivos
1. Escalar una emergencia en menos de 30 segundos y con confirmación visible de recepción.
2. Saber en todo momento quién es el médico responsable de cada paciente en el turno vigente.
3. Que la alerta escale automáticamente a un segundo responsable si nadie responde.
4. Registrar signos y eventos a pie de cama sin volver a la estación de enfermería.

## Frustraciones 
1. Llama al médico de guardia y no sabe si el aviso se recibió; termina llamando por teléfono personal.
2. No hay una regla clara de a quién escalar cuando el primer responsable no contesta.
3. El rol de guardia cambia y el sistema sigue mostrando al médico del turno anterior.
4. Exceso de notificaciones no críticas: se pierde la señal entre el ruido.
5. En el turno noche la red del hospital es inestable y no sabe si lo que registró se guardó.

## Escenario clave
2:40 a.m. El paciente de la cama 6 se desatura. Claudia marca la alerta crítica desde la tablet a pie
de cama en dos toques; el sistema notifica al médico de guardia asignado y muestra "entregado". A los
90 segundos no hay confirmación de lectura, así que la alerta escala sola al jefe de guardia y al
segundo internista, y Claudia lo ve en pantalla sin dejar al paciente. El evento queda registrado con
hora, destinatarios y tiempos de respuesta.

## Criterios de éxito
- Tiempo desde detección hasta alerta enviada: < 30 s.
- 100% de alertas críticas con acuse de recibo o escalamiento automático antes de los 2 minutos.
- Cero emergencias resueltas por vía informal (llamada al celular personal).
- Registro a pie de cama sin pérdida de datos ante caída de red.

## Requerimientos que le importan
- RF-EME-01 (escalamiento de emergencias), RF-NOT-01 (notificaciones en tiempo real), RF-TUR-01 (gestión de turnos)
- RNF-DIS-01 (disponibilidad 99.9%), RNF-DIS-02 (recuperación < 5 min), RNF-DIS-03 (RPO), RNF-USA-01 (usabilidad con manos ocupadas)
