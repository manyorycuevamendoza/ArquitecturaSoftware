# Case Study #2 — Machinery Leasing in Peru

Software Architecture — UTEC — 2026-II

## Source

This laboratory is based on `Lab #2- Arqui2026.2.docx`. The assignment asks for the specification to be translated into English before development.

## Objective

Design and validate the architecture of a Peruvian machinery-leasing platform for companies that need equipment to execute projects but receive project payment only at completion.

## Deliverables

| Deliverable | Location | Status |
| --- | --- | --- |
| Translated assignment | [Assignment.md](Assignment.md) | Complete |
| Filled specification template | [SPEC-TEMPLATE.md](SPEC-TEMPLATE.md) | Complete |
| Personas | [Personas/](Personas/) | Complete |
| Functional and non-functional requirements | [Requirements/](Requirements/) | Complete |
| Evaluation close to or above 8/10 | [Spec/Results.md](Spec/Results.md) | Complete |
| Selected architecture | [Architecture.md](Architecture.md) | Complete |
| Running happy-path POC | [POC/](POC/) | Complete |

## Assumptions introduced by the team

The source document names Pedro, Carlos and Julia but does not define their roles. For this iteration:

- Pedro is the owner of an SME requesting machinery leasing.
- Carlos is a credit-risk analyst at the leasing company.
- Julia is a leasing-operations coordinator.

These assumptions must be validated with the instructor or product sponsor. They are not statements extracted from the assignment.

## Repository structure

```text
Lab2/
├── README.md
├── Assignment.md
├── SPEC-TEMPLATE.md
├── Architecture.md
├── Personas/
│   ├── Pedro.md
│   ├── Carlos.md
│   └── Julia.md
├── Requirements/
│   ├── Functional.md
│   └── NonFunctional.md
├── Spec/
│   ├── Eval-Spec.md
│   └── Results.md
└── POC/
    ├── package.json
    ├── index.html
    ├── src/
    │   ├── domain/
    │   ├── application/
    │   └── adapters/
    └── scripts/
```

## Recommended reading order

1. [Assignment](Assignment.md)
2. [SPEC TEMPLATE](SPEC-TEMPLATE.md)
3. [Personas](Personas/)
4. [Requirements](Requirements/)
5. [Evaluation](Spec/Results.md)
6. [Architecture](Architecture.md)
7. [POC](POC/README.md)
