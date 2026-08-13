# Caso de Estudio #1 — EsSalud: Sistema de Manejo de UCI

Arquitectura de Software — UTEC — 2026-II

## Equipo

| Rol        | Nombre            |
| ---------- | ----------------- |
| Integrante | Manyory Cueva     |
| Integrante | Gonzalo Rodriguez |
| Integrante | integrante        |

## Contenido del repositorio

| Documento                              | Descripción                                                          |
| -------------------------------------- | -------------------------------------------------------------------- |
| [Definición del Problema](Problema.md) | Contexto, problemáticas críticas y metas de escalamiento/rendimiento |
| [Usuarios y Clientes](Usuarios.md)     | Usuarios directos, clientes y stakeholders                           |
| [Personas](Personas/)                  | Un MD por usuario modelo (máx. 5)                                    |
| [Requerimientos](Requirements/)        | Funcionales y No Funcionales                                         |
| [Agentes](Agents/)                     | Definición de agente por persona                                     |
| [Spec](Spec/)                          | Agente evaluador `Eval-Spec.MD` y prompts de evaluación              |

## Estructura

```
Lab1/
├── README.md              # Este archivo (índice)
├── Problema.md            # Definición del problema
├── Usuarios.md            # Usuarios / Clientes
├── Personas/
│   ├── README.md
│   ├── Pablo.md           # Médico Internista
│   ├── Claudia.md         # Enfermera de UCI
│   ├── Roberto.md         # Administrador de Red Regional
│   ├── Elena.md           # Jefa de Gestión Clínica (EsSalud)
│   └── Manuel.md          # Paciente / Familiar (beneficiario)
├── Requirements/
│   ├── README.md
│   ├── ReqFunc.md
│   └── ReqNoFunc.md
├── Agents/
│   ├── README.md
│   ├── Agent-Pablo.md
│   ├── Agent-Claudia.md
│   ├── Agent-Roberto.md
│   ├── Agent-Elena.md
│   └── Agent-Manuel.md
└── Spec/
    ├── README.md          # Prompt usado para la evaluación
    ├── Eval-Spec.md       # Agente evaluador (devuelve % de calidad)
    └── Resultados.md      # Salida de la ejecución de los agentes
```

## Flujo de trabajo

1. Entender el contexto → `Problema.md`
2. Identificar usuarios/clientes → `Usuarios.md`
3. Definir usuarios modelo → `Personas/`
4. Crear agente por persona → `Agents/`
5. Definir requerimientos → `Requirements/`
6. Evaluar requerimientos con cada agente → `Spec/`
