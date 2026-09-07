# Usuarios y actores

| Actor | Tipo | Responsabilidad |
| --- | --- | --- |
| Docente rural | Usuario modelo directo | Enseña con la caché local y solicita material asistido por IA. |
| Estudiante | Usuario beneficiario | Consulta y descarga el contenido semanal en la red local de la escuela. |
| Coordinadora de contenidos (Lima) | Usuario interno | Publica versiones curriculares y monitorea sincronizaciones y costo de IA. |
| Administrador regional | Rol interno | Configura y supervisa el Nodo Escolar Local; no publica contenido. |
| Proveedor de almacenamiento | Sistema externo | Expone por HTTPS los manifiestos y archivos versionados. |
| Proveedor de IA | Sistema externo | Recibe el prompt optimizado desde el AI Gateway y devuelve la generación. |

## Personas frente a roles

| Persona | Rol representado | Relación con el caso |
| --- | --- | --- |
| Rosa | Docente rural | Usuario modelo: necesita enseñar y producir material pese a cortes. |
| Diego | Estudiante | Beneficiario directo: necesita acceder al curso aunque Internet se caiga. |
| Valeria | Coordinadora de contenidos | Operadora: necesita publicar versiones correctas y controlar el presupuesto de IA. |

El administrador y los proveedores aparecen como roles o sistemas externos; no son personas modelo porque no concentran una necesidad primaria del caso.
