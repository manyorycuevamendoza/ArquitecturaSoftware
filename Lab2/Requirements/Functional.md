# Functional Requirements

## Application intake

| ID | Requirement | Acceptance criterion | Responsible role |
| --- | --- | --- | --- |
| FR-APP-01 | The platform shall let an applicant create one machinery-leasing request containing company name, 11-digit RUC, machinery description, equipment value, initial-payment percentage, requested term, months in operation and expected monthly project cash flow. | A request missing any mandatory field is not submitted and each missing or invalid field is identified. A valid request receives a unique ID. | SME owner |
| FR-APP-02 | The platform shall preserve accepted application data across later stages so that users do not re-enter it. | After quote acceptance and formal-review transition, the company, project and machinery fields match the originally accepted values. | SME owner |

## Quote and preliminary decision

| ID | Requirement | Acceptance criterion | Responsible role |
| --- | --- | --- | --- |
| FR-QUO-01 | The platform shall calculate a preliminary quote showing equipment value, initial payment, financed amount, annual reference rate, term and estimated monthly installment. | For a fixed test case, every channel returns the same values rounded to two decimal places according to the versioned formula. | SME owner |
| FR-RSK-01 | The platform shall evaluate structural eligibility using versioned rules for RUC format, operating history, initial payment, term and installment-coverage ratio. | The result is `PRE_APPROVED`, `MANUAL_REVIEW` or `REJECTED` and contains the identifier, input and pass/fail outcome of every evaluated rule. | Credit-risk analyst |
| FR-RSK-02 | A structurally valid request that needs human judgment shall move to `MANUAL_REVIEW` instead of being silently rejected. | Each manual-review test records at least one explicit review reason and becomes visible in the analyst worklist. | Credit-risk analyst |
| FR-QUO-02 | The applicant shall be able to accept a `PRE_APPROVED` quote once, after acknowledging that it is preliminary and non-binding. | The first valid acceptance moves the case to `FORMAL_REVIEW`; repeated requests return the same state and do not create another case. | SME owner |

## Formal review and operations

| ID | Requirement | Acceptance criterion | Responsible role |
| --- | --- | --- | --- |
| FR-DOC-01 | The platform shall maintain a checklist of required evidence and its state: missing, submitted, valid or rejected. | A case cannot be marked ready for final decision while mandatory evidence is missing or rejected. | Credit-risk analyst |
| FR-DEC-01 | The analyst shall record approval, rejection or request-for-information with reason and policy version. | Every decision contains analyst, timestamp, outcome, reason and policy version; it is included in the case history. | Credit-risk analyst |
| FR-OPS-01 | Each active application shall display one current status, owner role and next required action. | For every workflow state in the acceptance suite, the platform returns exactly one permitted next action and responsible role. | Leasing-operations coordinator |
| FR-OPS-02 | Operations shall filter cases by status, owner, age and quote-expiration date. | Given seeded cases, every filter returns only matching records and identifies overdue cases. | Leasing-operations coordinator |
| FR-OPS-03 | The platform shall preserve versions when accepted financial terms or machinery data change. | A change creates a new version with actor, timestamp and reason; the prior accepted version remains readable. | Leasing-operations coordinator |

## Access and traceability

| ID | Requirement | Acceptance criterion | Responsible role |
| --- | --- | --- | --- |
| FR-ACC-01 | The platform shall restrict applicant, credit and operational views according to authenticated role and case relationship. | All unauthorized access attempts in the security test are denied and recorded. | Platform administrator |
| FR-AUD-01 | The platform shall record creation, calculation, decision, acceptance, data change and access events with correlation to the application. | The case timeline reproduces every seeded event with actor, time, action, result and application ID, without gaps. | Platform administrator |

## Traceability summary

| Persona need | Requirements |
| --- | --- |
| Pedro — fast eligibility and transparent cost | `FR-APP-01`, `FR-QUO-01`, `FR-RSK-01`, `FR-QUO-02` |
| Pedro — no repeated data and clear status | `FR-APP-02`, `FR-OPS-01`, `FR-AUD-01` |
| Carlos — complete and comparable review | `FR-APP-01`, `FR-DOC-01`, `FR-RSK-01/02` |
| Carlos — explainable and traceable decisions | `FR-DEC-01`, `FR-AUD-01`, `FR-OPS-03` |
| Julia — owner, next step and overdue visibility | `FR-OPS-01/02` |
| Julia — consistent approved terms | `FR-APP-02`, `FR-OPS-03`, `FR-AUD-01` |
