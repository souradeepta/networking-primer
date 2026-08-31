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

## Detailed conversation transcripts

The cards above are prompts; these transcripts demonstrate production-ready
reasoning. Separate observed facts from inferences, name a falsifier, and keep
mutations inside an approved change window.

### Scenario A: logs are full and the host is unresponsive

**Interviewer:** An LTM utility host reports 100% disk usage and SSH times out.
What do you do first?

**Candidate:** I clarify impact, owner, timestamp, and whether this affects one
host or an HA pair. I do not reboot or delete logs blindly. Through console or
approved out-of-band access I collect `df -h`, inode usage, mount state, load,
memory, and last-known service health. My hypotheses are runaway logging, a
core dump, or a blocked filesystem. A directory-size report is the falsifier.

**Follow-up:** What may be removed?

**Candidate:** I preserve incident evidence and retention requirements. I use
the supported rotation path, archive approved files, and remove only identified
temporary artifacts. If the filesystem is read-only, deletion will not repair
I/O and I escalate. I verify free blocks, logging recovery, management access,
and traffic-plane health, then add rate and retention alerts.

**Wrong path:** `rm -rf /var/log/*` destroys evidence and may remove required
files. **Boundary:** no destructive action without owner, backup, and approval.
**Scorecard:** 4 requires evidence, containment, preservation, verification,
and a recurrence control.

### Scenario B: certificate expired on one VIP

**Interviewer:** Clients report TLS expiry, but only one hostname fails.

**Candidate:** I identify the terminating hop and query the exact VIP with the
client SNI. I inspect the served leaf, SAN, issuer chain, validity interval,
signature algorithm, and local clock. I compare client/server SSL profiles and
determine whether the backend leg is TLS or plaintext. Expiry is a fact only
after observing the served certificate; trust-chain and SNI errors look similar.
I stage an overlapping certificate, attach it to the correct profile, canary
representative clients, and retain a rollback version.

**Follow-up:** What changes for mTLS?

**Candidate:** The server must validate the client chain, key usage, revocation
policy, and identity mapping. Renewing the server certificate alone does not
fix client-auth failure. I never copy private keys into chat or disable
verification. Verification includes handshake logs, both legs, expiry alarms,
and a post-change negative test.

### Scenario C: intermittent LTM 503

**Interviewer:** A VIP is reachable, but users see intermittent 503 responses.

**Candidate:** I determine who generated the 503 using headers, event logs, and
a correlation ID. I snapshot virtual-server, pool, member, monitor,
persistence, SNAT, and policy state. Hypotheses are no eligible members, a
monitor mismatch, or an origin response passed through. I compare successful
and failed requests, including selected-member tuples. A monitor sending the
wrong Host header is falsified by an equivalent probe from the monitor source.

**Follow-up:** How do you remediate?

**Candidate:** Correct the monitor or pool through a canary, validate expected
status/body and TLS SNI, then observe error rate and member state. I avoid
clearing all persistence or restarting origins because that destroys state and
can increase load. Rollback is the prior versioned configuration.

### Scenario D: SDK create timed out

**Interviewer:** A Python F5 SDK create request timed out. Should it retry?

**Candidate:** The outcome is unknown. I record request ID, method, partition,
payload hash, and timeout, then read by the stable fully qualified name. If the
object exists I reconcile desired and observed state; if absent I check task or
error status and retry only when the operation is idempotent and permitted. I
use bounded backoff with jitter, pagination, least privilege, and redacted
logs. A blind second POST can create duplicates.

### Scenario E: authorized pen-test reports weak TLS

**Interviewer:** A scanner reports a weak TLS suite on production. Respond.

**Candidate:** I verify written scope, source addresses, window, stop
conditions, and service owner before reproducing. I capture hostname/SNI,
protocol, cipher, chain, and scanner version with a non-destructive handshake.
I compare the finding with supported clients and exceptions, then propose a
staged profile change, canary, monitoring, and rollback. I do not exploit past
authorization or brute-force credentials. Retest evidence must show the weak
suite rejected without breaking approved clients.
