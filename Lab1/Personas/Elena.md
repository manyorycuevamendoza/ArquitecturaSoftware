# Elena — Jefa de Gestión Clínica (EsSalud)

> Foco: Cumplimiento y métricas regionales

## Perfil

| Campo | Valor |
| --- | --- |
| Nombre | Elena Fuentes Navarro |
| Rol | Jefa de Gestión Clínica — EsSalud (cliente institucional) |
| Edad | 52 años |
| Sede | Sede central EsSalud, Lima; responsable del piloto regional |
| Nivel tecnológico | Medio; consume tableros y reportes, no opera el sistema clínico |
| Dispositivos | Laptop corporativa, smartphone, proyector en comités directivos |

## Contexto diario
Responde ante la dirección por los resultados del piloto y por el cumplimiento normativo del manejo de
datos clínicos. No usa el sistema a pie de cama: necesita evidencia agregada de que el handoff ocurre,
de que las emergencias se escalan a tiempo y de que el servicio está disponible. Su decisión de
extender el piloto a más regiones depende de indicadores comparables entre sedes.

## Objetivos
1. Medir tiempo de respuesta ante emergencias y cobertura de handoff por sede, servicio y turno.
2. Demostrar trazabilidad y auditoría completa de accesos y decisiones clínicas registradas.
3. Justificar el escalamiento del piloto (1K → 100K → 10M hospitales) con datos, no con percepciones.
4. Cumplir la normativa de protección de datos personales de salud sin frenar la operación clínica.

## Frustraciones / Dolores
1. Cada hospital reporta con su propio formato: no puede comparar ni consolidar.
2. Los indicadores llegan con semanas de retraso, cuando el problema ya escaló.
3. No hay evidencia auditable de quién accedió a qué información clínica y cuándo.
4. Los incidentes de disponibilidad se reportan de forma anecdótica, sin métrica de RTO real.

## Escenario clave
Fin del primer trimestre del piloto. Elena abre el tablero regional antes del comité directivo: ve
tiempo mediano de escalamiento de emergencias por sede, porcentaje de turnos cerrados con handoff
estructurado y disponibilidad del sistema del periodo. Detecta dos sedes fuera de meta, exporta el
reporte de auditoría y presenta la recomendación de ampliar el piloto con un plan de refuerzo focalizado.

## Criterios de éxito
- Indicadores homogéneos y comparables entre todas las sedes del piloto.
- Reportes disponibles sin espera manual, con trazabilidad completa de accesos.
- Disponibilidad ≥ 99.9% y RTO < 5 min demostrados con registro histórico.
- Cero hallazgos de incumplimiento en auditoría de protección de datos clínicos.

## Requerimientos que le importan
- RF-AUD-01 (auditoría y reportes), RF-DIA-01 (evidencia de handoff), RF-EME-01 (tiempos de escalamiento)
- RNF-SEG-01 (seguridad y privacidad), RNF-DIS-01/02 (disponibilidad y RTO), RNF-OBS-01 (observabilidad), RNF-ESC-01/02/03 (metas de escalamiento)
