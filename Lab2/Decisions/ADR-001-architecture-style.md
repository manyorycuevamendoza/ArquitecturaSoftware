# ADR-001 — Architecture style: hexagonal over 3-tier

- **Status:** Accepted
- **Scope:** Lab 2 — machinery-leasing platform
- **Supersedes:** the interim decision recorded in commit `5924d73` ("Cambiar arquitectura seleccionada a 3-tier")

## Context

The leasing platform has one cohesive domain — eligibility, quotation, credit policy and workflow — and a large, unstable perimeter of external capabilities: RUC and identity validation, negative-record sources, private credit bureaus, document storage, electronic signature, notification and supplier systems.

Two candidate styles were considered seriously. Both are viable for a system of this size; the choice was not about scale.

## Decision history

**First decision — hexagonal.** Chosen because the domain rules are the asset worth protecting and every external provider is replaceable.

**Interim decision — 3-tier** (commit `5924d73`). Adopted on the argument that a single team, a single deployment unit and a single database do not justify the ceremony of ports and adapters, and that a conventional presentation/business/data layering is faster to build and more familiar to review.

**Current decision — hexagonal** (reverted in the Lab 2 work). Two findings during requirements analysis reversed the interim decision:

1. The credit rules are not a thin layer over data. `FR-RSK-03` requires that the negative-record source be queried **before** any private-bureau query, and that a hit leave the later rules recorded as `NOT_EVALUATED` rather than failed. This is domain ordering logic whose correctness must be testable without any provider present. Under 3-tier the natural home for a provider call is the data layer, which makes the business layer depend on it and makes the ordering rule hard to test in isolation.
2. The POC must run with no real provider at all, while the pilot must reach authorized sandboxes and production must reach real ones — with the same rules unchanged. That is precisely a substitution requirement, which ports and adapters satisfy by construction.

## Decision

Adopt **hexagonal architecture (ports and adapters)** as one modular application over one transactional database.

## Consequences

**Positive**

- The credit and eligibility policies are pure domain code, testable without infrastructure. `scripts/self-test.mjs` exercises the short-circuit rule with no provider running.
- Provider substitution across POC, pilot and production is an adapter change, not a domain change.
- Each external boundary is named as a port, which makes the integration backlog explicit.

**Negative**

- More indirection than 3-tier for the same feature count; a reviewer unfamiliar with the style pays a comprehension cost.
- Ports invite speculative abstraction. Mitigated by the rule already recorded in [Architecture.md](../Architecture.md): add a port only for a demonstrated external boundary or test substitution.

**Retained from 3-tier**

The interim decision was right about scale. Hexagonal here means dependency direction, not distribution: one deployment unit and one database, as recorded in the data decision.

## Note on method

The reversal is the point worth recording. The style was chosen twice, and the second choice was driven by a specific requirement (`FR-RSK-03`) rather than by preference. Requirements before design, as the assignment asks.
