# Requerimientos no funcionales

| ID | Requerimiento y verificación | Responsable |
| --- | --- | --- |
| NFR-OFF-01 | La consulta de materiales publicados funciona con la interfaz WAN físicamente desconectada; la prueba abre catálogo, guía y actividad desde un cliente LAN. | Plataforma |
| NFR-INT-01 | Un paquete con firma o hash inválido no se publica y deja un registro con archivo y razón del rechazo. | Plataforma |
| NFR-INT-02 | El manifiesto y el paquete de retorno son inmutables una vez firmados; una nueva versión usa un identificador distinto. | Plataforma |
| NFR-PER-01 | Con 30 clientes LAN activos, el p95 para abrir la portada de una guía de hasta 5 MB es ≤ 3 s en la red de la escuela. | Nodo Escolar Local |
| NFR-PER-02 | La validación local de un paquete semanal de hasta 4 GB termina en ≤ 10 min en el hardware objetivo. | Nodo Escolar Local |
| NFR-COST-01 | Sobre un conjunto de al menos 30 solicitudes equivalentes, los tokens externos del AI Gateway son ≥ 40% menores que la línea base; se cuentan prompt y completion, incluido cualquier paso de IA adicional. | Plataforma |
| NFR-COST-02 | El 100% de invocaciones externas respeta los presupuestos configurados de entrada y salida o queda bloqueado antes de enviarse. | Plataforma |
| NFR-AUD-01 | Paquetes e invocaciones IA son auditables con identificador, versión, actor, fecha y resultado; no se registra el contenido sensible innecesario del estudiante. | Plataforma |
| NFR-SEC-01 | Solo los roles autorizados pueden publicar paquetes, importar contenido o ver reportes de costo; los clientes LAN solo leen sus recursos permitidos. | Plataforma |
| NFR-USA-01 | Al probar con cinco docentes, al menos cuatro completan una solicitud IA válida o responden una aclaración sin asistencia y entienden el estimado de alcance/costo mostrado. | Producto |

No se especifica una meta de alta disponibilidad ni tolerancia a fallas de entrega porque el enunciado la excluye en esta etapa. La corrección del curso se protege mediante verificación de integridad, no mediante conectividad remota.
