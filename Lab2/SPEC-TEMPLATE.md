# Product Specification — Machinery Leasing Platform

## Problem summary

Peruvian SMEs and corporate contractors need machinery before a project starts, while their principal project revenue may arrive only after delivery. Paying for equipment upfront can exhaust working capital and prevent otherwise viable projects from beginning. The leasing company also needs reliable evidence, repeatable credit rules and operational traceability before purchasing equipment on the applicant's behalf.

## Objective

Provide a single digital platform where a company can submit a machinery-leasing request, receive a preliminary quote, provide supporting evidence and follow the decision; internal staff must be able to evaluate risk, record a decision and coordinate the approved operation.

For the POC, success means completing one transparent happy path from application to accepted preliminary quote without real financial or legal execution.

## Out of scope

- Disbursement of real funds or payment to machinery suppliers.
- Legally binding electronic signatures.
- Integration with tax, identity, credit-bureau, banking or insurance providers.
- Physical delivery, GPS tracking, maintenance and recovery of machinery.
- Collections, delinquency management and repossession.
- Final regulatory or legal compliance certification.
- Automatic final credit approval; the POC provides preliminary eligibility only.

## Key product concepts

| Concept | Definition |
| --- | --- |
| Applicant company | Peruvian legal entity requesting the lease, identified by RUC |
| Lease application | Request linking the company, project, machinery, supplier and financing terms |
| Machinery item | Equipment to be acquired by the lessor and used by the applicant |
| Initial payment | Applicant contribution expressed as a percentage of equipment value |
| Preliminary quote | Estimated financed amount, term and monthly installment; it is not a binding offer |
| Risk review | Assessment of business history, project cash flow, evidence and payment capacity |
| Lease decision | Pre-approved, manual review or rejected outcome with recorded reasons |
| Happy path | Eligible SME submits valid data, obtains a preliminary quote and accepts it for formal review |

## Users and their needs

| User | Role | Primary needs |
| --- | --- | --- |
| [Pedro](Personas/Pedro.md) | SME owner / applicant | Know eligibility early, understand cost and avoid repeated paperwork |
| [Carlos](Personas/Carlos.md) | Credit-risk analyst | Receive complete, comparable evidence and explain every decision |
| [Julia](Personas/Julia.md) | Leasing-operations coordinator | Track approved cases, responsibilities and next steps without spreadsheets |

## Key product decisions

1. The POC uses Peruvian soles and an 11-digit RUC as the applicant identifier.
2. A preliminary decision is rule-based and explainable; it never represents final credit approval.
3. The platform has role-based views over one application and one source of transactional data.
4. Missing or borderline evidence sends an application to manual review instead of silently rejecting it.
5. Every relevant state change records actor, time and reason.
6. The initial product supports one machinery item per application; machinery fleets are deferred.
7. Architecture is selected only after evaluating the requirements and personas.

## Expected user experience

- Pedro completes a guided request in less than five minutes and sees field-level validation.
- The estimate clearly separates equipment value, initial payment, financed amount, term and monthly installment.
- Carlos sees the same mandatory fields in the same order for every application and receives explicit rule results.
- Julia sees the current owner, status and next required action for each approved case.
- No user needs to re-enter information already accepted in an earlier step.
- Status names use plain language and explain what happens next.

## Main flows

### Happy path

1. Pedro enters company, machinery, project-capacity and requested-term data.
2. The system validates completeness and calculates an indicative installment.
3. The eligibility policy returns `PRE_APPROVED` with an explainable quote.
4. Pedro reviews and accepts the quote.
5. The application moves to `FORMAL_REVIEW`, ready for Carlos to validate evidence.
6. Julia can identify the case status and next responsible role.

### Manual-review path

1. The request is structurally valid but one policy threshold is not met or requires evidence.
2. The system records the reason and moves the case to `MANUAL_REVIEW`.
3. Carlos requests or validates supporting documents and records a decision.

### Rejection path

1. Mandatory identity or financing conditions are invalid.
2. The system rejects the request with specific, auditable reasons.

## Scope by stages

| Stage | Included |
| --- | --- |
| POC | One-item application, deterministic eligibility, preliminary quote, quote acceptance, in-memory repository and one customer-facing happy path |
| Pilot | Authentication, role views, document evidence, analyst review, persistent database, audit and operational dashboard |
| Production | Authorized external integrations, contract workflow, supplier settlement, observability, high availability, security hardening and validated capacity |

## Acceptance criteria

1. A valid happy-path request returns a preliminary quote and a decision in no more than 3 seconds under the POC test profile.
2. The quote displays equipment value, initial payment, financed amount, term and estimated monthly installment.
3. An invalid RUC, term or initial payment is rejected with a specific reason.
4. Accepting a pre-approved quote moves the application to `FORMAL_REVIEW` exactly once.
5. The system does not present a preliminary quote as final approval or a binding contract.
6. Every decision includes the policy checks that passed or failed.
7. Functional and non-functional requirements trace to at least one persona need.
8. Eval-Spec obtains at least 8/10 without hiding residual gaps.
9. The POC builds and its automated self-test completes successfully.
