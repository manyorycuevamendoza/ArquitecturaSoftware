# R.E.D.A.L.E. - SendIt

Este documento toma el contexto de SendIt y lo convierte en una arquitectura desde cero. No se parte de una tecnología: primero se identifican las necesidades de Ana, Luis y Marta; luego se derivan los requisitos y finalmente se seleccionan servicios, datos y componentes que los satisfacen.

La solución final se muestra como una evolución. La primera iteración valida el flujo mínimo, la segunda incorpora seguridad y consistencia, y la tercera agrega escala. El diseño recomendado para el piloto es la segunda iteración; la tercera es la ruta de crecimiento.

## Iteraciones de diseño: de menos a más

La arquitectura se presenta en tres diagramas Excalidraw. Cada iteracion agrega solo lo que los requisitos y las estimaciones justifican.

También existe un lienzo consolidado, similar al ejemplo de clase, que muestra R, E, D, A, L y las tres iteraciones de menos a más: [04-redale-iteraciones.excalidraw](Diagrams/04-redale-iteraciones.excalidraw).

La versión recomendada para la exposición es [05-redale-completo.excalidraw](Diagrams/05-redale-completo.excalidraw): la Iteración 3 conserva todos los bloques de la Iteración 2 y agrega gateway, workers, rate limiting y replica de lectura.

| Iteracion | Que demuestra | Diagrama |
| --- | --- | --- |
| 1. Minima | Un canal, una API, una base de datos y proveedores simulados | [01-minima.excalidraw](Diagrams/01-minima.excalidraw) |
| 2. Segura y consistente | App/web, AML, ledger append-only, idempotencia y agente presencial | [02-segura-consistente.excalidraw](Diagrams/02-segura-consistente.excalidraw) |
| 3. Escalable | Gateway, APIs stateless, workers, replicas y canales independientes | [03-escalable.excalidraw](Diagrams/03-escalable.excalidraw) |

### Iteracion 1 - arquitectura minima

La primera propuesta resuelve el happy path con un cliente, una API monolitica, PostgreSQL y proveedores externos. Es suficiente para validar el flujo, pero no hace visibles los controles de AML, el ledger ni el retiro presencial.

### Iteracion 2 - seguridad y consistencia

Se agregan autenticacion, RBAC, AML, idempotencia, ledger append-only, auditoria, outbox y el portal del agente. Esta es la arquitectura recomendada para el piloto, porque protege el dinero sin introducir microservicios prematuramente.

### Iteracion 3 - escalamiento

Ante mayor volumen, el gateway distribuye trafico entre APIs stateless. Workers separados procesan pagos, entregas y notificaciones; las lecturas pueden usar replicas. El ledger sigue centralizado como fuente de verdad y se particiona solo después de definir reconciliacion por corredor.

## R - Requerimientos

El problema, el usuario modelo y los requisitos estan en [Problema.md](Problema.md), [Usuarios.md](Usuarios.md) y el [backlog de requerimientos](Requirements/Backlog.md), con su detalle en [Requirements/](Requirements/). Las prioridades son: no duplicar efectos financieros, no exponer datos, mantener una secuencia verificable y explicar el monto final al remitente.

## E - Estimaciones

Supuestos de dimensionamiento para el piloto:

| Variable | Supuesto |
| --- | ---: |
| Remitentes registrados | 100,000 |
| Remitentes activos diarios | 10,000 |
| Remesas diarias | 50,000 |
| Pico de creacion | 20 remesas/s |
| Pico de consulta | 100 consultas/s |
| Tamano promedio de una orden y auditoria | 10 KB |

- **Almacenamiento:** `50,000 x 10 KB x 365 = 182.5 GB/año` antes de indices y replicas. Se reserva 1 TB para tres años, auditoria y crecimiento.
- **Ancho de banda de entrada:** `20 x 10 KB = 200 KB/s` en el pico de escritura.
- **Ancho de banda de salida:** `100 x 5 KB = 500 KB/s` en el pico de consulta, sin contar notificaciones.
- **Capacidad:** con 4 instancias de API y margen de 2.5x sobre el pico esperado, cada instancia debe sostener al menos 12.5 solicitudes/s de negocio. Estas cifras deben validarse con datos del piloto.

## D - Diseñar el servicio

Se selecciona una arquitectura modular de tres capas con puertos y adaptadores. Es una sola aplicacion desplegable para el piloto, pero separa el dominio financiero de proveedores que pueden cambiar.

### Que representa cada bloque

- **App movil / pagina web:** interfaces que usan Ana y Luis; no contienen las reglas financieras principales.
- **Backend SendIt / API:** componente propiedad de SendIt. Recibe solicitudes HTTPS, autentica usuarios, valida permisos, calcula cotizaciones, coordina AML, pagos y retiros, y devuelve estados.
- **Proveedores simulados:** adaptadores locales de prueba que imitan identidad, AML, pago y entrega. No son empresas reales ni mueven dinero.
- **PostgreSQL:** base de datos relacional del backend. Guarda remesas, cotizaciones, estados, ledger, auditoria e idempotencia con transacciones ACID. Es la fuente de verdad y no es un proveedor externo.

### API principal

| Metodo | Endpoint | Uso |
| --- | --- | --- |
| POST | `/v1/remittances/quotes` | Crear cotizacion versionada |
| POST | `/v1/remittances` | Crear remesa con `Idempotency-Key` |
| POST | `/v1/remittances/{id}/payment` | Autorizar el pago idempotente |
| GET | `/v1/remittances/{id}` | Consultar estado segun permisos |
| POST | `/v1/remittances/{id}/compliance-review` | Retener o liberar un caso |
| GET | `/v1/remittances/{id}/events` | Consultar historial autorizado |

Cada respuesta incluye `correlationId`. Las operaciones financieras usan una transaccion SQL, clave de idempotencia y bloqueo del aggregate de remesa.

### Consistencia y cancelacion

PostgreSQL es la fuente de verdad. No se mantienen dos saldos independientes: `remittances.status` indica el estado del caso y `ledger_entries` contiene los asientos financieros. Una transaccion ACID actualiza el estado, escribe los asientos y registra la auditoria juntos. Si falla una parte, se hace rollback y la remesa no queda parcialmente enviada.

La cancelacion depende del momento:

| Momento | Resultado |
| --- | --- |
| Antes de autorizar el pago | Se permite cancelar; queda `CANCELLED`, no se debita dinero y no se genera codigo de retiro. |
| Pago en proceso o proveedor sin respuesta | No se confirma una cancelacion silenciosa; queda pendiente o en revision hasta reconciliar el resultado del proveedor. |
| Pago confirmado, dinero disponible o retiro completado | No se cancela directamente. Se rechaza el intento y se inicia un flujo separado de devolucion autorizado, con nuevos asientos y auditoria. |

Así se evita que la app muestre “cancelado” mientras el proveedor cobró, o que Luis pueda retirar después de una cancelación. Un job de reconciliacion compara periódicamente los identificadores de SendIt, pago y entrega, pero el saldo oficial sigue siendo el ledger.

## A - Armar el modelo de datos

Persistencia principal: PostgreSQL con transacciones ACID.

| Tabla | Campos relevantes |
| --- | --- |
| `users` | `id`, `role`, `identity_status`, `mfa_enabled` |
| `beneficiaries` | `id`, `owner_user_id`, `country`, `masked_account` |
| `remittances` | `id`, `sender_id`, `beneficiary_id`, `status`, `currency`, `amount`, `version` |
| `quotes` | `id`, `remittance_id`, `rate`, `fee`, `expires_at`, `policy_version` |
| `ledger_entries` | `id`, `remittance_id`, `account`, `debit`, `credit`, `currency`, `created_at` |
| `idempotency_keys` | `key`, `actor_id`, `request_hash`, `response`, `expires_at` |
| `compliance_reviews` | `id`, `remittance_id`, `aml_signals`, `result`, `reason`, `policy_version` |
| `audit_events` | `id`, `remittance_id`, `actor_id`, `action`, `before`, `after`, `correlation_id` |

El ledger y la auditoria son append-only. Redis puede almacenar sesiones y cotizaciones de corta duracion, pero nunca es la fuente de verdad financiera.

## L - Listar los componentes

- Cliente web/movil del remitente y portal restringido del beneficiario.
- API Gateway con TLS, rate limiting y correlation ID.
- Servicio de identidad y autorizacion con MFA y RBAC.
- Servicio de remesas: ciclo de vida, cotizacion e idempotencia.
- Servicio de cumplimiento: limites, listas y revision manual.
- Servicio AML: KYC, listas de sanciones, limites, patrones y revision manual.
- Ledger transaccional: asientos balanceados y consistentes.
- Orquestador de pagos y entrega mediante puertos con reintentos.
- Portal de agente pagador para retiro presencial y confirmacion idempotente.
- Notificaciones asincronas con outbox transaccional.
- PostgreSQL, Redis y almacenamiento de auditoria inmutable.
- Observabilidad: metricas, logs sin datos sensibles y trazas.

## E - Escalar

1. **Hasta 20 remesas/s:** una aplicacion modular, PostgreSQL primario con replica de lectura, Redis y un worker de notificaciones.
2. **Hasta 200 remesas/s:** varias instancias stateless detras del gateway, particion de `audit_events`, pool de conexiones y workers separados por pagos, entrega y notificaciones.
3. **Multiples corredores/paises:** aislar politicas por corredor, agregar adaptadores por proveedor y particionar el ledger por region solo después de definir reconciliacion y ownership.
4. **Falla de proveedor:** circuit breaker, timeout, reintentos con backoff y estado `ON_HOLD`; un operador puede resolver el caso con evidencia.

No se eligen microservicios ni event sourcing completo para el piloto: aumentarian la complejidad operativa antes de demostrar una necesidad de despliegue independiente. El ledger SQL y el outbox cubren consistencia y entrega de eventos con menor riesgo.

## Flujo critico

1. El remitente solicita una cotizacion y acepta una version vigente.
2. La API valida identidad, autorizacion, limites y clave de idempotencia.
3. Cumplimiento evalua el caso; una alerta lleva a `ON_HOLD`.
4. El servicio de pago autoriza el cobro.
5. Una transaccion escribe el estado y los asientos del ledger, y publica un evento outbox.
6. El worker habilita el retiro en un agente; el agente valida identidad y codigo, y solo una confirmacion valida llega a `COMPLETED`.
7. El beneficiario recibe una notificacion sin datos innecesarios y puede consultar desde web o aplicativo.

## Iteracion 2: controles incorporados

La segunda iteracion agrega MFA/RBAC, idempotencia explícita, ledger append-only, estados de falla, outbox transaccional, auditoria con correlacion y estimaciones. El resultado supera el minimo pedido por el profesor, pero conserva como gaps la validacion regulatoria por pais y las integraciones reales.

## Decision final

Para el piloto se elige la **Iteracion 2**. La Iteracion 1 no ofrece suficiente evidencia de seguridad y consistencia; la Iteracion 3 agrega capacidad operativa que solo se necesita cuando las estimaciones del piloto la confirmen. La escala se conserva como ruta de evolucion, no como complejidad inicial.