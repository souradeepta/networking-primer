# Interview simulation pack

Each scenario expects: clarify scope, state a tuple and time, name evidence,
offer a falsifier, respect authorization, and verify recovery.

1. DNS cache mismatch. Follow-ups: TTL? LDNS? DNSSEC? Wrong paths: edit zone first; blame GTM. Boundary: reserved names only. Answer: compare authoritative, recursive, cache age, and topology. Score: evidence, safety, communication.
2. TCP timeout. Follow-ups: reset? NAT? ACL? Wrong paths: raise timeout; restart VIP. Boundary: read-only captures. Answer: compare SYN path, listener, route, SNAT, and return traffic. Score tuple and falsifier.
3. Expired certificate. Follow-ups: SNI? chain? mTLS? Wrong paths: disable validation; replace all certs. Boundary: no private keys. Answer: inspect served chain, profile, clock, canary, and rollback.
4. LTM 503. Follow-ups: monitor? member? policy? Wrong paths: clear persistence; disable monitor. Boundary: approved canary. Answer: identify responding hop and member eligibility.
5. SNAT exhaustion. Follow-ups: port model? long sessions? source identity? Wrong paths: clear all flows; broad SNAT. Answer: correlate allocation errors and tuples, then stage capacity.
6. GTM site failure. Follow-ups: iQuery? TTL? LDNS? Wrong paths: lower TTL only; delete pool. Answer: validate listener, monitor, pool, cache, and failover.
7. TLS algorithm finding. Follow-ups: clients? profile? exception? Wrong paths: exploit; disable TLS. Answer: authorized reproduction and staged policy.
8. HA failover. Follow-ups: state sync? drains? rollback? Wrong paths: force failover; edit both peers. Answer: compare config/runtime state and planned drain.
9. Kubernetes ingress. Follow-ups: endpoints? secret? policy? Wrong paths: restart deployment; change selector blindly. Answer: inspect class, route, TLS, readiness, and service.
10. VXLAN MTU. Follow-ups: inner/outer? ICMP? VTEP? Wrong paths: raise MTU globally. Answer: bounded lab probes and underlay evidence.
11. BGP route leak. Follow-ups: policy? RIB? FIB? Wrong paths: withdraw all routes. Answer: isolate prefix, preserve state, correct policy.
12. Cache privacy issue. Follow-ups: key? cookies? purge? Wrong paths: purge only; disable CDN. Answer: test variants and authorization boundaries.
13. gRPC stream reset. Follow-ups: deadline? drain? retry? Wrong paths: retry writes; raise timeout. Answer: inspect stream code, proxy limits, and idempotency.
14. NTP drift. Follow-ups: monotonic? TLS? source? Wrong paths: change timezone; relax certs. Answer: inspect offset, source, clock, and dependency symptoms.
15. Full logs. Follow-ups: retention? access? rotation? Wrong paths: delete evidence; copy secrets. Answer: restrict access, preserve protected evidence, rotate, patch.
16. Suspected breach. Follow-ups: containment? chain of custody? scope? Wrong paths: scan broadly; confront actor. Answer: incident authority, preserve evidence, isolate approved scope.
17. API task timeout. Follow-ups: retry? pagination? RBAC? Wrong paths: repeat POST; assume failure. Answer: GET state, poll task, stable identity.
18. Load spike. Follow-ups: SLO? capacity? retries? Wrong paths: add retries; chaos now. Answer: partition demand, queue, dependencies, and guardrails.
19. Pen-test request. Follow-ups: target? window? stop? Wrong paths: credential guessing; destructive exploit. Boundary: written authorization. Answer: scope, rate, owner, evidence, report.
20. Change review. Follow-ups: rollback? canary? version? Wrong paths: approve from screenshot; skip verification. Answer: diff, dependencies, test, owner, and recovery.

## Scorecard

Give 0-4 for mechanism, evidence, safety, trade-off, and verification per
scenario. Passing recommendation: no safety score below 3 and average at least
3. Follow-ups should expose assumptions, not reward memorized commands.
