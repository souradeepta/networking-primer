# Network system design exercises

## Common requirements

For every design state request path, capacity assumptions, failure domains,
security boundaries, observability, rollout, and rollback. Label protocol facts
and engineering inferences. Use reserved addresses and authorized tests.

1. **Multi-site checkout:** Requirements: DNS/GTM site choice, LTM pools, TLS, drain, and stale-cache tolerance. Request path: LDNS to Wide IP to VIP to pool. Capacity: model peak connections and SNAT. Failures: site, DNS, member, certificate. Security: mTLS and RBAC. Observe SLO, TTL, health, and traces. Roll out one site first. Follow-ups: how handle cached answers? How test failover?
2. **Private service discovery:** Requirements: registry leases, readiness, config versions, retries. Path: client to resolver/registry to service. Capacity: registry and endpoint churn. Failures: partition and stale data. Security: identity and secret references. Observe effective version and endpoint. Canary configuration. Follow-ups: liveness versus readiness? Idempotent retry?
3. **CDN API edge:** Requirements: cache privacy and purge. Path: client to edge to origin LTM. Capacity: hit/miss and origin shield. Failures: stale object and origin overload. Security: key isolation and TLS. Observe age, status, origin timing. Version assets before rollout. Follow-ups: cache key? emergency correction?
4. **Kubernetes ingress:** Requirements: TLS, service routing, readiness, policy. Path: DNS to ingress to service endpoints. Capacity: connections and pod limits. Failures: empty endpoints and controller. Security: namespace and RBAC. Observe traces and endpoint slices. Canary ingress class. Follow-ups: rollback? network policy?
5. **BGP anycast edge:** Requirements: route policy and health withdrawal. Path: client to nearest announcement to edge. Capacity: regional headroom. Failures: route leak and stateful session movement. Security: prefix filters and authentication. Observe RIB/FIB and SLO. Stage one prefix. Follow-ups: convergence? asymmetric state?
6. **F5 automation platform:** Requirements: REST/SDK, AS3/DO/TS, RBAC, idempotency. Path: desired state to diff to task to effective VIP. Capacity: API rate and device resources. Failures: partial task and version drift. Security: scoped tokens. Observe request IDs. Canary declaration. Follow-ups: ambiguous timeout? pagination?
7. **DNS/DDI service:** Requirements: DHCP, IPAM ownership, authoritative DNS. Path: client lease to record to application. Capacity: scopes and queries. Failures: duplicate IP and stale record. Security: protected updates. Observe leases and audit. Roll out one scope. Follow-ups: overlap? recovery?
8. **TLS/mTLS gateway:** Requirements: SNI, trust rotation, backend re-encryption. Path: client to gateway to service. Capacity: handshakes and connections. Failures: expired chain and clock. Security: least trust. Observe ALPN and handshake errors. Canary certificates. Follow-ups: rollback? client inventory?
9. **Observability pipeline:** Requirements: logs, metrics, traces, TS-style export. Path: device/service to collector to store. Capacity: event volume and backpressure. Failures: destination or schema. Security: redaction and RBAC. Observe delivery SLO. Roll out one tenant. Follow-ups: sampling? data retention?
10. **Authorized resilience test:** Requirements: written scope, rate, abort, owner, recovery. Path: selected lab or canary dependency. Capacity: baseline and error budget. Failures: packet loss, delay, dependency outage. Security: no exploit or credential guessing. Observe impact and stop. Follow-ups: falsifier? rollback?

