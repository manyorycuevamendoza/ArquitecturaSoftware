# Carlos — Credit-Risk Analyst

> Focus: Make consistent, explainable leasing decisions

## Profile

| Field | Value |
| --- | --- |
| Name | Carlos Medina Paredes |
| Role | Senior credit-risk analyst |
| Age | 44 |
| Location | Leasing company headquarters, Lima |
| Technology level | High; uses financial models, bureaus and document systems |
| Devices | Corporate laptop with secured access |

## Daily context

Carlos reviews applications from companies of different sizes and sectors. He must determine whether project cash flow and company history support the requested lease while leaving an auditable explanation for approval committees and future reviews.

## Goals

1. Receive complete applications in a consistent structure.
2. Understand which policy rules produced the preliminary result.
3. Request missing evidence without restarting the application.
4. Record a decision, reason and supporting evidence for audit.

## Pain points

1. Pedro's RUC, machinery value, operating history and project cash flow arrive in separate emails or spreadsheets that Carlos must consolidate.
2. He cannot tell whether Pedro accepted the preliminary quote or whether the case is actually ready for formal review.
3. He starts reviewing a case without knowing whether the RUC record, signed project contract and bank statements are present and valid.
4. He manually recalculates the initial payment, financed amount and 36-month installment to verify the applicant's quote.
5. He receives only `PRE_APPROVED` or `MANUAL_REVIEW` without seeing which rule passed, failed or which policy version produced it.
6. Project cash flow and installment are shown in different screens, making the 125% payment-coverage check difficult to confirm.
7. He records an approval in personal notes without a mandatory reason attached to the application.
8. After approval, he must email Julia because the case does not automatically change owner or next action.
9. He cannot reconstruct who submitted, accepted and approved the case in chronological order.
10. A borderline case may be rejected before he can validate supporting evidence and apply human judgment.

## Pain points demonstrated by the POC

| Pain points | POC response |
| --- | --- |
| 1, 4, 6 | Carlos sees Pedro's normalized application, the same calculated quote and the project cash flow in one view. |
| 2 | The case enters Carlos's actionable view only after Pedro accepts the preliminary quote. |
| 3 | Approval requires a visible checklist for RUC record, project contract and bank statements. |
| 5, 10 | The view displays each versioned policy result and accepts both formal-review and manual-review cases. |
| 7 | Carlos must enter an approval reason; the decision stores analyst, time and policy version. |
| 8 | Approval changes the owner to Julia and states her next action. |
| 9 | The shared timeline records submission, quote acceptance, credit approval and delivery scheduling. |

## Key scenario

Carlos opens the same case after Pedro accepts the quote. He compares project cash flow with the calculated installment, reads every policy result, marks the three required evidence items as valid and records the formal approval reason. The case immediately becomes Julia's responsibility.

## Success criteria

- Every review-ready case contains all mandatory fields and evidence states.
- Recalculate a quote with the same result as the applicant view.
- Trace every material change to actor and time.
- Explain a decision using stored policy results rather than personal notes.
- Prevent approval until all three required evidence items are validated and a reason is recorded.
