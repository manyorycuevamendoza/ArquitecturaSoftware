# Machinery Leasing Happy-Path POC — React

## Demonstrated flow

1. Pedro submits company, machinery and project-capacity data from React.
2. The domain applies explainable preliminary eligibility rules.
3. A transparent quote displays financed amount and estimated installment.
4. Pedro acknowledges and accepts the non-binding quote.
5. The same application moves idempotently to `FORMAL_REVIEW` for Carlos.

## Architecture represented in code

```text
src/App.jsx + main.jsx                         React input adapter
src/application/leaseApplicationService.js    Application use cases
src/domain/preliminaryEligibilityPolicy.js    Quote and policy rules
src/adapters/inMemory...Repository.js          Repository adapter
```

The POC is a React single-page application. It uses no .NET, microservices, event queue, external provider or production database.

## Prerequisite

Install Node.js compatible with the current Vite requirement: Node.js 20.19+, 22.12+ or a newer supported LTS. This POC was validated with Node.js 24.16.0.

## Install, test and build

```powershell
npm install
npm test
npm run build
```

Expected test output includes `SELF-TEST PASSED` and `Final POC state: FORMAL_REVIEW`.

## Run the React POC

```powershell
npm run dev
```

Open the local URL printed by Vite, normally <http://localhost:5173>. Keep the sample values, calculate the quote, acknowledge its preliminary nature and accept it.

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
- RUC and financial evidence are not validated against external providers.
- Authentication, document evidence, analyst review and operations dashboards are not implemented.
- The POC does not produce final approval, a contract or a real financial transaction.
