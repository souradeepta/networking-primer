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

### Scenario F: modern DNS and IPv6 migration

**Interviewer setup:** A company is adding dual-stack service discovery. Some
IPv6 clients reach an old backend, while IPv4 clients reach the current pool.
The DNS team proposes replacing the existing `A` record with `A` and `AAAA`
records immediately.

**Candidate expectations:** I clarify the service owner, client populations,
resolver paths, authoritative providers, DNSSEC status, and rollback window. I
compare authoritative `A`/`AAAA` data with recursive answers, TTLs, negative
caching, health checks, and the actual IPv6 path. I verify that the advertised
address is routed, filtered, monitored, and served with the expected SNI and
policy. The migration is a staged dual-stack rollout with a small client or
region cohort, telemetry by address family, and a documented removal plan.

**Follow-ups:** What if IPv6 succeeds at the edge but fails in the application
network? How do you handle resolvers that retain stale data? What is your
success criterion? A strong answer names Happy Eyeballs behavior, PMTUD and
ICMPv6 filtering, separate IPv4/IPv6 SLOs, resolver-cache observation, and a
time-based rollback threshold.

**Wrong-path correction:** Do not delete the `A` record, lower every TTL, or
blame DNS before proving the authoritative answer, recursive view, route,
firewall, and backend listener. An `AAAA` record is not evidence that the IPv6
service is production-ready. **Irreversible stop:** pause publication if the
IPv6 path can reach an unintended tenant, bypasses security controls, or lacks
an owner and rollback mechanism.

**Evidence table:**

| Area | Evidence and decision signal |
| --- | --- |
| Ownership | Named DNS, network, application, and security owners approve the cohort. |
| Migration/adoption | Dual-stack canary, client inventory, runbook, and support notice are ready. |
| Cost | Resolver queries, transit, monitoring, and address-management costs are estimated. |
| Risk | Separate family metrics show stale DNS, route, MTU, policy, and backend failures. |
| Verification | Authoritative/recursive comparison, IPv6 probes, logs, and rollback drill pass. |

### Scenario G: edge abuse defense during a flash sale

**Interviewer setup:** A public API is under a distributed request surge. The
edge sees credential stuffing and expensive search requests mixed with real
customers. Product asks for an emergency global rate limit, while security asks
to block several countries.

**Candidate expectations:** I establish incident authority, business priority,
protected paths, privacy constraints, and the current SLO/error budget. I
partition traffic by endpoint, identity signal, cost, geography, ASN, and
authenticated status, then measure cache hit rate, origin saturation, WAF
actions, false positives, and queue latency. I apply narrow reversible controls:
bot challenge, per-identity and per-IP budgets, expensive-operation limits,
origin shielding, and graceful degradation. I preserve safe paths for recovery,
accessibility, and trusted partners.

**Follow-ups:** How do you distinguish a NAT-heavy mobile network from an
attacker? What happens when the attacker rotates IPs? How do you communicate a
country block? A strong answer uses layered keys, challenge outcomes, sampled
decision logs, partner exceptions with expiry, and a review cadence. It treats
a geography block as a hypothesis with legal and customer impact.

**Wrong-path correction:** Do not deploy one global limit, permanently block an
entire country, or purge caches without checking whether the purge increases
origin load. Do not collect more personal data than policy allows.
**Irreversible stop:** stop an edge rule if it can lock out administrators,
disable emergency access, expose a protected origin, or cannot be rolled back
from versioned configuration.

**Scorecard:**

| Dimension | Full-credit behavior |
| --- | --- |
| Ownership/adoption | Incident commander, product, security, privacy, and support have named decisions and messaging. |
| Migration | Controls are canaried by endpoint or cohort and removed through an expiry plan. |
| Cost | Challenge, CDN, compute, and support costs are compared with origin protection value. |
| Risk | False positives, evasion, origin exposure, privacy, and partner impact are quantified. |
| Evidence/verification | Before-after SLOs, action logs, sampled traces, and rollback tests support each change. |

### Scenario H: cloud and Kubernetes ingress ownership boundary

**Interviewer setup:** A Kubernetes service is healthy inside the cluster, but
external users receive intermittent 502 responses after an ingress-controller
upgrade. The cloud team owns the load balancer, the platform team owns the
controller, and the application team owns the service.

**Candidate expectations:** I establish one incident owner and shared timeline,
then trace requests across DNS, cloud load balancer, listener, ingress class,
controller, route, service, endpoints, readiness, network policy, TLS secret,
and application logs. I compare failed and successful requests by zone,
protocol, hostname, and controller version. I capture rendered configuration
and metrics before mutation. I choose a reversible canary or controller
rollback, with explicit handoffs and an owner for every layer.

**Follow-ups:** What if only one availability zone fails? What if rollback
would invalidate a CRD? How do you make the fix adoptable? A strong answer
checks cloud target health separately from Kubernetes readiness, validates
CRD/API compatibility in a lab, documents support boundaries, and leaves
dashboards, alerts, and a tested upgrade procedure.

**Wrong-path correction:** Do not restart every deployment, change a service
selector blindly, or assign blame based on team ownership. A green pod does not
prove the cloud listener or ingress route is correct. **Irreversible stop:**
halt rollout if the controller could delete unmanaged routes, the rollback
artifact is untested, or traffic could cross an unintended trust boundary.

**Evidence table:**

| Area | Evidence and decision signal |
| --- | --- |
| Ownership | Incident owner plus cloud, platform, and application layer owners accept the handoff map. |
| Migration/adoption | Version matrix, canary namespace, training, and runbook are ready. |
| Cost | Cross-zone transfer, load-balancer rules, observability, and rollback capacity are included. |
| Risk | Zone skew, CRD drift, TLS exposure, policy gaps, and blast radius are reviewed. |
| Verification | Synthetic probes, target health, rendered routes, controller metrics, and recovery test agree. |

### Scenario I: automation change with evidence governance

**Interviewer setup:** An automation job should update 400 load-balancer
objects through a vendor SDK. A prior run timed out after partially applying
changes, and its logs contain credentials and inconsistent object names.

**Candidate expectations:** I stop repeat execution, identify the change owner,
authorization, desired-state source, SDK/API version, partitions, and affected
objects. I restrict existing logs, preserve an access-controlled evidence copy,
and rotate exposed credentials through the incident owner. I reconcile desired
versus observed state with stable identifiers and hashes, classify operations
by idempotency, and use dry-run, bounded batches, rate limits, checkpoints,
and a canary. Every mutation has an approver, request ID, result, and rollback
or compensating action.

**Follow-ups:** What if the API reports a timeout but the mutation succeeded?
How do you prove what changed? How do you make teams adopt the tool? A strong
answer reads state before retrying, uses task status or audit records, stores
redacted structured evidence with retention rules, publishes a diff and failure
budget, and pairs rollout with training and an escape hatch for manual recovery.

**Wrong-path correction:** Do not blindly replay all POSTs, print full payloads,
or treat a successful process exit as proof of convergence. Do not delete logs
before preservation and retention decisions. **Irreversible stop:** stop
automation if identity cannot be reconciled, authorization is ambiguous,
evidence is unavailable, or a batch lacks bounded rollback.

**Scorecard:**

| Dimension | Full-credit behavior |
| --- | --- |
| Ownership/adoption | Service owner, security, and platform approvers are explicit; users get a runbook and training. |
| Migration | Dry-run, canary, checkpointed batches, compatibility pinning, and rollback are demonstrated. |
| Cost | API quotas, operator time, log storage, and maintenance cost are compared with drift reduction. |
| Risk | Duplicate writes, partial failure, secret exposure, rate limits, and blast radius have controls. |
| Evidence/verification | Redacted IDs, before/after state, audit records, and reconciliation report prove convergence. |

### Scenario J: multi-region failover with stale state

**Interviewer setup:** The primary region is unreachable. DNS health checks are
failing, but the secondary has lower capacity and replication lag. Executives
want immediate global failover; the application stores sessions and writes
orders.

**Candidate expectations:** I confirm authority, data-loss tolerance, RPO/RTO,
region health, replication position, fencing capability, capacity, dependencies,
and customer communication. I prevent split brain by fencing or proving the
primary cannot accept writes before promoting the secondary. I estimate safe
capacity, shed noncritical work, preserve idempotency, and change traffic via
staged mechanisms with explicit DNS and cache behavior. I record the last
consistent point and distinguish read-only recovery from write recovery.

**Follow-ups:** What if the primary returns during promotion? What if the
secondary cannot serve all traffic? How do you fail back? A strong answer
names fencing evidence, session strategy, queue handling, customer impact,
controlled load, and a separately tested failback plan. It does not equate a
DNS change with application recovery.

**Wrong-path correction:** Do not promote both regions, lower TTL as the only
step, or discard replication state to make dashboards green. Do not promise
zero data loss when the measured replication point cannot support it.
**Irreversible stop:** stop promotion if fencing is unproven, writes can reach
both regions, the recovery point is unknown, or the secondary would exceed
safe capacity and cause cascading failure.

**Evidence table:**

| Area | Evidence and decision signal |
| --- | --- |
| Ownership | Incident commander, data owner, application owner, and executive authority are named. |
| Migration/adoption | Failover/failback drills, dependency contracts, and customer recovery guidance exist. |
| Cost | Warm capacity, replication, transfer, reserved resources, and degraded-service costs are explicit. |
| Risk | Split brain, stale writes, session loss, dependency saturation, and headroom are assessed. |
| Verification | Fencing proof, replication position, synthetic transactions, traffic telemetry, and checkpoints pass. |

### Scenario K: capacity and cost trade-offs for growth

**Interviewer setup:** Traffic is forecast to double before a major launch. The
network team proposes larger load balancers, application teams propose more
pods, and finance asks for a lower-cost plan. Graphs show average CPU, but not
connection churn, SNAT ports, queue depth, or tail latency.

**Candidate expectations:** I define the SLO, workload mix, peak shape, growth
confidence, failure domains, and time horizon. I model requests, concurrent
connections, TLS handshakes, bytes, backend service time, SNAT allocation,
queue depth, and p95/p99 latency. I identify the first constrained resource
and validate it with representative load and failure tests. Options include
right-sizing, autoscaling, connection reuse, caching, warm capacity, and
admission control; each has an owner, cost, migration steps, and rollback.

**Follow-ups:** What if average utilization is low but p99 latency rises? What
if the cheapest option increases operational risk? How do you win adoption? A
strong answer separates steady-state and burst cost, prices observability and
on-call load, documents assumptions, gives product a degraded-mode choice, and
sets trigger-based capacity reviews.

**Wrong-path correction:** Do not scale only on CPU, add retries to hide queue
growth, or purchase peak capacity without measuring the bottleneck. Do not run
an unbounded production load test. **Irreversible stop:** stop rollout if
headroom is unmeasured, autoscaling can amplify dependency failure, or a
cost-saving change removes the last safe failure-domain capacity.

**Scorecard:**

| Dimension | Full-credit behavior |
| --- | --- |
| Ownership/adoption | Product, finance, platform, and service owners agree on SLOs, triggers, and operating model. |
| Migration | Load test, canary, autoscaling guardrails, and rollback are sequenced before launch. |
| Cost | Compute, transfer, licensing, observability, and incident labor are compared over the forecast horizon. |
| Risk | Tail latency, dependency amplification, zone failure, SNAT exhaustion, and forecast error are modeled. |
| Evidence/verification | Workload model, saturation tests, p99 results, cost projection, and alert thresholds are reviewed. |

### Scenario F: modern DNS and IPv6 migration

**Interviewer:** A company is dual-stacking its public service. Some IPv6
clients reach the service, while others time out or receive stale DNS data.
Design the investigation and migration.

**Candidate:** I establish the service owner, customer impact, resolver
populations, regions, and whether the change is an experiment or a committed
cutover. I compare authoritative A and AAAA answers, TTLs, DNSSEC validation,
negative caching, and responses from representative recursive resolvers. I then
trace an IPv6 connection through the client, WAN, firewall, load balancer, and
backend, checking route advertisements, PMTUD, listener binding, health
checks, and return-path symmetry. A DNS answer is observed evidence; “IPv6 is
broken” is only a hypothesis. A successful controlled connection from the
affected resolver and network is the falsifier for a pure DNS explanation.

The service owner approves the target behavior and the network/platform owners
own the address, route, and listener changes. I migrate by publishing AAAA at a
small TTL only after the IPv6 path is monitored, then ramp by region or resolver
cohort. Adoption includes runbooks, support training, dashboards split by IP
family, and a clear owner for stale-cache reports. The cost trade-off is extra
dual-stack monitoring and firewall/load-balancer capacity versus reduced NAT64
dependency and better reachability. I stop before publishing broadly if the
IPv6 listener, security policy, or rollback path is unverified; withdrawing or
altering production AAAA records without an approved window is irreversible in
practice because recursive caches and client behavior persist beyond the change.

**Follow-up:** What if DNSSEC validates, but large responses fail only over
IPv6?

**Candidate:** I test EDNS0 sizes, fragmentation, ICMPv6 Packet Too Big, and
the authoritative-to-recursive path. I compare a smaller response, TCP fallback,
and a bounded probe from each hop. I do not globally disable DNSSEC or raise
MTU values blindly. If the evidence points to an MTU or filtering defect, I
stage the narrowest underlay or resolver correction, verify both A and AAAA
resolution, and keep the migration paused until rollback and owner sign-off are
complete.

| Evidence | Interpretation | Next decision |
| --- | --- | --- |
| Authoritative and recursive A/AAAA, TTL, AD bit | Separates data, cache, and DNSSEC facts | Continue to path testing or engage DNS owner |
| IPv6 route, firewall, listener, and health state | Identifies the failing hop | Assign network, security, or service owner |
| IPv4/IPv6 success rate and PMTUD probes | Measures user impact and falsifies guesses | Ramp, hold, or roll back by cohort |
| Approved change, rollback, and support readiness | Establishes adoption and authorization | Publish broadly only when all gates pass |

### Scenario G: edge abuse defense during a traffic surge

**Interviewer:** An edge service is receiving a tenfold request spike. It may
be a flash crowd or an application-layer attack. Protect availability without
blocking legitimate customers.

**Candidate:** I name the incident commander, service owner, security owner,
and decision authority, then define the SLO, affected routes, customer cohorts,
and time window. I compare request rate with unique clients, authentication
success, cache hit ratio, expensive endpoints, origin saturation, geography,
and response codes. I preserve sampled headers and request IDs with privacy
controls. A traffic spike alone does not prove abuse; a stable cohort with
normal business indicators can falsify the attack hypothesis.

I start with reversible controls: cache safe public objects, enforce existing
per-identity and per-IP budgets, apply challenge or rate limits to the narrow
signature, and protect expensive origin paths with queues and concurrency
limits. Security owns detection policy, the product owner approves customer
friction, and the platform owner owns edge capacity. Migration is from emergency
rules to versioned policy with staged thresholds; adoption requires on-call
training, a customer exception process, and a post-incident review. I compare
the cost of edge compute, challenge volume, and origin scaling against lost
transactions and false-positive support load. I stop immediately before a
global block, destructive bot action, or rule that can lock out the only admin
path; those controls require explicit authorization, a tested bypass, and a
rollback owner.

**Follow-up:** What if the attacker rotates IPs and the rate limit begins
blocking mobile customers?

**Candidate:** I remove the overly broad dimension from the canary rule and
shift to authenticated identity, endpoint cost, token reputation, and adaptive
behavior signals. I test a known-good mobile cohort and inspect false positives
before widening enforcement. I would rather absorb bounded edge cost or shed a
documented low-priority operation than silently deny critical customers. Every
rule gets an expiry, owner, rationale, and rollback test.

| Evidence | Interpretation | Next decision |
| --- | --- | --- |
| Rate, cache, origin, endpoint, and cohort metrics | Separates flash crowd from abusive cost | Scale, cache, queue, or investigate |
| Rule match and false-positive samples | Tests whether mitigation is targeted | Narrow, hold, or remove the rule |
| SLO/error budget and customer impact | Makes the trade-off explicit | Prioritize availability or friction with owner approval |
| Expiry, bypass, rollback, and audit record | Controls adoption and irreversible risk | Keep emergency policy temporary and reviewable |

### Scenario H: cloud/Kubernetes ingress ownership boundary

**Interviewer:** A Kubernetes application is intermittently unreachable after
moving ingress from a shared appliance to a cloud load balancer. Who owns the
problem and how do you proceed?

**Candidate:** I establish the application, cluster, cloud account, ingress
class, service owner, and incident authority. I follow one request through DNS,
the cloud load balancer, ingress controller, service, endpoints, network policy,
and pod readiness. I compare successful and failed zones, IP families, TLS
secrets, health-check paths, and controller events. “The pod is healthy” is
insufficient; readiness, endpoint publication, and the external data path are
separate facts. A direct, authorized probe to a ready endpoint that succeeds
while ingress fails falsifies an application-only theory.

The platform team owns the ingress class and cloud integration; the application
team owns routes, readiness, and backend behavior; security owns policy and
certificate requirements. I freeze the migration at the smallest affected
scope, route a canary service through the new path, and retain the old path
until parity is demonstrated. Adoption includes ownership in the service
catalog, dashboards, escalation rules, and a rollback rehearsal. I compare
managed load-balancer cost, cross-zone transfer, operational toil, and blast
radius against the shared appliance’s capacity and dependency risk. I stop if
the new path has no tested rollback, lacks an owner for certificates or policy,
or would delete the last known-good ingress object; deleting it is an
irreversible stop condition during an incident.

**Follow-up:** The controller reports healthy, but only IPv6 clients fail.

**Candidate:** I verify dual-stack service and endpoint addresses, load-balancer
front-end listeners, security-group rules, subnet routes, and backend return
traffic. I test with explicit IPv4 and IPv6 probes from affected networks and
check whether the health check uses the same address family as customers. I
avoid changing selectors or restarting pods before proving a control-plane or
network-path defect. The smallest safe change is a canaried listener or route
correction with an observed rollback.

| Evidence | Interpretation | Next decision |
| --- | --- | --- |
| DNS, listener, ingress, service, endpoint, and readiness state | Locates ownership across layers | Assign the next investigation owner |
| IPv4/IPv6 and zone-specific probes | Distinguishes family or locality failure | Hold migration or ramp a cohort |
| Cost, transfer, capacity, and error-budget data | Supports an explicit platform choice | Approve parity, redesign, or revert |
| Catalog owner, rollback object, and runbook | Tests adoption readiness | Do not retire the old path yet |

### Scenario I: automation and evidence governance

**Interviewer:** An automation pipeline can change 500 network objects, but its
last run created drift and the audit trail is incomplete. How would you make it
safe enough to resume?

**Candidate:** I assign an automation owner, affected service owners, change
approver, and evidence custodian. I freeze broad writes while preserving the
pipeline version, input manifest, request IDs, actor identity, timestamps,
diffs, task results, and current state. I classify each claim as observed fact,
vendor terminology, or engineering inference and record the source and
confidence. A clean dry run against one representative partition is evidence;
it does not prove that 500 objects are safe.

I introduce stable object identity, idempotent reconciliation, schema and
permission checks, bounded batches, canaries, postconditions, and automatic
pause on unexpected drift. The migration path is manual review to one-object
reconciliation, then a small batch, then progressively larger batches with
measured rollback. Adoption requires training, a support queue, ownership of
the fact/inference ledger, and dashboards that show desired versus observed
state. I weigh engineering time and slower deployment against the cost of
silent drift, incident recovery, and audit failure. I stop before any bulk
write if identity is ambiguous, evidence cannot be reproduced, or rollback
would require guessing; a bulk delete or overwrite under those conditions is
an irreversible stop condition.

**Follow-up:** A task timed out after the first 40 objects may have succeeded.

**Candidate:** I do not replay the whole batch. I reconcile each object by
stable name and desired-state hash, query task status where supported, and
record unknown outcomes separately. I retry only idempotent operations with
bounded backoff and an approval gate. I redact secrets but retain enough
request metadata to reproduce the decision, then verify postconditions and
produce an auditable exception list.

| Evidence | Interpretation | Next decision |
| --- | --- | --- |
| Versioned manifest, diff, identity, and task records | Establishes what was intended and attempted | Reconcile, retry, or quarantine |
| Desired/observed state and postconditions | Detects drift without duplicate writes | Continue in bounded batches |
| Permissions, schema, canary, and rollback test | Establishes safety and blast radius | Approve the next migration stage |
| Ledger labels, redaction, retention, and owner | Makes evidence adoptable and reviewable | Resume only with governance gates |

### Scenario J: multi-region failover and recovery

**Interviewer:** Region A is degraded and the team wants to fail over a
stateful service to Region B. Traffic is split by DNS and some clients cache
answers for hours. Lead the decision.

**Candidate:** I identify the incident commander, data owner, regional service
owners, and authority to fail over. I quantify the SLO breach, dependency
health, replication lag, write fencing state, capacity headroom, DNS TTL and
resolver distribution, and the expected RPO/RTO. I distinguish a route-control
failure from an application or data-integrity failure. A successful health
check does not prove Region B can safely accept writes; replication and fencing
evidence are required.

I first protect data by fencing or making the failed writer read-only according
to the service’s tested procedure. I then canary a small traffic cohort to B,
verify authentication, dependencies, latency, error rate, and write behavior,
and ramp only within B’s capacity budget. DNS is one steering mechanism, not an
instant kill switch; I use any approved connection or edge steering controls
and communicate cache delay. The regional owners own execution, the data owner
approves consistency risk, and customer support owns communication. Migration
includes a recovery plan for A, failback criteria, and a rehearsal after the
incident. I compare duplicate capacity and transfer cost with outage impact and
data-loss risk. I stop before accepting writes if fencing, replication freshness,
or B’s capacity is unknown; allowing concurrent writers is an irreversible
stop condition because conflict resolution may not restore customer intent.

**Follow-up:** Region B has capacity, but replication lag is above the stated
RPO.

**Candidate:** I do not call that a successful failover. I present the options:
remain read-only, accept an explicitly approved RPO breach, or shed a bounded
workload while repairing replication. I estimate affected records and customer
impact, obtain data-owner approval, and document the decision. After recovery I
reconcile writes and verify no split brain before returning traffic.

| Evidence | Interpretation | Next decision |
| --- | --- | --- |
| RPO/RTO, replication lag, fencing, and writer identity | Establishes data safety | Fail over, remain read-only, or stop |
| B capacity, dependency, latency, and error budget | Tests whether B can serve safely | Ramp by cohort or shed load |
| DNS/edge cache and client distribution | Sets expectations for convergence | Communicate and use approved steering |
| Failback criteria, owner, and rehearsal record | Supports adoption beyond the incident | Recover and return only after verification |

### Scenario K: capacity and cost trade-offs for growth

**Interviewer:** Forecasts show a 3x increase in traffic before a major launch.
The team proposes larger load balancers, more origins, and aggressive caching.
How do you choose?

**Candidate:** I name the product owner, capacity owner, finance partner,
security owner, and launch decision authority. I model demand by endpoint,
region, protocol, object size, cacheability, concurrency, connection lifetime,
and peak shape rather than multiplying today’s average. I map each limit:
edge requests, TLS handshakes, SNAT ports, bandwidth, origin CPU, database
connections, queue depth, and recovery capacity. I use production telemetry,
load-test results, vendor quotas, and an uncertainty range; a forecast is not a
fact. A replayed workload with realistic cache misses and failure injection can
falsify the assumption that caching alone solves the bottleneck.

I compare options as a staged decision: tune safe cache keys and compression,
reserve or add edge capacity, scale origins, protect dependencies with queues
and admission control, and reduce noncritical launch work. The service owner
accepts SLO trade-offs, finance approves recurring and burst cost, and platform
owns implementation. Migration and adoption require a capacity dashboard,
load-shedding policy, on-call training, budget alerts, and a launch rollback
plan. I include the cost of overprovisioning, egress, cache invalidation, lost
revenue, and operational complexity. I stop before enabling a cache rule that
could serve personalized data publicly, or before raising limits without a
tested dependency and rollback path; a privacy or data-integrity breach is an
irreversible stop condition even if availability improves.

**Follow-up:** Finance rejects permanent 3x capacity, but the launch date is
fixed.

**Candidate:** I propose temporary reserved or burst capacity with an expiry,
then reduce launch scope or use explicit admission control. I prioritize
critical journeys, publish what will be shed, and set triggers tied to SLO,
queue age, error rate, and budget. I run a canary load test and obtain written
approval for both spend and customer-impact policy. I will not hide saturation
behind retries or disable safety limits because that transfers cost and risk to
dependencies.

| Evidence | Interpretation | Next decision |
| --- | --- | --- |
| Demand model, limits, telemetry, and load-test results | Identifies the actual bottleneck | Select edge, origin, or protection work |
| Cache safety, privacy, and invalidation tests | Controls data-integrity risk | Enable only approved cache scope |
| SLO, queue, shed policy, and dependency signals | Defines graceful degradation | Ramp, hold, or reduce launch scope |
| Cost forecast, expiry, owner, and budget alert | Makes adoption financially accountable | Approve temporary or permanent capacity |
