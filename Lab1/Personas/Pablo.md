# Pablo — Médico Internista

> Foco: Continuidad del diagnóstico entre turnos

## Perfil

| Campo | Valor |
| --- | --- |
| Nombre | Pablo Quispe Arana |
| Rol | Médico Internista de UCI |
| Edad | 41 años |
| Sede | Hospital Nacional Edgardo Rebagliati Martins (Lima) — rota además en 2 sedes de la red |
| Nivel tecnológico | Medio-alto; usa historia clínica electrónica a diario, pero no tolera flujos largos |
| Dispositivos | Laptop del hospital (compartida), smartphone Android personal, tablet en ronda |

## Contexto diario
Cubre turnos de 12 horas y rota entre sedes, por lo que rara vez atiende al mismo paciente dos días
seguidos. Al iniciar el turno recibe entre 8 y 15 pacientes críticos y necesita reconstruir en minutos
qué se hizo en las últimas 24 horas: diagnóstico presuntivo, cambios de medicación, resultados
pendientes y decisiones tomadas por el médico saliente. Hoy ese traspaso ocurre de forma verbal y en
notas dispersas, así que pierde los primeros 30–40 minutos del turno preguntando.

## Objetivos
1. Ver el estado y el diagnóstico vigente de cada paciente asignado en menos de 1 minuto al entrar al turno.
2. Dejar un handoff estructurado antes de salir, sin duplicar lo que ya está en la historia clínica.
3. Ser notificado solo de lo que le compete (sus pacientes, su turno) para no normalizar las alertas.
4. Acceder al historial de decisiones previas, con autor y hora, para no repetir estudios ni tratamientos.

## Frustraciones / Dolores
1. El handoff depende de que el médico saliente esté disponible; si ya se fue, la información se pierde.
2. Notas escritas en formatos distintos por cada colega: no puede comparar ni buscar.
3. La aplicación tarda en abrir y en cargar el listado, justo cuando tiene menos tiempo.
4. Recibe notificaciones de pacientes que no son suyos y termina ignorándolas todas.
5. Cuando el sistema se cae, no hay forma de saber qué información quedó sin registrar.
6. Debe revisar varias fuentes para reconstruir cambios de medicación, resultados y decisiones recientes.
7. Duplica información al completar el handoff y luego actualizar la historia clínica.
8. Los resultados pendientes no tienen un responsable visible y pueden quedar sin seguimiento.
9. Al rotar de sede encuentra flujos y criterios de registro diferentes.
10. No puede priorizar rápidamente a los pacientes más críticos al comenzar la ronda.

## Escenario clave
Pablo llega a las 7:00 a.m. a una sede en la que no estuvo la semana anterior. Abre la aplicación en su
teléfono camino a la UCI; en menos de un segundo ve sus 12 pacientes ordenados por criticidad, con el
handoff que dejó el médico de la noche: diagnóstico presuntivo, cambios de las últimas 12 horas y
pendientes marcados. Entra a la ronda ya sabiendo a qué dos camas ir primero.

## Criterios de éxito
- Tiempo de reconstrucción del contexto clínico al iniciar turno: < 5 minutos (hoy 30–40).
- 100% de los pacientes con handoff estructurado registrado antes del cierre de turno.
- Cero decisiones clínicas repetidas por desconocimiento del turno anterior.
- Aplicación disponible y utilizable en la primera pantalla en < 1 s.

## Requerimientos que le importan
- RF-DIA-01 (handoff de diagnóstico), RF-NOT-01 (notificaciones en tiempo real), RF-TUR-01 (gestión de turnos)
- RNF-PER-01 (inicio < 1 s), RNF-DIS-01 (disponibilidad 99.9%), RNF-DIS-02 (recuperación < 5 min), RNF-SEG-01 (confidencialidad del dato clínico)
