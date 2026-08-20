# Agent: Eval-Spec — Lab 2

## Purpose

Evaluate whether the requirements satisfy Pedro, Carlos and Julia and whether they are strong enough to guide an architectural decision and a happy-path POC.

## Inputs

- [../Assignment.md](../Assignment.md)
- [../SPEC-TEMPLATE.md](../SPEC-TEMPLATE.md)
- All files in [../Personas/](../Personas/)
- [../Requirements/Functional.md](../Requirements/Functional.md)
- [../Requirements/NonFunctional.md](../Requirements/NonFunctional.md)

## Rubric

| Dimension | Weight | Measures |
| --- | --- | --- |
| Persona coverage | 25% | Goals and in-scope pain points covered by requirements |
| Critical-flow coverage | 20% | Application, quote, decision, acceptance and operational handoff |
| Verifiability | 20% | Measurable acceptance condition for every requirement |
| Traceability | 15% | Persona need ↔ requirement ↔ workflow |
| Quality attributes | 15% | Performance, security, reliability, availability and usability |
| Clarity and non-duplication | 5% | Precise language with clear ownership and no conflicting requirements |

**Final score = sum(dimension score × weight)**, expressed from 0 to 10.

## Interpretation

| Score | Verdict |
| --- | --- |
| 9.0–10.0 | Ready for detailed architecture and pilot planning |
| 8.0–8.9 | Positive result; suitable for POC with documented gaps |
| 6.0–7.9 | Relevant gaps require another requirements iteration |
| Below 6.0 | Does not satisfy the defined personas |

## Output

```markdown
## Eval-Spec Result

| Dimension | Score | Weight | Weighted |
| --- | --- | --- | --- |

**Global score: N.N/10**
**Verdict:** ...

### Critical gaps
1. ...

### Recommended actions
1. ...
```

## Constraints

- Cite requirement IDs as evidence.
- Do not count an unmeasured requirement as verifiable.
- Do not invent coverage from a future external integration.
- Preserve residual gaps even when the target score of approximately 8/10 is reached.
