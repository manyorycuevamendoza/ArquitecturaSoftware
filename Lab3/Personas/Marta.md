# Marta - Operadora presencial / agente pagador

## Contexto

Marta trabaja en un agente autorizado de SendIt, similar a un local de Western Union. Es la operadora presencial: atiende a Luis, verifica sus datos y entrega el efectivo cuando la remesa esta disponible.

## Objetivos

- Verificar el nombre, documento de identidad y codigo de retiro de Luis.
- Confirmar que la remesa esta en estado `AVAILABLE`.
- Entregar el monto y moneda correctos una sola vez.
- Registrar la confirmacion del retiro sin modificar el saldo ni borrar auditoria.

## Pain points

1. Recibe solicitudes con nombres o documentos que no coinciden exactamente.
2. No quiere entregar efectivo si la remesa esta pendiente, retenida o cancelada.
3. Necesita confirmar que el codigo pertenece a esa remesa y no fue usado antes.
4. Le preocupa confirmar dos veces un retiro por una falla de red.
5. Debe distinguir entre una remesa disponible y una remesa ya completada.
6. Necesita ver el monto y la moneda correctos sin acceder a datos AML innecesarios.
7. Requiere autenticacion y permisos para demostrar que ella realizo la entrega.
8. Necesita instrucciones claras cuando el proveedor responde con timeout o error.
9. No puede modificar el saldo manualmente y necesita un flujo de correccion auditado.
10. Requiere un comprobante para entregar al beneficiario y cerrar la atencion.

## Necesidades del producto

Portal del agente con autenticacion, RBAC, validacion de identidad, codigo de un solo uso, estado `AVAILABLE` y auditoria append-only.

## Flujo representado

Marta busca el codigo de retiro, compara los datos de Luis con su documento, verifica el estado `AVAILABLE`, entrega el efectivo y confirma el retiro. La confirmacion es idempotente y ella nunca edita el saldo.