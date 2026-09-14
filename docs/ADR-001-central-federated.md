# ADR-001: Central Conversational Intelligence with Federated Journeys

## Decision

Use a central conversational platform for common AI capabilities and federated domain journeys for business capabilities.

## Why

A bank-scale organization needs consistent security/governance, one customer conversation, reusable model infrastructure, domain ownership, independent release cadence, bounded context and strong auditability.

## Consequences

Positive: domains evolve independently; model/provider changes remain centralized; security controls are consistent; cross-domain conversation is possible.

Trade-off: strong contracts and developer tooling are required; the central platform is critical infrastructure; context sharing must be carefully governed.
