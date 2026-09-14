# Enterprise Conversational AI Reference Architecture

A GitHub-ready reference implementation for a central conversational AI platform with federated domain journeys. This repository is intentionally provider-agnostic and uses dummy banking data so teams can run it locally, inspect the end-to-end control flow, and adapt it to their own organisation.

## Status

Reference implementation / starter kit. It is **not** production banking software and must not be connected to real customer accounts, payment rails, credentials, or regulated decisioning without a full security, architecture, privacy, model-risk, resilience, and compliance review.

## What is demonstrated

- Central Conversation API and orchestrator
- Global conversation context with scoped journey threads
- Journey registry / capability catalogue
- Federated Accounts, Payments, Cards and Lending journeys
- Tool Gateway boundary between AI and authoritative bank services
- Deterministic policy and confirmation flow for financial actions
- Mock authentication and step-up authentication boundary
- Model Gateway with local mock mode and optional Gemini integration
- Lightweight knowledge/RAG component
- Guardrails and response composition
- Structured audit events and trace IDs
- Dummy core-banking service
- Browser demo UI
- Docker / Cloud Run deployment starter
- Tests and an enterprise implementation playbook

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Open `http://localhost:8080`.

Try:

- `What is my balance?`
- `Show my cards`
- `What lending options do I have?`
- `Move £500 to my savings`

A financial transfer is intentionally split into proposal -> confirmation -> execution. The model never receives credentials and never directly calls the dummy bank.

## Gemini

Set `GEMINI_API_KEY` to enable Gemini through the model gateway. If the key is absent, the deterministic mock model is used so the application remains runnable without external credentials.

```bash
export GEMINI_API_KEY="..."
export GEMINI_MODEL="gemini-2.5-flash"
uvicorn app.main:app --reload --port 8080
```

Keep API keys out of source control. For GCP, use Secret Manager and workload identity / service accounts rather than hard-coded credentials.

## Architecture principle

> Centralise intelligence; federate capability; isolate authority.

The central platform owns conversation management, model access, safety, context brokering, routing, policy controls, observability and shared infrastructure. Domain teams own journey knowledge, business rules, tools and deterministic workflows.

```text
Customer Channels
       |
       v
Conversation API
       |
       +--> Identity / Session / Consent
       |
       v
Central Conversation Orchestrator
       |
       +--> Context Broker
       +--> Intent / Journey Router
       +--> Model Gateway
       +--> RAG / Knowledge
       +--> Guardrails
       +--> Policy Engine
       +--> Journey Registry
       |
       +-------------------------------+
       |                               |
       v                               v
Payments Journey                 Accounts Journey
Cards Journey                    Lending Journey
Fraud / Disputes                 Other Domains
       |                               |
       +----------- Tool Gateway ------+
                       |
                       v
             Authoritative Bank APIs
                       |
                       +--> Core Banking
                       +--> Payments
                       +--> Cards
                       +--> CRM / KYC
                       +--> Risk / Fraud

Cross-cutting: Audit | Security | Model Risk | Privacy | Observability | Resilience
```

## Repository structure

```text
app/
  api/                  HTTP API
  core/                 configuration and logging
  journeys/             federated domain implementations
  models/               API/domain schemas
  platform/             central conversational platform
  security/             auth and step-up boundaries
  tools/                tool gateway + dummy bank
frontend/               minimal browser demo
data/knowledge/         starter knowledge source
docs/                   architecture and implementation playbook
tests/                  end-to-end tests
Dockerfile              container image
cloudbuild.yaml         GCP Cloud Build starter
deploy.sh               Cloud Run deployment helper
```

## How to extend it

### Add a journey

1. Create a module under `app/journeys/`.
2. Implement the `Journey` contract from `base.py`.
3. Declare capabilities with explicit risk levels.
4. Register the journey in `app/main.py`.
5. Add deterministic workflows for any state-changing operation.
6. Add domain knowledge and evaluations.
7. Add tests for happy path, ambiguity, policy denial and failure/retry.

### Replace the dummy bank

Keep `ToolGateway` as the enforcement boundary. Replace the implementation behind it with adapters to your organisation's APIs. Do not allow an LLM to call core systems directly.

### Replace mock authentication

Replace `MockAuthProvider` and `StepUpService` with your IAM/OIDC stack, customer session service, device trust, fraud/risk controls and transaction-signing service.

### Add persistence

The starter uses in-memory state for clarity. A production deployment should externalise conversation state, journey state, idempotency keys, audit evidence, policy decisions and operational events to managed durable stores.

### Add enterprise RAG

The included RAG module is intentionally small. Production RAG should add document ingestion, classification, ACL-aware retrieval, metadata filtering, versioning, citations, evaluation, poisoning controls and regional/data-residency controls.

## Security rule for actions

The reference transaction path is:

```text
LLM / Router proposes intent
        |
        v
Deterministic validation + policy
        |
        v
Customer confirmation
        |
        v
Step-up authentication / transaction signing
        |
        v
Tool Gateway
        |
        v
Authoritative bank workflow
        |
        v
Audit + authoritative result
        |
        v
LLM explains result
```

The LLM is not the source of truth for balances, authorisation, transaction state, fraud decisions or regulated credit decisions.

## GCP starting point

The application can be deployed to Cloud Run using the included Dockerfile / Cloud Build configuration. A production platform should additionally introduce:

- Secret Manager
- IAM service accounts and workload identity
- Cloud SQL / Spanner or another durable conversation store
- Pub/Sub for asynchronous events
- managed object storage for evidence and documents
- regional or multi-region deployment strategy
- Cloud Logging / Monitoring and OpenTelemetry
- WAF / API gateway / rate limiting
- KMS / HSM-backed key management where required
- SIEM integration
- CI/CD with security, dependency, IaC and model evaluations

See `docs/IMPLEMENTATION_PLAYBOOK.md` for the phased enterprise roadmap.

## Contributing

This project is designed as a reference architecture. Keep provider integrations behind adapters, keep domain ownership explicit, add tests with every journey, and document security assumptions and architectural decisions.

## License

Apache-2.0. See `LICENSE`.
