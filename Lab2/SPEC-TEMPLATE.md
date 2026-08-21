# SPEC TEMPLATE — Machinery Leasing Platform

## Summary

This product is a digital machinery-leasing platform for Peruvian SMEs and corporate contractors. It allows an applicant company to request financing for machinery, obtain an explainable preliminary quote and continue to formal credit review. Internal leasing-company users evaluate risk and coordinate approved operations.

The POC demonstrates one end-to-end happy path: Pedro submits and accepts a preliminary quote, Carlos validates the required evidence and formally approves the case, and Julia records the supplier, contract reference and scheduled delivery date. Pedro then sees the completed progress and delivery information in the same case.

## Problem

Peruvian companies often win projects that require machinery before work can begin, but they receive most of the project payment only after completing milestones or delivering the project. Purchasing equipment upfront can consume the money needed for payroll, materials and operations, preventing a viable project from starting.

The current leasing process may also depend on meetings, email, spreadsheets and repeated document requests. Applicants cannot see eligibility or status quickly; credit analysts receive inconsistent information; and operations coordinators lack one reliable view of approved cases, ownership and next actions.

## Objective

Provide a single digital platform where a company can submit a machinery-leasing request, receive a preliminary quote, provide supporting evidence and follow the decision; internal staff must be able to evaluate risk, record a decision and coordinate the approved operation.

For the POC, success means completing one transparent digital happy path from application through formal credit approval to scheduled delivery, without real document validation, legal execution, supplier integration or physical delivery.

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
| Happy path | Eligible SME submits valid data, accepts a preliminary quote, receives formal credit approval and obtains a scheduled machinery-delivery date |

## Users and their needs

| User | Role | Primary needs |
| --- | --- | --- |
| [Pedro](Personas/Pedro.md) | SME owner / applicant | Know eligibility early, understand cost and avoid repeated paperwork |
| [Carlos](Personas/Carlos.md) | Credit-risk analyst | Receive complete, comparable evidence and explain every decision |
| [Julia](Personas/Julia.md) | Leasing-operations coordinator | Track approved cases, responsibilities and next steps without spreadsheets |

### Pedro.md

- **Organization:** Applicant SME — Constructora Andina SAC.
- **Meaning of the role:** Pedro represents the company that needs the machinery and requests the lease.
- **Product needs:** Fast preliminary eligibility, transparent financing terms, no repeated data entry, clear status and protection of company information.
- **Participation in the POC:** Pedro fills in the React form, sees the payment count and costs, accepts the preliminary quote and later sees Carlos's approval and Julia's delivery schedule in the same case.
- **Full persona:** [Pedro.md](Personas/Pedro.md)

### Carlos.md

- **Organization:** Leasing company.
- **Meaning of the role:** Carlos is the credit-risk analyst who evaluates evidence and decides whether the leasing company can formally accept the financial risk.
- **Product needs:** Complete and comparable applications, explainable policy results, evidence status, decision history and auditability.
- **Participation in the POC:** Carlos has a credit-review view. After Pedro accepts the quote, Carlos sees the same application and rule results, validates three simulated evidence items and records the formal approval reason.
- **Full persona:** [Carlos.md](Personas/Carlos.md)

### Julia.md

- **Organization:** Leasing company.
- **Meaning of the role:** Julia is the operations coordinator who takes a formally approved case and coordinates contract preparation, supplier contact and machinery delivery.
- **Product needs:** One case status, owner, next action, consistent approved terms and visibility of overdue work.
- **Participation in the POC:** Julia has an operations view. After Carlos approves the case, she reuses the approved data and records the supplier, contract reference and confirmed delivery date.
- **Full persona:** [Julia.md](Personas/Julia.md)

### Machinery supplier boundary

The machinery supplier is an external participant, not one of the three personas required by this iteration. In the POC, Julia records a simulated supplier confirmation and delivery date; the supplier has no login or view, and no real purchase or delivery occurs.

## Key product decisions

1. The POC uses Peruvian soles and an 11-digit RUC as the applicant identifier.
2. A preliminary decision is rule-based and explainable; it never represents final credit approval.
3. The POC has simulated views for Pedro, Carlos and Julia over the same application in one in-memory repository. Authentication and a transactional database belong to the pilot.
4. Missing or borderline evidence sends an application to manual review instead of silently rejecting it.
5. Every relevant state change records actor, time and reason.
6. The initial product supports one machinery item per application; machinery fleets are deferred.
7. Architecture is selected only after evaluating the requirements and personas.

## Expected user experience

- Pedro completes a guided request in less than five minutes and always sees whether the result is preliminary, pending formal review or formally approved.
- The estimate clearly separates equipment value, initial payment, financed amount, number of monthly payments, monthly installment and estimated totals.
- Carlos sees the exact data Pedro submitted, the same calculated quote, explicit rule results and a three-item evidence checklist.
- Julia sees only when the case is ready for operations, along with the approved terms, current owner and next required action.
- No user needs to re-enter information already accepted in an earlier step.
- Pedro sees the supplier and scheduled delivery date after Julia completes coordination.
- Every view displays the current status, owner, next action and chronological history.

## Main flows

### Happy path

1. Pedro enters company, machinery, project-capacity and requested-term data.
2. The system validates completeness and calculates an indicative installment.
3. The eligibility policy returns `PRE_APPROVED` with an explainable quote.
4. Pedro reviews the installment, number of payments and estimated totals, acknowledges that the quote is preliminary and accepts it.
5. The application moves to `FORMAL_REVIEW`, ready for Carlos to validate evidence.
6. Carlos sees the same request and rule results, validates the simulated RUC record, project contract and bank statements, and records an approval reason.
7. The application moves to `CREDIT_APPROVED`, owned by Julia.
8. Julia records the simulated supplier, contract reference and confirmed delivery date without re-entering Pedro's data.
9. The application moves to `DELIVERY_SCHEDULED`, and Pedro sees the formal decision, delivery details and complete timeline.

This is the complete scope of the implemented POC. `PRE_APPROVED` is not final approval; `CREDIT_APPROVED` is a simulated formal decision for demonstrating the workflow, not a binding contract or real authorization to purchase machinery. `DELIVERY_SCHEDULED` records a simulated coordination outcome, not physical delivery.

### Manual-review path

1. The request is structurally valid but one policy threshold is not met or requires evidence.
2. The system records the reason and moves the case to `MANUAL_REVIEW`.
3. Carlos opens the same review view, validates the simulated supporting evidence and records a decision.

### Rejection path

1. Mandatory identity or financing conditions are invalid.
2. The system rejects the request with specific, auditable reasons.

## Scope by stages

| Stage | Included |
| --- | --- |
| POC | One-item application; deterministic eligibility; detailed quote; simulated Pedro, Carlos and Julia views; formal approval; supplier/contract/delivery scheduling; shared timeline; and one in-memory repository |
| Pilot | Authentication and authorization, real document upload/validation, rejection and information-request decisions, persistent database, append-only audit and operational worklists |
| Production | Authorized external integrations, contract workflow, supplier settlement, observability, high availability, security hardening and validated capacity |

## Acceptance criteria

1. A valid happy-path request returns a preliminary quote and a decision in no more than 3 seconds under the POC test profile.
2. The quote displays equipment value, initial payment, financed amount, term and estimated monthly installment.
3. An invalid RUC, term or initial payment is rejected with a specific reason.
4. Accepting a pre-approved quote moves the same application to `FORMAL_REVIEW` exactly once and makes it actionable in Carlos's view.
5. The system does not present a preliminary quote as final approval or a binding contract.
6. Every decision includes the policy checks that passed or failed.
7. Carlos cannot approve the happy-path case until the three required evidence items are marked valid and an approval reason is entered.
8. Carlos's approval changes the same case to `CREDIT_APPROVED`, assigns it to Julia and preserves Pedro's original data and quote.
9. Julia cannot schedule delivery before credit approval and must record supplier, contract reference and delivery date.
10. Julia's completion moves the same case to `DELIVERY_SCHEDULED`, and Pedro can see the formal decision and delivery information.
11. The case history records Pedro's submission and acceptance, Carlos's approval and Julia's coordination in order.
12. Functional and non-functional requirements trace to at least one persona need.
13. Eval-Spec obtains at least 8/10 without hiding residual gaps.
14. The POC builds and its automated end-to-end self-test completes successfully.
