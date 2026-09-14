# Implementation Playbook

## 1. Start with the platform boundary

Build the central platform before building dozens of domain agents.

Central services: Conversation API, Conversation/Thread Store, Context Broker, Journey Registry, Model Gateway, Policy Engine, Tool Gateway, Guardrails, Audit/Trace and Evaluation.

## 2. Pick one read journey and one transactional journey

Start with account balance and own-account transfer. The pair proves context, authorization, confirmation, step-up authentication and deterministic execution. Do not start with autonomous financial actions.

## 3. Define the journey contract

Every journey should publish journey ID/version, owner, supported intents, capabilities, context schema, tools, risk classification, authorization scopes, confirmation requirements, escalation path, evaluation suite and SLO.

## 4. Make tools typed and deterministic

A tool should define name, version, input/output schemas, risk, required scope, idempotency requirement, audit fields, timeout and retry policy. The model may request a tool; the Tool Gateway decides whether it can reach a domain service.

## 5. Productionize in this order

1. Identity/IAM
2. Policy-as-code
3. Durable conversation store
4. Immutable audit
5. Secrets and key management
6. Transaction signing
7. PII/DLP
8. Observability/SIEM
9. Evaluation and model registry
10. Multi-region resilience

## 6. Federate without fragmenting UX

The customer sees one conversation while domains maintain scoped threads:

```text
Conversation C123
  ├── Accounts thread A1
  ├── Payments thread P1
  └── Lending thread L1
```

Each domain receives only context it is entitled to receive.

## 7. GCP evolution

```text
API Gateway / WAF
        ↓
Central Conversation Service
  ├── Cloud SQL / Spanner
  ├── Memorystore
  ├── Pub/Sub
  ├── Cloud Storage
  ├── Secret Manager
  ├── Cloud Logging / Monitoring
  └── Vertex AI / Gemini / approved model gateway
```

Use regional separation where data residency or resilience requirements demand it.

## 8. Measure before scaling

Track journey completion, abandonment, fallback rate, intent confidence, policy denials, confirmation conversion, tool error rate, model latency, cost per conversation, hallucination rate, unsafe response rate, context leakage rate, customer satisfaction and operational incidents.

## 9. Build an AI evidence chain

```text
conversation → journey version → prompt version → model/version
            → policy version → tool/version → transaction ID → outcome
```

Use this chain for model-risk management, compliance, incident investigation and customer disputes.

## 10. Golden rule

**The central platform provides intelligence and control. Domain teams provide capability and business authority. Core systems remain authoritative.**
