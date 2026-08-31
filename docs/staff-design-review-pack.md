# Staff design review pack

These prompts are deliberately ambiguous. For each one, the candidate must
state assumptions, draw the packet and control paths, quantify capacity, name
owners, compare alternatives, and propose a staged migration with rollback.

## Design prompts

1. **Global checkout edge:** Move a single-region checkout service to two
   regions. Address DNS cache, write fencing, replication lag, data residency,
   RTO/RPO, failback, and who owns the database promotion decision.
2. **Platform load-balancer migration:** Replace a mixed F5 and cloud-LB fleet
   with a portable edge platform. Define compatibility, tenant onboarding,
   cost allocation, escape hatches, and adoption metrics.
3. **Retry storm:** A dependency is slow and every client retries. Design
   deadlines, budgets, backpressure, load shedding, tenant fairness, and a
   safe rollout without retrying non-idempotent writes.
4. **Multi-cluster ingress:** Provide one service identity across three
   Kubernetes clusters. Cover endpoint churn, policy, certificate rotation,
   traffic locality, cluster failure, and control-plane ownership.
5. **Abuse-resistant public API:** Protect an API from volumetric and costly
   application abuse while preserving legitimate bursty traffic. Compare CDN,
   WAF, gateway, and origin controls and define safe degradation.
6. **Private connectivity platform:** Give product teams private access to
   shared services across accounts or projects. Cover routes, DNS, identity,
   transitive connectivity, quotas, cost, and tenant isolation.
7. **Anycast stateful service:** Use anycast for a latency-sensitive service
   with some stateful sessions. Explain route withdrawal, session movement,
   regional headroom, and a migration path to stateless tokens.
8. **Certificate and trust migration:** Rotate a shared mTLS CA across many
   teams. Design overlap, client inventory, authorization mapping, emergency
   rollback, and a plan for unknown consumers.
9. **Observability ownership:** Create a cross-platform request trace and SLO
   standard. Define propagation, sampling, cardinality, privacy, storage cost,
   and how teams resolve conflicting definitions.
10. **Network configuration reconciliation:** Build a desired-state service
    for heterogeneous devices. Handle ambiguous API timeouts, drift, version
    differences, RBAC, rate limits, and safe partial failure.
11. **IPv6-only expansion:** Add IPv6-only clients without breaking legacy
    services. Cover DNS64/NAT64, dual-stack testing, telemetry, third-party
    dependencies, and an evidence-based rollback gate.
12. **Capacity under regional loss:** A service meets normal p99 latency but
    cannot absorb a region failure. Choose between overprovisioning, shedding,
    queueing, and degraded features; include cost and customer communication.

## Required review artifact

For each prompt, submit a one-page decision record with:

| Section | Required content |
| --- | --- |
| Context | Users, business impact, assumptions, SLO/RTO/RPO |
| Design | Data path, control path, state owner, security boundary |
| Capacity | RPS/CPS, concurrency, failure load, headroom, cost driver |
| Alternatives | At least two options and the rejected trade-off |
| Ownership | Team boundaries, operational contract, escalation |
| Migration | Canary, compatibility, adoption, rollback, failback |
| Evidence | Metrics, logs, traces, falsifier, success gate |

Score with [the Staff rubric](staff-interview-rubric.md). A polished diagram
without an ownership or rollback story is incomplete.
