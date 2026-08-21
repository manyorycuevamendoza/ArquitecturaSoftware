# Functional Requirements

## Application intake

| ID | Requirement | Acceptance criterion | Responsible role |
| --- | --- | --- | --- |
| FR-APP-01 | The platform shall let an applicant create one machinery-leasing request containing company name, 11-digit RUC, machinery description, equipment value, initial-payment percentage, requested term, months in operation and expected monthly project cash flow. | A request missing any mandatory field is not submitted and each missing or invalid field is identified. A valid request receives a unique ID. | SME owner |
| FR-APP-02 | The platform shall preserve accepted application data across later stages so that users do not re-enter it. | After quote acceptance and formal-review transition, the company, project and machinery fields match the originally accepted values. | SME owner |

## Quote and preliminary decision

| ID | Requirement | Acceptance criterion | Responsible role |
| --- | --- | --- | --- |
| FR-QUO-01 | The platform shall calculate a preliminary quote showing equipment value, initial payment, financed amount, annual reference rate, number of monthly payments, estimated installment, estimated lease payments and estimated total including the initial payment. | For a fixed test case, every role view returns the same values rounded to two decimal places according to the versioned formula. | SME owner |
| FR-RSK-01 | The platform shall evaluate structural eligibility using versioned rules for RUC format, operating history, initial payment, term and installment-coverage ratio. | The result is `PRE_APPROVED`, `MANUAL_REVIEW` or `REJECTED` and contains the identifier, input and pass/fail outcome of every evaluated rule. | Credit-risk analyst |
| FR-RSK-02 | A structurally valid request that needs human judgment shall move to `MANUAL_REVIEW` instead of being silently rejected. | Each manual-review test records at least one explicit review reason and becomes visible in the analyst worklist. | Credit-risk analyst |
| FR-QUO-02 | The applicant shall be able to accept a `PRE_APPROVED` quote once, after acknowledging that it is preliminary and non-binding. | The first valid acceptance moves the case to `FORMAL_REVIEW`; repeated requests return the same state and do not create another case. | SME owner |

## Formal review and operations

| ID | Requirement | Acceptance criterion | Responsible role |
| --- | --- | --- | --- |
| FR-DOC-01 | The platform shall maintain a checklist for the RUC record, signed project contract and recent bank statements, including each evidence state. | A case cannot be marked ready for the happy-path formal approval while any of the three evidence items is not valid. | Credit-risk analyst |
| FR-DEC-01 | The analyst shall record approval, rejection or request-for-information with reason and policy version. | Every decision contains analyst, timestamp, outcome, reason and policy version; it is included in the case history. | Credit-risk analyst |
| FR-OPS-01 | Each active application shall display one current status, owner role and next required action. | For every workflow state in the acceptance suite, the platform returns exactly one permitted next action and responsible role. | Leasing-operations coordinator |
| FR-OPS-02 | Operations shall filter cases by status, owner, age and quote-expiration date. | Given seeded cases, every filter returns only matching records and identifies overdue cases. | Leasing-operations coordinator |
| FR-OPS-03 | The platform shall preserve versions when accepted financial terms or machinery data change. | A change creates a new version with actor, timestamp and reason; the prior accepted version remains readable. | Leasing-operations coordinator |
| FR-OPS-04 | After formal credit approval, operations shall record the machinery supplier, contract reference and confirmed delivery date on the same application. | Julia cannot coordinate a case before `CREDIT_APPROVED`; completing the three fields moves it to `DELIVERY_SCHEDULED` and exposes the coordination result to Pedro. | Leasing-operations coordinator |

## Access and traceability

| ID | Requirement | Acceptance criterion | Responsible role |
| --- | --- | --- | --- |
| FR-ACC-01 | The platform shall restrict applicant, credit and operational views according to authenticated role and case relationship. | All unauthorized access attempts in the security test are denied and recorded. | Platform administrator |
| FR-AUD-01 | The platform shall record creation, calculation, decision, acceptance, data change and access events with correlation to the application. | The case timeline reproduces every seeded event with actor, time, action, result and application ID, without gaps. | Platform administrator |

## Traceability summary

| Persona need | Requirements |
| --- | --- |
| Pedro — distinguish preliminary from formal approval and see the current owner (`P1`, `P4`, `P10`) | `FR-RSK-01`, `FR-QUO-02`, `FR-OPS-01`, `FR-DEC-01` |
| Pedro — understand payment count and complete cost (`P2`, `P3`) | `FR-QUO-01` |
| Pedro — avoid re-entry and follow the full case (`P6`, `P8`, `P9`) | `FR-APP-02`, `FR-OPS-01`, `FR-OPS-04`, `FR-AUD-01` |
| Carlos — receive one complete comparable case (`C1`, `C2`, `C3`, `C4`, `C6`) | `FR-APP-01/02`, `FR-QUO-01/02`, `FR-DOC-01` |
| Carlos — explain and trace the decision (`C5`, `C7`, `C9`, `C10`) | `FR-RSK-01/02`, `FR-DEC-01`, `FR-AUD-01` |
| Julia — receive only formally approved work with one owner (`J1`, `J2`, `J9`) | `FR-DEC-01`, `FR-OPS-01` |
| Julia — reuse approved data and record the operational outcome (`J3`–`J8`, `J10`) | `FR-APP-02`, `FR-OPS-03/04`, `FR-AUD-01` |

`P`, `C` and `J` refer to the numbered pain points in Pedro.md, Carlos.md and Julia.md.

## POC coverage boundary

The React POC implements `FR-APP-01/02`, `FR-QUO-01/02`, `FR-RSK-01`, the manual-review decision branch of `FR-RSK-02`, the valid-evidence and approval branch of `FR-DOC-01` and `FR-DEC-01`, `FR-OPS-01`, `FR-OPS-04`, and a visible in-memory case history that demonstrates part of `FR-AUD-01`.

The POC does not implement real document upload/validation, rejection or request-for-information decisions, operations worklist filters (`FR-OPS-02`), accepted-term versioning (`FR-OPS-03`), authentication/authorization (`FR-ACC-01`) or an append-only production audit store (`FR-AUD-01`).
