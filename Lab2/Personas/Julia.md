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

1. Julia does not know with certainty whether Carlos formally approved the financing before she begins preparing the leasing contract and contacting the supplier.
2. She does not know when an approved case becomes her responsibility or which operational action she must perform first, so the request can remain unattended for days.
3. She finds different company names, RUCs or excavator descriptions in the sales, credit and contract files and must ask which version was actually approved.
4. She manually copies the supplier, machinery description and approved financial terms into an operations spreadsheet, risking a contract with different information from the credit decision.
5. She does not have the approved S/12,303.95 installment and 36-month term available while preparing the contract reference and coordinating the purchase.
6. She stores the supplier confirmation and delivery date in email, so the rest of the team cannot verify whether the delivery is only being discussed or already confirmed.
7. She repeatedly answers Pedro's calls because he cannot consult the supplier or confirmed delivery date needed to plan operators and transport.
8. She does not know how long the request remained with sales or credit before reaching operations, making it difficult to identify which handoff delayed the project.
9. She cannot clearly identify whether Carlos or operations is responsible when contract preparation begins before the credit handoff is completed.
10. She can consider the coordination complete without confirming all three required items: supplier name, contract reference and delivery date.

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
