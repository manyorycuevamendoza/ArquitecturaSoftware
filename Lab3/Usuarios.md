# Usuarios y actores

| Actor | Tipo | Responsabilidad |
| --- | --- | --- |
| Remitente | Usuario modelo directo | Crea, paga y consulta la remesa |
| Beneficiario | Usuario beneficiario | Recibe y confirma la entrega |
| Operador de cumplimiento | Rol interno del sistema | Control AML automatico y excepciones |
| Operador de soporte | Usuario interno | Atiende consultas sin alterar el ledger |
| Operador de SendIt | Usuario interno | Supervisa seguridad, consistencia, proveedores y operación del servicio |
| Agente pagador | Rol de Marta | Verifica al beneficiario y entrega efectivo |
| Proveedor de identidad | Sistema externo | Devuelve resultado de verificacion |
| Proveedor AML | Sistema externo | Evalua listas, limites y patrones de riesgo |
| Proveedor de pago | Sistema externo | Autoriza o rechaza el cobro |
| Red de entrega | Sistema externo | Confirma disponibilidad y entrega |

## Personas frente a roles

| Nombre de persona | Rol que representa | Es persona modelo? |
| --- | --- | --- |
| Ana | Remitente | Si |
| Luis | Beneficiario | Si |
| Marta | Operadora presencial / agente pagador | Si |

En los requisitos se usa el **rol** porque la regla debe aplicar a cualquier agente autorizado o a cualquier operador de cumplimiento. En las historias de usuario y diagramas de personas se usa el **nombre**: Ana, Luis y Marta son las únicas personas modelo de este caso. Marta representa al agente pagador presencial; los proveedores, soporte, administración y el control AML automatico son actores o roles, no personas modelo.

## Decisión sobre el usuario modelo

El remitente es el usuario modelo. Es quien concentra el objetivo de negocio, inicia la transaccion y debe comprender el resultado. El beneficiario es importante para el diseño de seguridad y notificaciones, pero no se usa como usuario modelo porque no inicia ni administra la remesa.

## Canales de uso

- **Aplicativo movil:** canal principal para crear la remesa, pagar y recibir notificaciones.
- **Pagina web:** canal alternativo con las mismas reglas de negocio y permisos.
- **Agente presencial:** canal de retiro; solo puede consultar una remesa habilitada y confirmar la entrega.