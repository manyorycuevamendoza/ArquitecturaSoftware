# Grupo 03 Brain

## Propósito

Este archivo conserva aprendizajes reutilizables del Grupo 03 para iniciar cada laboratorio con mejor contexto. No sustituye el enunciado ni contiene requisitos permanentes del producto: cada laboratorio debe validar nuevamente su problema, usuarios, alcance y atributos de calidad.

## Equipo

| Integrante |
| --- |
| Manyory Cueva |
| Jean Pier Angeles |
| Gonzalo Rodriguez |

## Aprendizajes verificados

### LAB-LEARN-01 — Requerimientos antes que arquitectura

- **Modifica:** el orden de trabajo; no se selecciona arquitectura antes de conocer objetivos, pain points, flujos críticos y requisitos no funcionales.
- **Origen:** Lab 1.
- **Evidencia:** la reevaluación de personas reveló necesidades que la primera decisión arquitectónica no había considerado.
- **Límite:** un prototipo exploratorio puede comenzar antes, pero no constituye una decisión arquitectónica final.

### LAB-LEARN-02 — Elegir la alternativa más sencilla que alcance la calidad requerida

- **Modifica:** la selección entre 3-tier, hexagonal, event-driven y microservicios.
- **Origen:** Lab 1.
- **Evidencia:** microservicios y eventos añadían distribución, bases y operación sin dominios autónomos que lo justificaran; 3-tier cubrió el proceso integrado de UCI.
- **Límite:** si otro caso demuestra despliegue independiente, escalamiento desigual o aislamiento obligatorio, deben reevaluarse microservicios o eventos.

### LAB-LEARN-03 — Varios roles no significan varias aplicaciones

- **Modifica:** el diseño de la capa de presentación; se prefiere una plataforma con vistas y permisos por rol cuando todos participan en el mismo proceso.
- **Origen:** Lab 1.
- **Evidencia:** médicos, enfermeras y administradores comparten pacientes, turnos y alertas sobre una fuente consistente.
- **Límite:** canales con capacidades incompatibles o públicos realmente independientes pueden requerir clientes diferentes.

### LAB-LEARN-04 — Un flujo crítico no debe competir con trabajo de menor prioridad

- **Modifica:** el tratamiento de emergencias y operaciones con plazo máximo.
- **Origen:** Lab 1.
- **Evidencia:** una alerta clínica no puede esperar detrás de una cola FIFO de eventos informativos.
- **Límite:** la mensajería sigue siendo válida si la prioridad, capacidad reservada y plazo de entrega están demostrados.

### LAB-LEARN-05 — Persona beneficiaria no equivale a rol operador

- **Modifica:** la trazabilidad; diferencia quién usa/administra una capacidad de quién recibe su valor.
- **Origen:** Lab 1.
- **Evidencia:** Manuel era beneficiario de continuidad y privacidad, pero no responsable de ejecutar requisitos del sistema.
- **Límite:** una persona puede ser simultáneamente beneficiaria y operadora si el caso lo define explícitamente.

### LAB-LEARN-06 — Pain points completos deben volver a evaluarse

- **Modifica:** el control de cobertura; cada ampliación de personas obliga a ejecutar nuevamente la evaluación.
- **Origen:** Lab 1.
- **Evidencia:** pasar a diez dolores por persona redujo la evaluación de 93.3% a 89.4% y reveló gaps nuevos.
- **Límite:** no se agregan requisitos por cada molestia; solo por necesidades dentro del alcance y con valor demostrable.

### LAB-LEARN-07 — Los términos deben ser comprensibles y verificables

- **Modifica:** la redacción; sustituye jerga innecesaria y expresiones vagas por comportamiento observable.
- **Origen:** Lab 1.
- **Evidencia:** “modo degradado” se aclaró como “cómo funciona el sistema cuando no hay conexión”; tiempos como “rápido” se convirtieron en segundos medibles.
- **Límite:** se conserva terminología técnica cuando es necesaria y se define para su audiencia.

### LAB-LEARN-08 — El estilo del código no obliga a distribuir el despliegue

- **Modifica:** la interpretación de alternativas; una arquitectura hexagonal puede implementarse como una sola aplicación y una sola base de datos.
- **Origen:** Lab 2.
- **Evidencia:** el POC en React aisló dominio, casos de uso y repositorio en memoria; su self-test y build de producción pasaron sin microservicios ni cola de eventos.
- **Límite:** hexagonal aporta valor cuando existen reglas centrales que deben aislarse de interfaces o proveedores cambiantes; no se selecciona solo para agregar carpetas.

### LAB-LEARN-09 — Un POC debe demostrar y limitar su afirmación

- **Modifica:** la entrega del prototipo; incluye una prueba ejecutable y declara qué capacidades productivas no demuestra.
- **Origen:** Lab 2.
- **Evidencia:** el self-test y el build verificaron `PRE_APPROVED → FORMAL_REVIEW → CREDIT_APPROVED → DELIVERY_SCHEDULED`, mientras el README diferencia decisiones simuladas de crédito real, contratos e integraciones.
- **Límite:** pasar el happy path no valida seguridad, capacidad, regulación ni escenarios de fallo de producción.

### LAB-LEARN-10 — El happy path debe cruzar todos los roles necesarios para producir el resultado

- **Modifica:** el alcance del POC; no termina en el primer handoff si el resultado esperado del negocio requiere decisiones posteriores de otros usuarios.
- **Origen:** Lab 2.
- **Evidencia:** la primera POC terminaba al asignar el caso a Carlos; la revisión del flujo exigió implementar las vistas de Carlos y Julia hasta dejar la entrega programada y visible para Pedro.
- **Límite:** un happy path end-to-end demuestra el recorrido exitoso, pero no obliga a implementar todas las excepciones, integraciones reales ni acciones físicas.

### LAB-LEARN-11 — Una regla bloqueante debe cortar consultas posteriores

- **Modifica:** el orden de integraciones de riesgo; primero se ejecuta la fuente bloqueante y solo un resultado limpio habilita consultas privadas o con costo.
- **Origen:** Lab 2.
- **Evidencia:** el self-test verifica que un RUC presente en la base negativa produce `CREDIT_REJECTED`, deja score, mora y atrasos como `NOT_EVALUATED` y no incrementa el contador del adaptador de bureau.
- **Límite:** una falla técnica del proveedor no equivale a un registro negativo; en un piloto debe generar revisión técnica o reintento, nunca rechazo crediticio automático.

## Checklist para iniciar un laboratorio

1. Leer el enunciado original completo y registrar el idioma solicitado.
2. Separar problema, objetivo, alcance, fuera de alcance y supuestos.
3. Definir usuarios y personas con necesidades distintas, no solo nombres distintos.
4. Redactar requisitos con ID, rol responsable y criterio verificable.
5. Evaluar cobertura antes de elegir arquitectura.
6. Comparar alternativas usando atributos de calidad y complejidad real.
7. Implementar y ejecutar el happy path mínimo del POC.
8. Registrar gaps y aprendizajes reutilizables.

## Registro de laboratorios

| Laboratorio | Caso | Estado del contexto |
| --- | --- | --- |
| Lab 1 | Gestión clínica y operativa de UCI | Lecciones incorporadas |
| Lab 2 | Leasing de maquinaria en Perú | Eval-Spec 9.1/10 y POC end-to-end ejecutado en tres vistas |

## Regla de actualización

Agrega una lección únicamente después de contar con evidencia dentro del repositorio. Evita duplicar requisitos, decisiones particulares o descripciones completas de los laboratorios.
