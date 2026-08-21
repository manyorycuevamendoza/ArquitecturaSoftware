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

1. Carlos receives Pedro's company data, machinery value and project cash flow in different emails and spreadsheets, so he must consolidate them manually and can base the decision on a copied value that is incorrect.
2. He does not know which applicants accepted their preliminary quote and are genuinely waiting for formal credit evaluation, so he can prioritize a case that the customer abandoned.
3. He often discovers during analysis that the RUC record, signed customer project contract or recent bank statements are missing, forcing him to stop the review and contact Pedro again.
4. He recalculates the initial payment, financed amount, installment and term to confirm that he is evaluating the same financial conditions Pedro accepted.
5. He cannot justify an approval or rejection when he does not know which negative-record source and credit bureau were consulted, which values they returned or which policy rules were applied.
6. He manually compares project cash flow with the required installment coverage, increasing the risk of applying the payment-capacity rule incorrectly.
7. He records the reason for approval in personal notes, leaving the decision without a direct connection to the analyst, evidence, date and policy version used.
8. After approving a case, he must notify Julia and copy the approved terms manually; a missed email leaves the case without operational follow-up.
9. He cannot reconstruct the order and date of Pedro's submission, quote acceptance and credit decision when the evidence is distributed across different channels.
10. He may request a paid private-bureau report even when an earlier negative record already prevents approval, creating unnecessary cost and access to sensitive information.

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
