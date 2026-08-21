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

1. Julia can receive a `PRE_APPROVED` or `FORMAL_REVIEW` case by email and start preparing a contract before Carlos records `CREDIT_APPROVED`, creating work for financing that may still be rejected.
2. When Carlos approves by email without changing the owner to “Leasing-operations coordinator,” Julia has no queue item telling her to contact the supplier and the case can remain unattended for days.
3. If the contract draft says a different company name, RUC or excavator description from Carlos's approved record, Julia cannot tell which version is authoritative without returning the case to credit.
4. Copying “Maquinarias del Peru SAC,” the excavator description and approved values into an operations spreadsheet can introduce a supplier or amount different from the credit-approved application.
5. Without seeing the approved S/12,303.95 installment and 36-month term beside the case, Julia can assign a contract reference to terms that Pedro and Carlos never accepted.
6. A supplier confirmation and delivery date stored only in an email thread do not move the case to `DELIVERY_SCHEDULED`, so the team cannot distinguish a verbal promise from a recorded commitment.
7. If Pedro cannot see the supplier and confirmed date in his view, he calls Julia for status and she must search email before answering whether the excavator can arrive before mobilization.
8. Without timestamps for Pedro's acceptance and Carlos's approval, Julia cannot calculate how long the case waited before reaching operations or identify which handoff endangered the project start.
9. If Julia can schedule delivery while the case owner is still Carlos or the status is `FORMAL_REVIEW`, two roles can act on incompatible assumptions about whether credit was approved.
10. If supplier name, contract reference or delivery date can be omitted, Julia may mark the case complete even though Pedro still lacks one of the three pieces needed to plan receipt of the excavator.

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
