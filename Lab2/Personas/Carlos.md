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
5. Consult negative records and credit behavior in a controlled order without paying for unnecessary bureau queries.

## Pain points

1. Carlos receives the company name and RUC by email, the S/450,000 machinery value in a sales spreadsheet and the S/18,000 monthly cash flow in another file; copying those figures into his model can change the decision through a transcription error.
2. Without a recorded quote-acceptance event, Carlos cannot distinguish a `PRE_APPROVED` case Pedro has not accepted from a `FORMAL_REVIEW` case that is ready for his work queue.
3. Carlos can begin analysis before noticing that the RUC record, signed customer project contract or recent bank statements are still missing, forcing him to stop and request evidence halfway through the review.
4. He manually recalculates the S/90,000 initial payment, S/360,000 financed amount and S/12,303.95 installment to confirm that his decision uses the same 36-month quote Pedro accepted.
5. A result without the negative-record source, bureau source, returned score, overdue debt, late payments and policy version prevents Carlos from reproducing the exact reason for approval or rejection.
6. With S/18,000 project cash flow on one screen and a S/12,303.95 installment on another, Carlos must manually verify the required S/15,379.94 coverage threshold and can apply the 125% rule incorrectly.
7. If the approval reason remains in Carlos's personal notes instead of the case, an auditor cannot link the decision to Carlos, its timestamp, evidence and `POC-CREDIT-2026-08-v1` policy version.
8. After approving the case, Carlos must email Julia and copy the approved terms; if she misses the message, the case remains without an operations owner and Pedro receives no delivery date.
9. Without one ordered timeline, Carlos cannot prove that Pedro submitted the data, accepted the preliminary quote and received the credit decision in the permitted sequence.
10. If RUC `20999999999` is already found in the blocking negative-record source, querying the private bureau anyway adds an unnecessary query and exposes score and debt data that the decision no longer needs.

## Pain points demonstrated by the POC

| Pain points | POC response |
| --- | --- |
| 1, 4, 6 | Carlos sees Pedro's normalized application, the same calculated quote and the project cash flow in one view. |
| 2 | The case enters Carlos's actionable view only after Pedro accepts the preliminary quote. |
| 3 | Approval requires a visible checklist for RUC record, customer project contract and bank statements. |
| 5 | The view displays the negative-list source, bureau source, score, overdue debt, late payments and every versioned rule result. |
| 10 | The negative-record adapter runs first; a hit stops the flow and records the remaining bureau rules as `NOT_EVALUATED`. |
| 7 | Carlos must enter an approval reason; the decision stores analyst, time and policy version. |
| 8 | Approval changes the owner to Julia and states her next action. |
| 9 | The shared timeline records submission, quote acceptance, credit approval and delivery scheduling. |

## Key scenario

Carlos opens the same case after Pedro accepts the quote. The application checks the simulated negative-record source first. If clear, it consults the simulated Equifax-like report and evaluates score, overdue debt and late payments together with the three evidence items. Carlos records the reason; only a fully passing case becomes Julia's responsibility.

## Success criteria

- Every review-ready case contains all mandatory fields and evidence states.
- Recalculate a quote with the same result as the applicant view.
- Trace every material change to actor and time.
- Explain a decision using stored policy results rather than personal notes.
- Prevent approval until all three required evidence items are validated and a reason is recorded.
- Prove that a negative-list hit prevents the credit-bureau query and leaves its rules as not evaluated.
- See the consulted source, returned values, policy version and outcome in the case.
