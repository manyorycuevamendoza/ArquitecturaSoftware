# Requerimientos no funcionales

| ID | Requerimiento y verificación | Responsable |
| --- | --- | --- |
| NFR-NET-01 | Ante un corte de hasta 30 min, una descarga segmentada conserva el progreso de los bloques ya verificados y se reanuda automáticamente dentro de 5 min después de recuperar conectividad. | Plataforma |
| NFR-NET-02 | La sincronización usa HTTPS, compresión y solicitudes por rango; con un enlace de 1 Mbps no inicia multimedia opcional hasta que todos los recursos esenciales estén `READY`. | Nodo Escolar Local |
| NFR-INT-01 | Un paquete con firma o hash inválido no se activa y deja un registro con archivo y razón del rechazo. | Plataforma |
| NFR-INT-02 | El manifiesto, los bloques descargados y los eventos de sincronización son auditables con versión e identificadores; una nueva versión no mezcla archivos con la anterior. | Plataforma |
| NFR-AVL-01 | Durante un corte, el catálogo y la última versión `READY` permanecen accesibles para 30 clientes LAN; no se requiere que las funciones que dependen de Internet estén disponibles. | Nodo Escolar Local |
| NFR-PER-01 | Con 30 clientes LAN activos, el p95 para abrir la portada de una guía de hasta 5 MB es ≤ 3 s. | Nodo Escolar Local |
| NFR-COST-01 | Sobre un conjunto de al menos 30 solicitudes equivalentes, los tokens externos del AI Gateway son ≥ 40% menores que la línea base; se cuentan prompt y completion, incluido cualquier paso de IA adicional. | Plataforma |
| NFR-COST-02 | El 100% de invocaciones externas respeta los presupuestos configurados de entrada y salida o queda bloqueado antes de enviarse. | Plataforma |
| NFR-AUD-01 | Sincronizaciones e invocaciones IA son auditables con identificador, versión, actor, fecha y resultado; no se registra contenido sensible innecesario del estudiante. | Plataforma |
| NFR-SEC-01 | Solo los roles autorizados pueden publicar contenido, administrar un nodo o ver reportes de costo; los clientes LAN solo leen sus recursos permitidos. | Plataforma |
| NFR-USA-01 | Al probar con cinco docentes, al menos cuatro completan una solicitud IA válida o responden una aclaración sin asistencia y entienden el estado “pendiente de sincronización”. | Producto |

No se especifica una meta de disponibilidad total ni una segunda conexión. El diseño aprovecha el Internet existente, reduce datos transferidos y asegura continuidad local con la última versión verificada durante un corte.
