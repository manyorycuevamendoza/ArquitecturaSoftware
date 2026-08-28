# Personas

El caso usa exactamente tres personas modelo. Los proveedores, el agente pagador, soporte y administración aparecen como actores o roles del sistema, pero no se modelan como personas adicionales.

| Persona | Rol | Canal principal | Necesidad principal |
| --- | --- | --- | --- |
| [Ana](Ana.md) | Remitente | Aplicativo y pagina web | Enviar dinero sin incertidumbre ni duplicados |
| [Luis](Luis.md) | Beneficiario | Aplicativo, pagina web y agente presencial | Recibir el monto correcto y retirarlo de forma segura |
| [Marta](Marta.md) | Operadora presencial / agente pagador | Portal del agente | Verificar los datos de Luis y entregar el efectivo |

## Cobertura de canales y acciones

| Capacidad | Ana | Luis | Marta |
| --- | --- | --- | --- |
| Crear remesa | Aplicativo / web | No aplica | No aplica |
| Pagar remesa | Aplicativo / web | No aplica | No aplica |
| Consultar estado | Aplicativo / web | Aplicativo / web | Portal interno |
| Retirar efectivo | No aplica | Presencial en agente autorizado | No aplica |
| Validar identidad y entregar efectivo | No | Presencial | Presencial en el agente |

Las tres personas cubren el flujo completo: Ana inicia y paga, Luis recibe y solicita el retiro, y Marta atiende presencialmente a Luis, valida sus datos y entrega el efectivo. El control AML es una regla del sistema; sus proveedores y revisores internos no se agregan como personas modelo.