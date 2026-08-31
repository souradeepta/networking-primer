# Interview rubric

## Scale

| Score | Meaning |
| --- | --- |
| 0 | No model or unsafe action |
| 1 | Names a component, little evidence |
| 2 | Correct path with gaps |
| 3 | Evidence-led diagnosis and trade-offs |
| 4 | Clear mechanism, caveats, safety, and verification |

## Scored exemplars

1. **DNS wrong answer:** 0 guesses LTM; 2 queries authoritative and recursive; 4 records LDNS, TTL, topology, cache, ownership, and rollback.
2. **TCP timeout:** 0 changes timeout; 2 captures SYN; 4 compares both directions, NAT, ACL, listener, route, and falsifier.
3. **TLS failure:** 0 disables verification; 2 checks expiry; 4 checks SNI, chain, trust, clock, profile, canary, and rollback.
4. **LTM 503:** 0 restarts; 2 checks pool; 4 identifies responding hop, monitor source, member, policy, SNAT, and evidence.
5. **SNAT capacity:** 0 adds ports; 2 checks counters; 4 models tuple capacity, connection age, identity, route, and staged remediation.
6. **GTM failover:** 0 lowers TTL blindly; 2 checks health; 4 explains cache, LDNS, iQuery, monitor, TTL, and verification.
7. **Kubernetes outage:** 0 restarts pods; 2 checks endpoints; 4 compares selectors, readiness, service ports, policy, ingress, and rollout.
8. **BGP withdrawal:** 0 adds route; 2 checks session; 4 checks advertisements, policy, RIB, FIB, next hop, convergence, and blast radius.
9. **Automation retry:** 0 reruns POST; 2 catches exception; 4 reads state, handles task, idempotency, RBAC, audit, and rollback.
10. **Vulnerability:** 0 exploits target; 2 repeats scanner; 4 confirms scope, authorization, evidence, impact, mitigation, and retest.
11. **Load test:** 0 floods production; 2 sets rate; 4 defines baseline, guardrails, abort, owner, and recovery.
12. **Incident:** 0 blames team; 2 collects logs; 4 states impact, timeline, hypotheses, containment, evidence preservation, and lessons.

## Scoring guidance

Score mechanism, evidence, safety, communication, and verification separately.
Facts must be labeled as facts; inferences require a falsifier. A candidate who
knows syntax but cannot bound a change should not receive a production-ready
score.

## Answer templates

### 90-second answer

Clarify scope, user impact, and timestamp. State the mechanism and request
path, name two competing hypotheses, and identify the first read-only evidence
for each. Give one falsifier, one safe next action, the main trade-off, and the
verification or rollback signal. Finish with a concise uncertainty statement.

### Five-minute answer

Draw the architecture and both traffic tuples, state assumptions and capacity
units, walk through control-plane and data-plane state, and compare two design
options. Include security boundaries, observability, rollout, rollback, and
what you would do if the first API read or capture were ambiguous. Label facts
from RFCs or F5 documentation separately from inferences.

## Role-specific scorecards

| Dimension | SDE1 | SDE2 | Staff | Automation |
| --- | --- | --- | --- | --- |
| Mechanism | Correct layer and protocol | State transitions and failure domains | Portable abstraction, state ownership, and system evolution | API/resource semantics and convergence |
| Evidence | Useful command or capture | Correlated multi-hop evidence | Decision evidence, falsifier, and success metric | Redacted plan, status, and read-back |
| Trade-off | Practical operational risk | Design and capacity comparison | Cost, adoption, migration, and long-term operability | Retries, drift, and ownership |
| Safety | Avoids blind mutation | Defines blast radius and rollback | Makes authorization, blast radius, and rollback explicit across teams | Least privilege and unknown-state handling |
| Communication | Clear concise close | Decision record and escalation | Aligns stakeholders, handles dissent, and records durable ownership | Reproducible artifact and audit |

## Detailed exemplar explanations

**Expired certificate:** A score-4 answer identifies the termination hop, SNI,
SAN, chain, clock, and client/server SSL profiles; distinguishes expiry from
trust and mTLS authorization; stages overlap rotation; and verifies
representative clients. A weak answer says “renew the cert” without checking
the backend leg. Disabling verification is an unsafe score-0 response.

**LTM 503:** A score-4 answer identifies who emitted the response, records
VIP/pool/member/monitor/persistence/SNAT state, compares client and server
tuples, and names a falsifier. It proposes a canary monitor correction and
rollback. Restarting the origin or clearing all flows without evidence is not
production-ready reasoning.

**Ambiguous SDK timeout:** A score-4 answer classifies the outcome as unknown,
records request ID/status/task, reads by stable partition-qualified name, and
only then decides whether retry is safe. It mentions pagination, idempotency,
RBAC, redaction, and behavior verification rather than immediately repeating a
non-idempotent POST.
