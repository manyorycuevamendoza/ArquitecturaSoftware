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

1. A case appears in her spreadsheet after a preliminary result, but she cannot confirm whether Carlos formally approved it.
2. Credit approval arrives by email without changing the responsible owner or stating Julia's next action.
3. During contract preparation she discovers that the company, RUC or machinery description differs from Carlos's approved case.
4. She retypes the supplier name, approved machinery and financial terms into a separate operations file.
5. She cannot see the exact approved installment and number of monthly payments while preparing the contract reference.
6. Supplier confirmation and delivery date remain in an email thread instead of the applicant's case.
7. Pedro calls operations because he cannot see whether a delivery date has been confirmed.
8. She cannot reconstruct when Pedro accepted the quote or when Carlos approved the credit decision.
9. A delivery may be coordinated while the current case owner is still credit, producing unclear responsibility.
10. She has no single completion signal showing that supplier, contract reference and delivery date were all recorded.

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
