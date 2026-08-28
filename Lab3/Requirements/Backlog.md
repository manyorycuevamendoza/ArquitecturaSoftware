# Backlog de requerimientos - SendIt

Formato pedido por el enunciado: solo el titulo del requerimiento, claro y entendible. El detalle, los criterios de aceptacion y los responsables estan en [Functional.md](Functional.md) y [NonFunctional.md](NonFunctional.md).

## Backlog funcional

| ID | Titulo | Prioridad |
| --- | --- | --- |
| FR-REM-01 | Crear una remesa internacional | Alta |
| FR-REM-02 | Cotizar tipo de cambio, comision y monto que recibe el beneficiario | Alta |
| FR-REM-03 | Validar identidad del remitente antes de cobrar | Alta |
| FR-REM-03A | Evaluar señales de lavado de activos y listas de sanciones | Alta |
| FR-REM-04 | Pagar la remesa de forma idempotente | Alta |
| FR-REM-05 | Registrar el movimiento en el ledger de forma atomica | Alta |
| FR-REM-05A | Cancelar una remesa antes de autorizar el pago | Media |
| FR-REM-05B | Bloquear la cancelacion despues del pago o del retiro | Alta |
| FR-REM-06 | Notificar al beneficiario cuando el dinero este disponible | Media |
| FR-REM-06A | Retirar efectivo presencialmente en un agente autorizado | Alta |
| FR-REM-06B | Consultar la remesa desde aplicativo movil o pagina web | Media |
| FR-REM-07 | Restringir la consulta del caso segun rol y pertenencia | Alta |
| FR-REM-08 | Confirmar el retiro desde el portal del agente pagador | Alta |

## Backlog no funcional

| ID | Titulo | Prioridad |
| --- | --- | --- |
| NFR-SEC-01 | Cifrado de datos sensibles en transito y en reposo | Alta |
| NFR-SEC-02 | MFA para remitentes y operadores, con expiracion de sesion | Alta |
| NFR-SEC-03 | Ledger append-only para roles de aplicacion | Alta |
| NFR-SEC-04 | Visibilidad de datos AML e identidad restringida a cumplimiento | Alta |
| NFR-REL-01 | Un solo efecto financiero ante solicitudes repetidas | Alta |
| NFR-REL-01A | Estado, ledger y auditoria en una sola transaccion ACID | Alta |
| NFR-REL-02 | Falla de proveedor tratada como pendiente, nunca como exito o rechazo | Alta |
| NFR-REL-03 | Confirmacion de retiro presencial idempotente y autenticada | Alta |
| NFR-PER-01 | Cotizacion en 2 segundos o menos (p95) | Media |
| NFR-PER-02 | Consulta de estado en 1 segundo o menos (p95) | Media |
| NFR-AVL-01 | Disponibilidad mensual de 99.5% en creacion y consulta | Media |
| NFR-AUD-01 | Trazabilidad completa de cada cambio financiero | Alta |
| NFR-PRV-01 | Minimizacion de datos y retencion documentada por pais | Media |
| NFR-USA-01 | Envio de prueba completado sin asistencia en menos de 5 minutos | Media |
