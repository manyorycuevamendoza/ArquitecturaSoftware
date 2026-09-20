# Arquitectura top-down y versión escalada con confiabilidad

> **Entregables:**
> [top-down editable en Excalidraw](../Diagrams/diagrama-top-down.excalidraw) y
> [arquitectura escalada con reliability](../Diagrams/diagrama-reliability.excalidraw).
> Los actores se identifican solo por su rol, según la indicación del docente.
> El lienzo usa cinco iteraciones top-down. Las primeras cuatro descubren
> contexto, registro, preaprobación y ejecución. La quinta reúne todos los
> servicios end-to-end sin escalar. El segundo lienzo aplica los mecanismos de
> escalamiento y confiabilidad sobre esa vista completa.

## Decisión

Implementar el happy path como un **monolito modular de tres capas**, desplegado
en una sola instancia y respaldado por una base de datos relacional. Los
portales de cliente y gerentes son vistas de una misma aplicación web con acceso
por rol.

Esta es la alternativa más simple para un proceso transaccional único: todos los
módulos trabajan sobre el mismo expediente y varias transiciones requieren
consistencia inmediata. La propuesta conserva límites internos claros sin
introducir la operación distribuida de microservicios.

## Alcance de la arquitectura

La arquitectura soporta exclusivamente el camino exitoso desde el registro de
la empresa hasta la entrega conforme. Incluye las integraciones y documentos
necesarios para ese camino, pero no intenta tolerar fallas, escalar carga ni
procesar incidencias de entrega en esta primera parte.

## Diagrama de contenedores y componentes

```mermaid
flowchart LR
    subgraph Roles[Roles del negocio]
        CLI[Empresa cliente]
        VEN[Gerente de Ventas]
        LOG[Gerente de Logística]
        FIN[Gerente de Finanzas]
    end

    subgraph Lease[Lea$e — despliegue único]
        WEB[Aplicación web<br/>vistas por rol]
        API[API / Controladores]

        subgraph MOD[Monolito modular]
            IAM[Acceso y roles]
            EMP[Empresas y validación]
            SOL[Solicitudes y preaprobación]
            APR[Aprobaciones y expediente]
            CON[Contratos]
            ORD[Órdenes y entregas]
            NOT[Notificaciones]
            AUD[Auditoría]
        end
    end

    DB[(Base de datos<br/>relacional)]
    DOC[(Almacenamiento privado<br/>de documentos)]
    SUNAT[SUNAT]
    CREDIT[Servicio de historial<br/>crediticio]
    SUP[Sistema del proveedor]
    MAIL[Servicio de correo]

    CLI --> WEB
    VEN --> WEB
    LOG --> WEB
    FIN --> WEB
    WEB --> API
    API --> IAM
    API --> EMP
    API --> SOL
    API --> APR
    API --> CON
    API --> ORD

    EMP --> SUNAT
    EMP --> CREDIT
    SOL --> SUP
    ORD --> SUP
    CON --> DOC
    ORD --> DOC

    EMP --> DB
    SOL --> DB
    APR --> DB
    CON --> DB
    ORD --> DB
    IAM --> DB

    EMP --> AUD
    SOL --> AUD
    APR --> AUD
    CON --> AUD
    ORD --> AUD
    AUD --> DB

    EMP --> NOT
    SOL --> NOT
    APR --> NOT
    CON --> NOT
    ORD --> NOT
    NOT --> MAIL
```

## Responsabilidades

| Componente | Responsabilidad en el happy path |
| --- | --- |
| Aplicación web | Presenta formularios y bandejas según el rol; muestra estado, siguiente acción y expediente. |
| API / Controladores | Recibe solicitudes, valida formato y delega cada operación al módulo correspondiente. |
| Acceso y roles | Autentica a los usuarios y autoriza las acciones de cliente, Ventas, Logística y Finanzas. |
| Empresas y validación | Registra la empresa, consulta SUNAT e historial crediticio y conserva el perfil validado. |
| Solicitudes y preaprobación | Crea la solicitud, consulta disponibilidad, valida capacidad, calcula propuesta y ordena proveedores. |
| Aprobaciones y expediente | Aplica el orden de aprobaciones y consolida las decisiones de los tres gerentes. |
| Contratos | Genera las versiones preliminar y definitiva y registra la aceptación del cliente. |
| Órdenes y entregas | Activa la orden, registra la fecha confirmada, el acta y la conformidad. |
| Notificaciones | Envía correo después de cada cambio de estado confirmado. |
| Auditoría | Registra actor, acción, fecha, estado anterior, estado nuevo y motivo. |
| Base de datos relacional | Es la fuente de verdad para empresa, solicitud, aprobaciones, contrato, orden, entrega y auditoría. |
| Almacenamiento de documentos | Guarda contrato preliminar, contrato definitivo y acta; la base conserva sus metadatos y referencias. |

## Flujo interno

```mermaid
flowchart TD
    A[Registrar empresa] --> B[Validar SUNAT]
    B --> C[Validar historial crediticio]
    C --> D[Guardar perfil validado]
    D --> E[Crear solicitud]
    E --> F[Consultar disponibilidad]
    F --> G[Validar capacidad financiera]
    G --> H[Rankear proveedores]
    H --> I[Generar preaprobación]
    I --> J[Aprobación de Ventas]
    J --> K[Aprobación de Logística]
    K --> L[Aprobación de Finanzas]
    L --> M[Generar contrato definitivo]
    M --> N[Registrar aceptación]
    N --> O[Activar orden al proveedor]
    O --> P[Confirmar entrega]
    P --> Q[Registrar acta]
    Q --> R[Registrar conformidad]
```

En la línea base de las iteraciones 2–5, las llamadas a SUNAT, historial
crediticio, proveedor y correo son síncronas. Cada operación que cambia un estado actualiza el
expediente y agrega su auditoría dentro de una misma transacción local. Una vez
confirmada esa transacción, el módulo de notificaciones envía el correo. La
Iteración 5 solo consolida el flujo completo; outbox, broker y workers se
incorporan después, en el diagrama de reliability.

## Datos principales

| Entidad | Datos mínimos |
| --- | --- |
| Empresa | RUC, razón social, contacto, estado SUNAT, resultado crediticio y fecha de validación. |
| Solicitud | Empresa, productos, cantidades, monto, estado, proveedor candidato y fechas. |
| Evaluación | Capacidad financiera, propuesta preliminar y ranking versionado de proveedores. |
| Aprobación | Tipo, gerente, decisión, comentario y fecha. |
| Contrato | Versión, condiciones de pago, cuotas, entrega, proveedor, documento y aceptación. |
| Orden de compra | Proveedor, productos, fecha de activación, fecha confirmada y estado. |
| Entrega | Acta, receptor, fecha, fin de ventana de 48 horas y conformidad. |
| Evento de auditoría | Caso, actor, acción, estados anterior/nuevo y marca de tiempo. |

## Reglas de consistencia del happy path

1. Una solicitud referencia una empresa previamente validada.
2. Las aprobaciones pertenecen a roles distintos y se aplican en el orden
   Ventas → Logística → Finanzas.
3. El contrato definitivo usa exactamente el proveedor, plazo y plan de cuotas
   aprobados en el expediente.
4. La aceptación del contrato y la activación de la orden son transiciones
   separadas; no existe orden activa sin contrato aceptado.
5. El acta pertenece a una orden entregada y la conformidad debe registrar si
   ocurrió dentro de la ventana de 48 horas.
6. Cada cambio de estado se guarda junto con su evento de auditoría en una
   transacción de la base de datos.

## Decisiones de la línea base

| Alternativa | Motivo para no usarla aún |
| --- | --- |
| Microservicios | El happy path comparte un expediente y no demuestra necesidad de despliegue o escalamiento independiente. |
| Arquitectura orientada a eventos | La primera versión busca mostrar un flujo secuencial y una respuesta inmediata. |
| Varias bases por dominio | Complican la consistencia de aprobación, contrato y orden sin aportar valor al ejercicio individual. |
| Procesamiento por colas | No forma parte de la línea base top-down; se agrega recién en la arquitectura de reliability. |

## Límites deliberados de las iteraciones 1–5

| Límite | Consecuencia |
| --- | --- |
| Una instancia de aplicación | Su caída detiene todos los canales y roles. |
| Una base de datos | Es un punto único de falla y de capacidad. |
| Integraciones síncronas | La lentitud o caída de SUNAT, riesgo o proveedor bloquea la operación. |
| Correo síncrono | Una falla del correo puede retrasar la respuesta al usuario. |
| Un almacenamiento documental | Su indisponibilidad impide generar o consultar contratos y actas. |
| Sin reintentos ni circuit breaker | Los errores transitorios se devuelven directamente al usuario. |
| Sin cola ni outbox | No se garantiza la entrega diferida de notificaciones u órdenes externas. |
| Sin réplicas ni balanceador | No hay continuidad ante falla ni distribución de carga. |

Estos límites forman la línea base completa representada por la Iteración 5.

## Iteración 5 — End-to-end consolidado, sin escalar

La última iteración contiene el flujo completo, no solo el segmento de
aprobaciones: `LoginService` → registro y validación → solicitud y
preaprobación → aprobaciones → contrato → orden → entrega → conformidad o
incidencia.

La secuencia termina en una salida explícita tanto para `SÍ` como para `NO`.
Cada transición de estado baja a un único flujo transversal:
`StateTransitionService` → `AuditService` → `Leasing DB` → `COMMIT OK` →
`NotificationService` → `Email API` → empresa cliente. Así se hace visible en
qué momento se guarda, cuándo termina la transacción y cuándo se envía el
correo. En esta iteración existe una instancia de aplicación, una base lógica y
una sola `Email API`.

## Arquitectura escalada con reliability

El segundo diagrama toma el E2E consolidado como punto de partida. No es una
sexta iteración del top-down: es la arquitectura de la Parte 3, donde se agregan
capacidad, redundancia y tolerancia a fallas.

| Riesgo de la línea base | Respuesta de la arquitectura escalada |
| --- | --- |
| Una instancia de aplicación | Load balancer y `App Instances N+1` stateless con health checks. |
| Base de datos como SPOF | `Leasing DB Primary`, standby con failover, read replica y backups con PITR probado. |
| Pérdida de notificaciones | Outbox en la misma transacción, broker persistente y workers N+1. |
| Duplicación por reintentos | `IdempotencyService` conserva la identidad de la operación. |
| Dependencias lentas o caídas | Timeout, retry acotado con exponential backoff y jitter, y circuit breaker. |
| Una falla consume todos los recursos | Bulkheads separados para validaciones, proveedor y notificaciones. |
| Auditoría separada del cambio | Estado, auditoría y outbox se confirman en el mismo commit. |
| Almacenamiento documental único | `Document Store N+1` con versionado. |
| Fallas invisibles | Métricas, logs, traces, liveness y readiness. |

### Aplicación de las técnicas vistas

| Técnica | Aplicación concreta |
| --- | --- |
| Health Endpoints | Cada réplica expone `/health/live` y `/health/ready`; el balanceador solo enruta a instancias `READY`. |
| Load Balancing | Distribuye solicitudes entre instancias stateless N+1 y retira del pool las no saludables. |
| Retries & Exponential Backoff | Reintentos limitados, con jitter, únicamente ante errores transitorios y operaciones seguras o idempotentes. |
| Circuit Breaker | Tres circuitos independientes protegen SUNAT/crédito, proveedor y correo; pasan por `CLOSED`, `OPEN` y `HALF-OPEN`. |
| Bulkheads & aislamiento de fallas | Cada grupo externo tiene su propio pool de hilos y conexiones; una caída del correo no agota los recursos de las validaciones. |
| Degradación elegante | Una dependencia obligatoria caída deja el trámite `PENDIENTE`; nunca fabrica un rechazo ni activa una orden sin confirmación. |
| Chaos Engineering | Experimentos controlados detienen una réplica, abren un circuito, pausan un broker o fuerzan el failover de la base. |

La degradación preserva un estado honesto: si falla SUNAT o crédito, el registro
queda pendiente; si falla el proveedor, la solicitud u orden no avanza; si
falla el correo, el cambio de negocio permanece confirmado y la notificación
queda en outbox/broker para reintento. Los experimentos de chaos se ejecutan
con condiciones de aborto y se validan mediante SLO, alertas y runbooks.

## Evidencia esperada para validar la Parte 1

- Demostrar una solicitud que recorra todos los estados hasta `CONFORME`.
- Medir las dos validaciones rápidas y comprobar que cada una responde en menos
  de 3 segundos bajo las condiciones del ejercicio.
- Verificar que los tres gerentes ven el mismo expediente y aprueban con su
  propio rol.
- Comprobar que la orden no se envía antes de la aceptación del contrato.
- Consultar la línea de tiempo completa y los documentos asociados al cerrar el
  caso.
