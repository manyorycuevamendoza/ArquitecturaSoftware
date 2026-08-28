# Requerimientos funcionales

`Actor que inicia` indica quién usa la capacidad. `Responsable` indica el rol de usuario que debe garantizar, operar o supervisar que el requisito se cumpla. Por eso Ana inicia el pago, pero el **Administrador de SendIt** supervisa la idempotencia, la validación de pertenencia y la consistencia financiera.

| ID | Requerimiento | Criterio de aceptacion | Actor que inicia | Responsable |
| --- | --- | --- | --- | --- |
| FR-REM-01 | El remitente podra crear una remesa con origen, destino, monto, moneda, beneficiario y medio de pago. | Un campo invalido impide enviar y explica el error; una solicitud valida recibe un `remittanceId` asociado al `senderId` autenticado. | Remitente | Remitente |
| FR-REM-02 | El sistema mostrara una cotizacion con tipo de cambio, comision, total debitado y monto recibido. | Recalcular la misma cotizacion con la misma version devuelve los mismos valores a dos decimales y la cotizacion queda ligada a la remesa. | Remitente | Administrador de SendIt |
| FR-REM-03 | El sistema validara identidad, limites y reglas de cumplimiento antes de cobrar. | Una remesa no validada no puede pasar a `PAYMENT_PENDING`; cada validacion conserva resultado, hora y `correlationId`. | Administrador de SendIt | Operador de cumplimiento |
| FR-REM-03A | El sistema evaluara señales de lavado de activos y sanciones antes de autorizar el pago. | Una alerta crea `ON_HOLD`, conserva las señales evaluadas y bloquea pago y retiro hasta una liberacion registrada. | Plataforma | Cumplimiento |
| FR-REM-04 | El pago y la confirmacion de la remesa seran idempotentes. | Repetir 20 veces la misma solicitud con una clave produce un solo cobro y una sola remesa; la clave solo puede reutilizarse con el mismo `senderId`, endpoint y hash de solicitud. | Remitente | Administrador de SendIt |
| FR-REM-05 | El sistema registrara el movimiento en un ledger y cambiara el estado de forma atomica. | No existe una remesa `COMPLETED` sin movimiento de debito, credito pendiente y evento de auditoria relacionados; una falla hace rollback de todo. | Administrador de SendIt | Administrador de SendIt |
| FR-REM-05A | El remitente podra cancelar una remesa antes de que el pago sea autorizado. | La cancelacion exige que el solicitante sea el `senderId`, cambia el estado a `CANCELLED`, libera la cotizacion y no crea debito ni retiro. | Remitente | Remitente |
| FR-REM-05B | El sistema impedira cancelar una remesa despues de confirmar el pago o el retiro. | Una cancelacion tardia es rechazada, conserva el estado financiero y registra el intento; una devolucion requiere un flujo autorizado separado. | Remitente | Administrador de SendIt |
| FR-REM-06 | El sistema notificara al beneficiario cuando la remesa este disponible. | Una notificacion duplicada no crea un segundo movimiento, puede reintentarse y nunca incluye señales AML ni datos financieros innecesarios. | Administrador de SendIt | Administrador de SendIt |
| FR-REM-06A | El beneficiario podra retirar presencialmente en un agente autorizado tipo Western Union. | El agente autenticado valida identidad, codigo de un solo uso, estado `AVAILABLE` y monto; la confirmacion idempotente mueve la remesa a `COMPLETED` una sola vez. | Beneficiario / Agente | Agente pagador |
| FR-REM-06B | El remitente y el beneficiario podran consultar el caso desde aplicativo movil o pagina web. | Ambos canales muestran el mismo estado de PostgreSQL; Ana solo consulta sus remesas y Luis solo las remesas donde es beneficiario. | Remitente / Beneficiario | Administrador de SendIt |
| FR-REM-07 | Remitente y soporte podran consultar el estado segun su relacion y rol. | Un usuario fuera del caso recibe denegacion, no obtiene datos por enumeracion de IDs y el intento queda auditado. | Remitente / Soporte | Administrador de SendIt |
| FR-REM-08 | El operador presencial podra confirmar el retiro despues de validar los datos del beneficiario. | Cada decision contiene agente autenticado, nombre y documento coincidentes, codigo vigente, hora, monto, estado anterior y nuevo estado; el agente no edita el ledger. | Operador presencial / agente pagador | Agente pagador |

## Estados principales

`DRAFT -> QUOTED -> COMPLIANCE_PENDING -> PAYMENT_PENDING -> PROCESSING -> AVAILABLE -> COMPLETED`.

Las salidas excepcionales son `REJECTED`, `ON_HOLD`, `PAYMENT_FAILED`, `DELIVERY_FAILED` y `CANCELLED`; no se debe saltar directamente a `COMPLETED`.