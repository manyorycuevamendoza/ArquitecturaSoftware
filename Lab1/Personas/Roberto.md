# Roberto — Administrador de Red Regional

> Foco: Configuración y escalamiento

## Perfil

| Campo | Valor |
| --- | --- |
| Nombre | Roberto Cárdenas Loayza |
| Rol | Administrador de la red hospitalaria regional (TI EsSalud) |
| Edad | 45 años |
| Sede | Oficina regional Lima; da soporte a hospitales de Lima y distritos |
| Nivel tecnológico | Alto; administra infraestructura, redes y despliegues |
| Dispositivos | Laptop corporativa, consola de administración web, VPN, smartphone para alertas de guardia |

## Contexto diario
Es responsable de dar de alta hospitales, servicios y usuarios en el sistema, y de que el piloto
regional pueda crecer de 1K a 100K y luego a 10M de hospitales sin rediseñar la operación. Cada
hospital nuevo llega con su propia realidad: conectividad intermitente en distritos, personal con
rotación alta y equipos heterogéneos. Su métrica personal es el tiempo de puesta en marcha por sede y
la cantidad de incidentes que escalan hasta él.

## Objetivos
1. Configurar y activar un hospital nuevo en menos de 5 segundos de configuración de aplicación por instancia.
2. Gestionar roles, turnos y reglas de escalamiento de forma centralizada, sin tocar cada sede.
3. Monitorear disponibilidad, latencia y errores por región desde un solo tablero.
4. Escalar horizontalmente sin ventanas de indisponibilidad para las UCI en operación.

## Frustraciones / Dolores
1. Cada sede exige configuración manual: no escala más allá de unas decenas de hospitales.
2. No tiene visibilidad de qué falló ni dónde cuando una UCI reporta que "el sistema está lento".
3. Las sedes de distrito pierden conectividad y no hay comportamiento definido para modo degradado.
4. Los despliegues obligan a coordinar ventanas con áreas clínicas que operan 24/7.
5. La gestión de accesos crece sin control con la rotación de personal.

## Escenario clave
EsSalud incorpora 40 hospitales de distrito en una semana. Roberto carga la configuración desde una
plantilla regional, define reglas de escalamiento por defecto y activa las sedes por lotes; cada
instancia queda configurada en menos de 5 segundos. Cuando dos sedes pierden enlace, su tablero se lo
muestra y el sistema mantiene el modo degradado local hasta que la conexión vuelve y sincroniza.

## Criterios de éxito
- Alta de un hospital nuevo sin intervención manual sede por sede.
- Configuración de aplicación < 5 s; disponibilidad regional ≥ 99.9%.
- Recuperación ante caída < 5 min, verificada con simulacros.
- Crecimiento a 100K y 10M de hospitales sin cambio de arquitectura ni ventanas de indisponibilidad.

## Requerimientos que le importan
- RF-ADM-01 (administración y configuración regional), RF-TUR-01 (roles y turnos), RF-NOT-01 (entrega de notificaciones)
- RNF-ESC-01/02/03 (1K, 100K, 10M hospitales), RNF-PER-02 (configuración < 5 s), RNF-DIS-01/02 (disponibilidad y RTO), RNF-OBS-01 (observabilidad), RNF-SEG-01 (control de accesos)
