# SPEC TEMPLATE - SendIt Remittance Platform

## Summary

SendIt is a secure digital remittance platform. A sender creates and pays an international money transfer from the mobile application or website. The beneficiary receives a notification and withdraws the money in person at an authorized agent, similar to a Western Union location. The platform must protect identity and financial data, prevent money laundering, and preserve one consistent financial history.

The proposed happy path is: sender creates a quote, passes identity and compliance checks, pays once, and the beneficiary withdraws the available amount at an authorized agent. The same remittance can be consulted through the mobile application and website, subject to role permissions.

## Problem

People sending money internationally need to know the exact fee, exchange rate and amount the beneficiary will receive. They also need reliable confirmation that the money was not charged twice and that the beneficiary can collect it safely.

Remittance failures are financially sensitive. Duplicate requests, inconsistent status updates, weak identity checks, sanctions exposure, money laundering and provider outages can cause loss of funds or regulatory violations. SendIt needs one authoritative transaction history and explicit handling for uncertain external responses.

## Objective

Provide a secure and traceable service that allows a sender to create, pay and track a remittance, while allowing an authorized agent to verify the beneficiary and confirm an in-person cash withdrawal. The service must support both mobile-app and website access and must isolate AML information from users who do not need it.

## Out of scope

- Real bank, card, wallet, identity, sanctions or AML-provider integrations in the POC.
- Holding or settling real money with a financial institution.
- International regulatory certification for every country corridor.
- Automatic approval of a transaction with unresolved AML or provider errors.
- Agent cash-management, physical security and real-world cash delivery operations.
- A full banking core, card issuing service or cryptocurrency transfer.
- Production-scale disaster recovery and multi-region ledger partitioning.

## Key product concepts

| Concept | Definition |
| --- | --- |
| Remittance | A money transfer from a sender to a beneficiary in another country. |
| Sender | The user who creates and pays the remittance; the product's model user. |
| Beneficiary | The person who receives the money and may withdraw it. |
| Quote | Versioned exchange rate, fee, source amount and destination amount shown before payment. |
| Authorized agent | A physical cash-pickup location that verifies the beneficiary and confirms delivery. |
| Withdrawal code | One-time code used with identity verification to collect an available remittance. |
| AML review | Compliance assessment for identity, sanctions, limits, countries and unusual patterns. |
| Ledger | Append-only financial record of balanced debit and credit entries. |
| Idempotency key | Client request key that prevents one logical action from creating duplicate effects. |
| ON_HOLD | State used for AML alerts or technical uncertainty; it is not an automatic rejection. |
| CANCELLED | State used when the sender cancels before payment authorization; it cannot enable withdrawal. |
| Outbox | Transactional record used to publish notifications and provider work after the ledger commits. |
| Remittance status | The authoritative lifecycle state visible according to each user's permissions. |

## Users and their needs

### Ana — Sender

Ana sends money from Peru to her family member Luis in Colombia. She needs a transparent quote, strong authentication, a single charge, a clear status and a receipt. She uses the mobile application or website.

### Luis — Beneficiary

Luis needs to know when the money is available, the amount and currency, the authorized pickup location and the withdrawal code. He must not see Ana's private financial or AML information.

### Marta — In-person payout operator

Marta works at an authorized payout agent. She verifies Luis's name, identity document, one-time withdrawal code, amount and `AVAILABLE` status before handing over cash. She can confirm one withdrawal, but cannot edit balances or delete audit events.

## Key product decisions

1. The sender is the model user; the beneficiary is a beneficiary user, not the primary operator.
2. The mobile application and website use the same API, policies and source of truth.
3. Cash withdrawal is performed by an authenticated authorized agent and requires identity plus a valid one-time code.
4. AML alerts move a remittance to `ON_HOLD` for review; technical failures never become an automatic financial rejection.
5. PostgreSQL is the pilot source of truth for remittances, ledger entries, idempotency records and audit events.
6. Payment, ledger posting and state transition are committed atomically.
7. A repeated idempotency key produces one charge, one withdrawal confirmation or one state transition.
8. The ledger and audit history are append-only for application roles.
9. Notifications and provider calls use an outbox/worker flow after the financial transaction commits.
10. A modular three-tier architecture is sufficient for the pilot; microservices are deferred until independent scaling or isolation is demonstrated.

## Expected user experience

- The sender completes a remittance from either channel with the same behavior and data.
- The quote clearly separates source amount, fee, exchange rate and beneficiary amount.
- The sender receives a confirmation and can see `ON_HOLD`, `PAYMENT_PENDING`, `AVAILABLE` or `COMPLETED` without ambiguous wording.
- Compliance sees detailed AML evidence, while sender, beneficiary and agent receive minimized responses.
- The beneficiary receives a withdrawal code only after the remittance is available.
- The agent sees only the information needed to validate identity and pay the correct amount.
- A duplicate click or network retry does not duplicate a charge or cash delivery.
- Provider timeouts show a pending or failed state with a correlation ID, never a false success.

## Main flows

### Happy path: website or mobile application to agent withdrawal

1. Ana signs in with MFA and enters the beneficiary, corridor, amount and payment method.
2. SendIt validates required fields and displays a versioned quote.
3. Identity, limits, sanctions and AML checks pass.
4. Ana confirms the quote and pays with an idempotency key.
5. SendIt atomically records the debit, beneficiary credit obligation and `AVAILABLE` state.
6. Luis receives a notification and a one-time withdrawal code.
7. Luis visits an authorized agent similar to a Western Union location.
8. The agent authenticates, validates Luis's identity, code, status and amount.
9. SendIt records one withdrawal confirmation and moves the remittance to `COMPLETED`.

### Cancellation flow

1. Ana cancels before payment authorization.
2. SendIt atomically changes the remittance to `CANCELLED`, releases the quote and creates no debit or withdrawal code.
3. If payment is already confirmed, direct cancellation is rejected; a separate authorized refund flow is required.

### AML alert flow

1. A sanctions match, unusual pattern or limit breach is detected.
2. SendIt moves the remittance to `ON_HOLD` and records the signals and correlation ID.
3. An authorized compliance role reviews the case and records release or rejection with reason and policy version.
4. No payment or withdrawal is allowed before a release decision.

### Provider failure flow

1. An identity, payment or delivery provider times out or returns a malformed response.
2. SendIt records the provider, outcome and correlation ID.
3. The remittance remains pending or moves to `DELIVERY_FAILED`.
4. A retry or operator action may continue the case; the error is never treated as a successful payment or automatic AML rejection.

## Scope by stages

| Stage | Scope |
| --- | --- |
| POC | Deterministic identity, AML, payment and agent adapters; mobile/website channel model; quote; idempotent state flow; simulated in-person withdrawal; visible audit timeline. |
| Pilot | Real authentication, PostgreSQL ledger, RBAC, provider sandbox integrations, outbox workers, operational dashboard and agent portal. |
| Production | Country-specific compliance, real payment settlement, agent reconciliation, multi-region recovery, fraud operations and regulatory reporting. |

## Acceptance criteria

1. The sender can create a valid remittance from the mobile application or website and receives a unique ID.
2. The quote shows source amount, fee, exchange rate and beneficiary amount with two decimal places.
3. Invalid identity, beneficiary or amount data is rejected with a specific reason.
4. Twenty repetitions with one idempotency key create one payment effect.
5. AML or sanctions alerts create `ON_HOLD`, expose evidence only to compliance and block payment or withdrawal.
6. A provider timeout or malformed response never creates `COMPLETED` and includes a correlation ID.
7. The ledger contains balanced append-only entries for every successful payment and withdrawal.
8. A cancellation before payment creates no debit and cannot produce a withdrawal code.
9. The beneficiary receives a one-time code only when the remittance is `AVAILABLE`.
10. An agent cannot withdraw without authentication, valid identity, matching code and `AVAILABLE` status.
11. Twenty repeated withdrawal confirmations create one cash-delivery effect.
12. A valid withdrawal changes the remittance to `COMPLETED` and creates an audit event.
13. Sender, beneficiary, compliance operator and agent see only data allowed by their roles.
14. Mobile and website views display the same authoritative status for the same remittance.
15. The audit history records actor, timestamp, action, previous state, new state and correlation ID.
16. The requirements evaluation reaches at least 8/10 while preserving unresolved regulatory and integration gaps.