# Requerimientos no funcionales

> El enunciado pide los requerimientos en formato backlog, solo con titulo. Esa vista esta en [Backlog.md](Backlog.md); este documento es el detalle de respaldo de los requerimientos no funcionales.

| ID | Requerimiento y verificacion | Responsable |
| --- | --- | --- |
| NFR-SEC-01 | Datos sensibles cifrados en transito y reposo; todos los accesos no autorizados son denegados y auditados. | Plataforma |
| NFR-SEC-02 | MFA para remitentes y operadores; sesion de operadores expira tras 15 minutos inactivos. | Plataforma |
| NFR-SEC-03 | El ledger es append-only para roles de aplicacion; no se permite actualizar o borrar movimientos. | Plataforma |
| NFR-SEC-04 | Las alertas AML, listas de sanciones y datos de identidad solo son visibles para cumplimiento; remitente, beneficiario y agente reciben respuestas minimizadas. | Cumplimiento |
| NFR-REL-01 | Una clave de idempotencia repetida 20 veces genera un solo efecto financiero. | Plataforma |
| NFR-REL-01A | Estado, ledger y auditoria se escriben en una sola transaccion ACID; una falla antes del commit deja todos los cambios sin efecto. | Plataforma |
| NFR-REL-02 | Una falla o timeout de proveedor entra a `ON_HOLD` o `DELIVERY_FAILED`, nunca a exito ni rechazo financiero automatico. | Plataforma |
| NFR-REL-03 | La confirmacion de retiro presencial es idempotente y requiere agente autenticado, codigo vigente y coincidencia de identidad. | Agente pagador |
| NFR-PER-01 | El p95 de cotizar y mostrar el resultado es menor o igual a 2 segundos con 100 usuarios concurrentes. | Plataforma |
| NFR-PER-02 | El p95 de consultar estado es menor o igual a 1 segundo con 10,000 remesas activas. | Plataforma |
| NFR-AVL-01 | Disponibilidad mensual de creacion y consulta mayor o igual a 99.5%, excluyendo mantenimiento anunciado. | Plataforma |
| NFR-AUD-01 | Cada cambio financiero conserva actor, timestamp, correlacion, estado anterior y nuevo estado. | Plataforma |
| NFR-PRV-01 | Solo se recolectan datos necesarios y se aplican retenciones documentadas por pais y finalidad. | Cumplimiento |
| NFR-USA-01 | 90% de usuarios representativos completa una remesa de prueba en menos de 5 minutos sin asistencia. | Producto |