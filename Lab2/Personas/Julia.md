# Julia — Leasing-Operations Coordinator

> Focus: Move approved cases to contract and delivery without losing ownership

## Profile

| Field | Value |
| --- | --- |
| Name | Julia Torres Valdivia |
| Role | Leasing-operations coordinator |
| Age | 35 |
| Location | Lima operations center |
| Technology level | Medium-high; works with CRM, email and spreadsheets |
| Devices | Corporate laptop and smartphone |

## Daily context

Julia coordinates the handoff from commercial and credit teams to contract preparation and supplier contact. Today she maintains a spreadsheet to know which case is approved, which document is missing and who must act next.

## Goals

1. See every active case with status, owner and next action.
2. Receive only cases that completed the required prior step.
3. Prevent an accepted quote from expiring without follow-up.
4. Keep applicant, machinery and supplier information consistent through the process.

## Pain points

1. Acting on a case before she can confirm Carlos's formal approval risks starting contract preparation on a deal that was never credit-approved.
2. Credit approval arriving by email, without reassigning ownership or stating her next action, means a decision can go unnoticed for days while Pedro waits on a delivery that has not moved.
3. Discovering that the company, RUC or machinery description differs from Carlos's approved case mid-preparation risks producing a contract that does not match what credit actually approved.
4. Retyping the supplier, approved machinery and financial terms into a separate file risks introducing errors that make the contract diverge from the approved decision.
5. Preparing the contract reference without visibility into the exact approved installment and term risks a contract that does not reflect what was actually approved.
6. When supplier confirmation and delivery date live only in an email thread, nothing forces her to close the loop, and a delivery can slip without anyone tracking it against the case.
7. Pedro has to call operations directly because he cannot see whether a delivery date has been confirmed, pulling her away from other cases to answer status questions.
8. Without a record of when Pedro accepted the quote or Carlos approved credit, she cannot tell how much time has already passed before she even starts scheduling — time that matters if Pedro's mobilization date is at risk.
9. Delivery can be coordinated while the case owner is still credit, leaving it unclear who is accountable if the handoff goes wrong.
10. Without one clear signal that supplier, contract reference and delivery date are all recorded, a case can be treated as complete while a required piece is still missing — and no one catches it until Pedro complains.

## Pain points demonstrated by the POC

| Pain points | POC response |
| --- | --- |
| 1, 2, 9 | Julia can act only in `CREDIT_APPROVED`; the handoff changes the owner and next action explicitly. |
| 3, 4, 5 | Her view reuses the same company, machinery and approved payment terms without re-entry. |
| 6, 10 | Completion requires supplier, contract reference and confirmed delivery date, then moves to `DELIVERY_SCHEDULED`. |
| 7 | The scheduled delivery becomes visible in Pedro's view. |
| 8 | The shared case history shows Pedro's and Carlos's earlier actions in order. |

## Key scenario

After Carlos formally approves Pedro's case, Julia receives the same record with herself as owner. She verifies the approved company, machinery and payment term, records the supplier and contract reference, and confirms a delivery date. The case then returns to Pedro as `DELIVERY_SCHEDULED`.

## Success criteria

- Every active case has one status, owner and next action.
- No case reaches contract preparation with mandatory data missing.
- Identify delayed cases and the responsible side in less than one minute.
- Complete the happy-path handoff without copying applicant or approved financial data.
- Make the supplier and scheduled delivery date visible to Pedro in the same case.
