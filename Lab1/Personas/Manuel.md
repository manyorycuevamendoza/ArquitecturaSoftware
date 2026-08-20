# Manuel — Paciente UCI / Familiar

> Foco: Beneficiario de la continuidad del cuidado

## Perfil

| Campo | Valor |
| --- | --- |
| Nombre | Manuel Tapia Solís (paciente) — representado por su hija Rosa (familiar) |
| Rol | Paciente crítico en UCI / familiar acompañante |
| Edad | 68 años (paciente); 39 años (familiar) |
| Sede | UCI del Hospital Guillermo Almenara (Lima) |
| Nivel tecnológico | Bajo (paciente, sedado gran parte del tiempo); medio (familiar, usa WhatsApp y banca móvil) |
| Dispositivos | Ninguno el paciente; smartphone Android gama media el familiar, con datos limitados |

## Contexto diario
Manuel no opera el sistema: lo vive a través de la calidad de la atención. Su hija Rosa espera fuera
de la UCI y depende de un reporte médico diario que a veces no llega porque el médico que la atendió
ayer ya rotó. Cada cambio de turno es, para la familia, un reinicio de la conversación: vuelven a
explicar antecedentes y alergias que ya habían informado.

## Objetivos
1. Que cualquier médico que atienda a Manuel conozca su historia y sus decisiones previas sin repreguntar.
2. Que un deterioro nocturno sea atendido rápido, sin depender de que alguien logre ubicar al médico.
3. Recibir información clara y oportuna sobre el estado del paciente y quién es el responsable del turno.
4. Que sus datos clínicos estén protegidos y solo accesibles por personal autorizado.

## Frustraciones / Dolores
1. Repetir antecedentes y alergias a cada nuevo médico o enfermera del turno.
2. Información contradictoria entre turnos sobre el diagnóstico o el plan de tratamiento.
3. No saber a quién dirigirse de noche ni si alguien está atendiendo el aviso de la enfermera.
4. Temor a que la información clínica se pierda o quede expuesta.
5. Recibir el reporte médico tarde o no recibirlo cuando cambia el profesional responsable.
6. No saber quién está a cargo del paciente durante cada turno.
7. Escuchar términos clínicos sin una explicación clara del estado y de los próximos pasos.
8. Tener que consultar a varias personas para reconstruir lo ocurrido durante la noche.
9. No poder confirmar si una decisión o indicación importante quedó registrada para el siguiente turno.
10. Sentir incertidumbre sobre si el equipo conoce las decisiones previas y preferencias del paciente.

## Escenario clave
Manuel se agrava a la 1:00 a.m. La enfermera escala la alerta y, al no haber respuesta en 90 segundos,
el sistema la deriva automáticamente al jefe de guardia, que llega con el diagnóstico y el plan
actualizados del turno anterior ya cargados. A la mañana siguiente, Rosa recibe un reporte consistente
con lo ocurrido de noche, sin tener que reconstruirlo preguntando a tres personas distintas.

## Criterios de éxito
- Cero repeticiones de antecedentes y alergias entre turnos.
- Atención efectiva de un deterioro nocturno en menos de 5 minutos desde la detección.
- Información consistente entre turnos: un solo diagnóstico vigente comunicado a la familia.
- Ningún acceso a su información clínica por personal no autorizado.

## Requerimientos que le importan
- RF-DIA-01 (handoff de diagnóstico), RF-EME-01 (escalamiento de emergencias), RF-NOT-01 (notificaciones al responsable de turno)
- RNF-SEG-01 (privacidad del dato clínico), RNF-DIS-01/02 (disponibilidad y recuperación), RNF-DIS-03 (RPO: no perder registros clínicos), RNF-USA-01 (claridad de la información)
