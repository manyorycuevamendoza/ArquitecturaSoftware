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

1. Consolidating Pedro's RUC, machinery value, operating history and cash flow from separate emails and spreadsheets slows every review and introduces transcription errors that can affect a credit decision.
2. Without knowing whether Pedro accepted the preliminary quote, he risks spending review time on a case Pedro never confirmed, or delaying one Pedro is actively waiting on.
3. Starting a review without knowing whether the RUC record, project contract and bank statements are present forces rework once a missing document surfaces mid-analysis.
4. Manually recalculating the initial payment, financed amount and installment is slow, and a mismatch he misses could mean approving a deal at the wrong terms.
5. Receiving only `PRE_APPROVED` or `MANUAL_REVIEW`, without the rule and policy version behind it, leaves him unable to explain or defend the decision to the approval committee.
6. Cross-referencing cash flow and installment across separate screens makes it easy to misjudge the 125% payment-coverage check and approve a deal that does not actually meet it.
7. Recording an approval only in personal notes, without a mandatory reason on the case, leaves the company unable to defend the decision if it is later questioned in an audit.
8. Emailing Julia after approval, instead of the case reassigning itself, means a decision can sit unnoticed and delay Pedro's delivery.
9. Without a reliable chronological record of submission, acceptance and approval, he cannot defend the integrity of a decision during an audit or dispute.
10. Rejecting a borderline case automatically, before he can validate evidence and apply judgment, risks losing a client who was actually financeable.

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
