# Machinery Leasing End-to-End Happy-Path POC — React

## Demonstrated flow

1. Pedro submits company, machinery and project-capacity data from React.
2. The domain applies explainable preliminary eligibility rules.
3. A transparent quote displays financed amount, number of payments, estimated installment and totals.
4. Pedro acknowledges and accepts the non-binding quote.
5. The same application moves idempotently to `FORMAL_REVIEW` and React switches to Carlos's view.
6. Carlos sees the same data, validates three simulated evidence items and runs the formal credit assessment.
7. The service checks a simulated negative-record source first. A match creates `CREDIT_REJECTED` and prevents the simulated private-bureau query.
8. For a clear RUC, an Equifax-like adapter returns score, overdue debt and late payments; the versioned domain policy records every pass/fail result.
9. The happy-path application moves to `CREDIT_APPROVED` and React switches to Julia's view.
10. Julia records a simulated supplier, contract reference and delivery date without copying Pedro's data.
11. The application reaches `DELIVERY_SCHEDULED`; Pedro sees approval, delivery information and the complete case history.

The role selector at the top lets the evaluator inspect the three views at any point. These are simulated POC views; no authentication or authorization is claimed.

## Architecture represented in code

```text
src/App.jsx + main.jsx                         React input adapter
src/application/leaseApplicationService.js    Application use cases
src/domain/preliminaryEligibilityPolicy.js    Quote and policy rules
src/domain/creditAssessmentPolicy.js           Ordered credit rules and short-circuit result
src/adapters/inMemory...Repository.js          Repository adapter
src/adapters/simulatedCreditRiskProviders.js   Negative-list and Equifax-like test adapters
```

The POC is a React single-page application. It uses no .NET, microservices, event queue, real external provider or production database.

## Prerequisite

Install Node.js compatible with the current Vite requirement: Node.js 20.19+, 22.12+ or a newer supported LTS. This POC was validated with Node.js 24.16.0.

## Install, test and build

```powershell
npm install
npm test
npm run build
```

Expected test output includes `SELF-TEST PASSED` and `Final POC state: DELIVERY_SCHEDULED`.

## Run the React POC

```powershell
npm run dev
```

Open the local URL printed by Vite, normally <http://localhost:5173>. Keep the sample values, calculate the quote, acknowledge its preliminary nature and accept it.

## Simulated credit-risk scenarios

Start a new scenario by reloading the page and entering one of these RUCs in Pedro's form:

| RUC | Formal credit result in Carlos's view |
| --- | --- |
| `20123456789` | Negative source clear; score 780, no overdue debt or late payments; `CREDIT_APPROVED` |
| `20999999999` | Negative record found; `CREDIT_REJECTED`; bureau and behavior rules `NOT_EVALUATED` |
| `20666666666` | Negative source clear; score 580, overdue debt S/8,500 and 4 late payments; `CREDIT_REJECTED` |

For every scenario, Pedro's preliminary values remain valid. Accept the quote and select **Run credit assessment** in Carlos's view. For the clear-RUC scenarios, mark the three evidence items first. For the negative-record scenario, they may remain unchecked because the service stops before document and private-bureau evaluation.

On the development machine used for this lab, the helper also detects the verified portable Node copy:

```powershell
.\run-poc.cmd
```

To execute the self-test and production build through the same helper:

```powershell
.\run-poc.cmd --validate
```

## POC boundaries

- In-memory data is lost when the page reloads.
- The formula and rules are illustrative, not an approved leasing policy.
- RUC, negative-record and financial behavior responses are deterministic test data, not validated against SBS, Equifax or another external provider.
- The Carlos checklist simulates validation; no real file upload, external verification or credit policy is implemented.
- The Julia step records simulated coordination; it does not sign a contract, contact a supplier or deliver machinery.
- Authentication, authorization, persistent storage, multi-case worklists and production audit controls are not implemented.
- The score ≥ 650, overdue debt = S/0 and maximum 2 recent late payments are illustrative thresholds, not Equifax rules or an approved leasing policy.
- `CREDIT_APPROVED` and `CREDIT_REJECTED` are simulated workflow decisions; the POC does not produce a legally valid decision, signed contract, supplier order, physical delivery or real financial transaction.
