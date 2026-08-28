# Problema y alcance

## Problema

Las personas que envian dinero al extranjero necesitan una forma confiable de crear, pagar y consultar remesas. Un error de identidad, tipo de cambio, duplicacion o confirmacion puede causar perdida de dinero y reclamos difíciles de resolver.

## Objetivo

Permitir que un remitente cree una remesa internacional, conozca el costo y el monto que recibira el beneficiario, pague de forma segura y obtenga un comprobante trazable.

## Alcance del caso

- Registro y autenticacion del remitente.
- Validacion de identidad y controles contra fraude y lavado de activos como integraciones simuladas.
- Cotizacion con moneda origen, moneda destino, tipo de cambio, comision y monto recibido.
- Creacion idempotente de la orden.
- Pago, confirmacion y entrega simulada al beneficiario mediante retiro presencial en un agente autorizado tipo Western Union.
- Consulta del estado y notificaciones desde aplicativo movil y pagina web.
- Auditoria de cada cambio de estado.

## Fuera de alcance

La regulacion especifica de cada pais, la conexion real con bancos, tarjetas, billeteras y agentes pagadores, la custodia real de fondos y la implementacion de un motor antifraude productivo.

## Supuestos

El operador del servicio mantiene una cuenta transaccional o ledger como fuente de verdad. Los proveedores externos pueden responder con exito, rechazo o error tecnico; un error tecnico nunca se interpreta como un rechazo financiero definitivo.

## Canales y retiro

El remitente puede operar desde el aplicativo movil o la pagina web. El beneficiario puede retirar el dinero presencialmente en un agente autorizado, presentando identificacion y un codigo de retiro. El agente confirma identidad, disponibilidad y entrega; SendIt registra el resultado, pero no permite que el agente modifique el saldo.

## Lavado de activos

Antes de autorizar el pago, SendIt ejecuta controles de conocimiento del cliente, listas de sanciones, frecuencia y monto acumulado, paises de origen/destino y patrones inusuales. Una alerta no se convierte automaticamente en rechazo: pasa a `ON_HOLD` para revision de cumplimiento. El operador debe registrar la razon y la evidencia; los reportes regulatorios, cuando correspondan, no exponen informacion al remitente.