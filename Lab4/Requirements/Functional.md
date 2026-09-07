# Requerimientos funcionales

Cada requisito nace de un punto de decisión resuelto en
[../Diagrams/00-contexto-diagrama.md](../Diagrams/00-contexto-diagrama.md) y se
dibuja en los lienzos de [../Diagrams/Problema1/](../Diagrams/Problema1/README.md)
y [../Diagrams/Problema2/](../Diagrams/Problema2/README.md). La columna **Usuario responsable** dice de quién nace el requisito: qué persona
tiene la necesidad que lo justifica. Un requisito sin usuario detrás no es un
requisito, es una decisión técnica buscando excusa. La columna **PD** dice en qué
punto de decisión se resolvió.

## Problema 1: distribución con Internet intermitente

| ID | Requerimiento | Criterio de aceptación verificable | Usuario responsable | PD |
| --- | --- | --- | --- | --- |
| FR-DIS-01 | La central deberá publicar un manifiesto semanal por región, escuela, grado y curso, que describa el **estado completo** del curso a esa fecha y no las diferencias contra la semana anterior. | El manifiesto contiene `packageId`, semana, destino, versión curricular, lista completa de archivos vigentes, tamaño, hash SHA-256 y firma; no se publica sin esos campos. Un archivo publicado en una semana previa y todavía vigente sigue apareciendo en el manifiesto de la semana actual. | Valeria, coordinadora | PD-1, PD-4 |
| FR-DIS-02 | El Nodo Escolar Local deberá consultar por HTTPS el manifiesto y resolver cada archivo en uno de cuatro casos: nuevo, editado, sin cambio o retirado. | Frente a una versión nueva con un solo archivo cambiado, el registro muestra que descarga ese archivo y el manifiesto, y no vuelve a transferir archivos con el mismo hash. Un archivo presente en la caché que ya no figura en el manifiesto vigente se elimina de la caché y del catálogo local. | Rosa, docente rural | PD-1 |
| FR-DIS-03 | El Nodo Escolar Local deberá descargar archivos en segmentos reanudables y persistir su progreso. | Si una descarga se corta después de un bloque validado, al recuperar red solicita el siguiente rango pendiente y no vuelve a solicitar los bloques ya validados. El índice de bloques validados sobrevive a un reinicio del nodo. | Rosa, docente rural | PD-1 |
| FR-DIS-04 | El Nodo deberá priorizar recursos esenciales antes de multimedia opcional. | Con un límite de transferencia configurado, guía, ficha y actividad de la semana alcanzan estado `READY` antes de que inicie la descarga de video o audio opcional. | Diego, estudiante | PD-1 |
| FR-DIS-05 | El Nodo deberá verificar hash de cada archivo y firma del manifiesto antes de activar una versión nueva, y conservar la última versión válida si no puede completarla. | Un archivo con hash distinto al del manifiesto queda `REJECTED` y no se activa; una firma inválida rechaza el paquete completo. Durante un corte o una validación fallida, Rosa y Diego siguen viendo únicamente la última versión `READY`. Cuando no existe versión anterior `READY`, el nodo queda en estado explícito y emite alerta a Lima en lugar de servir contenido sin verificar. | Diego, estudiante | PD-2 |
| FR-DIS-06 | El sistema deberá encolar avances, incidencias y confirmaciones mientras no haya red y entregarlos una sola vez cuando vuelva. | Una incidencia creada durante un corte queda `PENDING_SYNC`; al recuperar conexión se entrega una vez al servidor y recibe confirmación identificada. El identificador se compone de escuela, contador local monótono y hash del contenido, y se fija al **crear** el evento, nunca al transmitirlo: un reintento envía el mismo identificador y no genera un segundo registro. La central aplica el evento y guarda su identificador en la misma transacción. | Diego, estudiante | PD-3, PD-6 |
| FR-DIS-07 | El Nodo deberá activar una versión nueva moviendo un puntero, no copiando archivos sobre la versión anterior. | Cada versión reside en su propio directorio y la versión servida se determina por un puntero. El orden de operaciones es descargar, verificar, mover el puntero y solo entonces liberar la versión anterior. Tras un corte de energía en cualquier instante, el nodo sirve la versión anterior completa o la nueva completa; no existe un estado observable que mezcle archivos de ambas. | Rosa, docente rural | PD-5 |
| FR-DIS-08 | El sistema deberá registrar dos marcas de tiempo por evento de retorno: la del nodo y la de la central. | Cada evento almacena `created_at`, puesto por el nodo, y `received_at`, puesto por la central al recibirlo. Los reportes y la auditoría ordenan por `received_at`; un nodo con el reloj desviado no altera el orden ni duplica el evento. | Valeria, coordinadora | PD-6 |
| FR-DIS-09 | El Nodo deberá poder pasar de cualquier versión previa a la más reciente sin aplicar las versiones intermedias. | Una escuela con tres semanas de atraso compara su manifiesto local contra el manifiesto más reciente publicado, descarga el acumulado resultante y activa directamente la versión más nueva. No se descargan versiones de archivos que una versión posterior ya reemplazó, ni se ejecutan activaciones intermedias. | Diego, estudiante | PD-4 |
| FR-DIS-10 | El Nodo deberá evaluar red, horario de clase y energía disponible antes de abrir una transferencia. | Sin señal utilizable no se intenta transferir y la clase continúa sirviéndose desde la caché local. Sin energía suficiente no se inicia la transferencia. En horario de clase la transferencia se ejecuta con tope de ancho de banda; si además la energía es insuficiente, no se ejecuta. | Rosa, docente rural | PD-7 |
| FR-DIS-11 | El Nodo deberá verificar el espacio disponible antes de descargar y liberar según una jerarquía fija cuando no alcance. | Si la versión nueva no cabe, se libera en este orden: multimedia opcional de versiones antiguas, luego versiones antiguas completas. Nunca se elimina la versión activa, la cola de eventos sin enviar ni el índice de bloques validados. Con la cola pendiente y el disco lleno, la cola se envía antes de liberar espacio. | Administrador regional | PD-8 |

## Problema 2: gobernanza del gasto en IA

| ID | Requerimiento | Criterio de aceptación verificable | Usuario responsable | PD |
| --- | --- | --- | --- | --- |
| FR-AI-01 | El docente deberá iniciar una solicitud de IA con un formulario intermedio, no con un cuadro libre obligatorio. | El formulario exige objetivo, grado, curso, tipo de recurso, duración y formato esperado; el texto libre es opcional y tiene límite visible. | Rosa, docente rural | PD-9 |
| FR-AI-02 | El AI Gateway deberá normalizar la solicitud en un archivo estructurado, clasificando cada dato para decidir si entra al prompt. | Cada dato se resuelve en una de cuatro clases: ruido, que se elimina; redundante, que ya viaja como campo del formulario y se elimina; acotable, del que entran solo los fragmentos pertinentes; e imprescindible, que entra literal. La solicitud almacenada conserva campos, plantilla y versión curricular; el prompt final no repite el temario completo ni texto descartado, y no arrastra el historial de la conversación. | Valeria, coordinadora | PD-11 |
| FR-AI-03 | Antes de invocar el modelo, el AI Gateway deberá evaluar en orden plantilla vigente, cuota disponible y campos obligatorios, y pedir aclaraciones específicas solo si falta información indispensable. | Sin plantilla vigente para el tipo de recurso y año no se construye el prompt y se avisa a la coordinadora. Si la cuota está agotada se informa **antes** de pedir cualquier aclaración. Si falta un campo crítico, devuelve como máximo tres preguntas concretas. Ninguno de estos pasos crea llamada al proveedor ni registro de tokens facturados. | Rosa, docente rural | PD-9 |
| FR-AI-04 | El AI Gateway deberá recuperar únicamente los fragmentos curriculares etiquetados como pertinentes. | Para una solicitud, el registro muestra IDs de fragmentos; el contexto inyectado no excede el límite configurado y no incluye documentos no seleccionados. Los IDs se registran para auditoría y no se envían además como texto dentro del prompt. | Valeria, coordinadora | PD-11 |
| FR-AI-05 | El AI Gateway deberá aplicar una plantilla por tipo de recurso y presupuestos de tokens de entrada **y** de salida, ambos obligatorios. | Cada llamada conserva `templateVersion`, presupuesto de entrada, presupuesto de salida y tokens reportados. Exceder el presupuesto de entrada intenta recortar contexto, nunca el objetivo; exceder el de salida recorta el formato pedido y vuelve a estimar. Si no se puede recortar, la llamada se bloquea antes de enviarse. | Valeria, coordinadora | PD-12 |
| FR-AI-06 | El sistema deberá reutilizar un resultado aprobado cuando la huella de la solicitud coincida, y deberá consultar la caché **antes** de evaluar el presupuesto. | La huella se calcula sobre plantilla, versión de plantilla, valores de campos, IDs de fragmentos, modelo y versión curricular. Una repetición equivalente devuelve el `generationId` existente y no invoca al proveedor, incluso sin conexión. Una huella cuya versión curricular ya no es la vigente no se entrega: se regenera. Una solicitud sin cuota cuya huella existe y está vigente se atiende desde la caché. | Valeria, coordinadora | PD-10 |
| FR-AI-07 | El sistema deberá registrar tokens de entrada, salida y costo estimado por solicitud, curso y escuela. | Toda llamada al proveedor, exitosa o fallida, tiene `requestId`, modelo, tokens, costo, versión y fecha. Las preguntas de aclaración, los aciertos de caché y los bloqueos por presupuesto registran cero tokens externos. | Valeria, coordinadora | PD-12 |
| FR-AI-08 | La coordinadora deberá ejecutar un reporte de reducción contra una línea base comparable. | Para el conjunto de prueba, el reporte calcula `(tokens_base - tokens_gateway) / tokens_base × 100`, identifica tareas no comparables y aprueba la meta solo si el resultado es ≥ 40%. Una tarea solo es comparable si coinciden tarea, modelo y versión curricular. | Valeria, coordinadora | PD-12 |
| FR-AI-09 | El docente deberá autenticarse antes de iniciar una solicitud de IA. | La sesión expone identificador de usuario, rol, escuela, cursos asignados y cuota vigente. Una solicitud sin identidad no se acepta, porque no se puede presupuestar, atribuir en el ledger ni auditar. | Valeria, coordinadora | PD-9 |
| FR-AI-10 | El sistema deberá conservar los prompts como plantillas versionadas en una biblioteca, no en la conversación del docente. | Cada plantilla guarda `prompt_id`, versión, texto canónico, campos obligatorios, presupuesto, autor, estado y versión curricular de origen. Publicar una plantilla nueva marca la anterior como histórica; ninguna se elimina, porque se necesita para auditar el gasto del periodo en que estuvo vigente. El Clarification Gate lee de la plantilla qué campos exige y no los infiere. | Valeria, coordinadora | PD-9 |
| FR-AI-11 | El sistema deberá encolar la solicitud lista cuando no haya conexión, reservando la cuota, y revalidarla al drenar la cola. | Una solicitud sin red queda `PENDING_NETWORK` con su cuota reservada, de modo que varias solicitudes encoladas no puedan exceder el presupuesto del periodo al enviarse juntas. Al recuperar conexión, cada solicitud recalcula su huella contra la versión curricular vigente y vuelve a pasar por campos, caché y presupuesto antes de invocar al proveedor: estar encolada no es una autorización de gasto. | Rosa, docente rural | PD-10, PD-12 |
| FR-AI-12 | Un bloqueo por presupuesto deberá devolver el control al docente y no reintentar automáticamente. | Cuando la solicitud no cabe en el presupuesto y no se puede recortar, el sistema explica qué reducir y no vuelve a intentar por su cuenta. El bloqueo se registra con cero tokens externos. | Rosa, docente rural | PD-12 |

## De quién nace cada requisito

La misma tabla leída al revés. Si una persona no tiene requisitos, no es una
persona del caso; si un requisito no tiene persona, es una decisión técnica sin
necesidad que la justifique.

| Persona | Lo que necesita | Requisitos que nacen de ahí |
| --- | --- | --- |
| **Rosa**, docente rural | Enseñar en la fecha en que toca, con o sin señal, y pedir material sin perder el tiempo ni gastar de más. | `FR-DIS-02`, `FR-DIS-03`, `FR-DIS-07`, `FR-DIS-10`, `FR-AI-01`, `FR-AI-03`, `FR-AI-11`, `FR-AI-12`, `NFR-NET-01`, `NFR-NET-03`, `NFR-INT-03`, `NFR-USA-01` |
| **Diego**, estudiante | Acceder al curso completo aunque Internet se caiga, y que su avance no se pierda ni se cuente dos veces. | `FR-DIS-04`, `FR-DIS-05`, `FR-DIS-06`, `FR-DIS-09`, `NFR-NET-02`, `NFR-INT-01`, `NFR-AVL-01`, `NFR-PER-01` |
| **Valeria**, coordinadora de contenidos | Publicar versiones correctas, auditar qué llegó a cada escuela y demostrar el ahorro en vez de prometerlo. | `FR-DIS-01`, `FR-DIS-08`, `FR-AI-02`, `FR-AI-04`, `FR-AI-05`, `FR-AI-06`, `FR-AI-07`, `FR-AI-08`, `FR-AI-09`, `FR-AI-10`, `NFR-NET-04`, `NFR-INT-02`, `NFR-COST-01..04`, `NFR-AUD-01/02`, `NFR-SEC-01` |
| **Administrador regional** | Dimensionar y supervisar el nodo de la escuela sin viajar hasta ella. | `FR-DIS-11`, `NFR-CAP-01`, `NFR-CAP-02` |

Los proveedores de almacenamiento y de IA no aparecen como responsables: son
sistemas externos, no tienen una necesidad propia dentro del caso.

### Los pain points que no dejamos sin cubrir

| Persona | Pain point del caso | Requisito que responde |
| --- | --- | --- |
| Rosa | La descarga reinicia desde cero en cada corte y nunca termina. | `FR-DIS-03`, `NFR-NET-01` |
| Rosa | Enseña con la guía nueva y la ficha vieja porque la activación quedó a medias. | `FR-DIS-07`, `NFR-INT-03` |
| Rosa | No puede abrir un recurso que ya está en el nodo porque la sincronización satura la red. | `FR-DIS-10`, `NFR-NET-03` |
| Rosa | Completa tres preguntas y recién ahí se entera de que no tiene cuota. | `FR-AI-03` |
| Diego | Pierde el material de las semanas en que la escuela estuvo sin señal. | `FR-DIS-09` |
| Diego | Su actividad queda registrada dos veces porque el envío se reintentó. | `FR-DIS-06`, `FR-DIS-08` |
| Diego | La escuela se queda sin material y nadie se entera. | `FR-DIS-05`, `NFR-INT-01` |
| Valeria | Sigue viendo temas que ya retiró del currículo. | `FR-DIS-02` |
| Valeria | No puede saber si el 40% de ahorro es real o un número inventado. | `FR-AI-08`, `NFR-COST-01`, `NFR-COST-03` |
| Valeria | No puede auditar en qué se gastó el presupuesto porque el prompt vivía en un chat. | `FR-AI-07`, `FR-AI-10` |
| Administrador regional | El nodo no puede activar nunca porque se dimensionó con el tamaño del paquete. | `NFR-CAP-01` |
| Administrador regional | El disco llega al 100% y ni siquiera se puede escribir el registro del fallo. | `NFR-CAP-02` |
