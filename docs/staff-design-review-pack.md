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

## Worked Staff answer keys

These examples show the expected decision depth; they are not prescriptive
runbooks.

### Traffic delivery: F5 and DNS

Keep F5 LTM/GTM as the traffic-policy owner while the application team owns
health semantics and the platform team owns the shared edge service. Start
with read-only inventory and synthetic checks, then canary one low-risk VIP,
onboard tenants by cohort, and measure success with error rate, p99 latency,
DNS steering accuracy, and rollback time. Prefer staged migration to a
portable edge only where policy parity is proven; dual-running adds license,
egress, and operational cost, while a bad monitor or stale DNS answer risks a
wide outage. Communicate the cohort schedule, customer-visible behavior, and
go/no-go evidence in a shared review with product, security, and support. Stop
before any irreversible DNS delegation, certificate cutover, or stateful
policy change if ownership, rollback, or tenant impact is not evidenced.

### Routing and multi-region

The network team owns routing policy and failover automation, the service team
owns readiness and data fencing, and the data team owns promotion approval.
Validate the design in a shadow region, then migrate stateless traffic in
small cohorts before enabling writes and automated failover. Compare active-
active with active-standby using measured replication lag, RTO/RPO, regional
headroom, and the cost of duplicate capacity and cross-region transfer. Give
executives and support a plain-language failure plan, status cadence, and
customer impact thresholds. Stop before irreversible write-fencing or
database-promotion changes when replication evidence, residency approval, or
an independently tested failback is missing.

### Cloud and Kubernetes

The platform team owns ingress, cluster policy, and shared identity; workload
teams own service health and resource requests; security owns admission and
network policy exceptions. Establish one cluster as a pilot, test service
identity and certificate rotation, then adopt clusters and namespaces in
cohorts with an explicit rollback window. Choose managed ingress, a gateway,
or service mesh based on portability, operator load, telemetry cost, and the
risk of a common control-plane failure. Communicate ownership boundaries,
maintenance windows, and migration scorecards to developers and incident
commanders. Stop before irreversible CRD, identity, or policy migration if
the previous cluster cannot still serve traffic and restore testing is
incomplete.

### Security and WAF

Security owns detection policy and exception approval, the API team owns
request contracts and origin controls, and SRE owns availability guardrails.
Begin in observe-only mode with replay and representative traffic, tune by
endpoint and tenant, then enforce rules in cohorts with a tested bypass. Fund
WAF/CDN capacity and analyst review explicitly; false positives threaten
legitimate revenue while overly broad bypasses increase exploit risk. Share
blocked-request evidence, privacy implications, and customer-support guidance
before each enforcement stage. Stop before an irreversible block, certificate
change, or emergency bypass if an owner-approved exception path and verified
origin protection do not exist.

### Automation and observability

The network automation team owns reconciliation and change safety, device
owners own platform-specific contracts, and observability owns the telemetry
schema and SLO publication. Start with read-only discovery, then apply changes
to a lab and one production cohort; expand only after idempotence, timeout
handling, drift detection, and trace coverage meet the gate. Compare a central
controller with team-owned pipelines, including engineering effort, storage
and cardinality cost, rate-limit risk, and blast radius. Publish dashboards,
escalation paths, and weekly adoption evidence so teams can challenge bad
signals. Stop before irreversible device writes, schema removal, or alert
retuning if dry-run diffs, audit trails, and a tested restore path are absent.

### Reliability and capacity

Service ownership stays with the product team; SRE owns capacity modeling and
failure drills; finance and support own cost and customer-impact decisions.
Model normal, burst, dependency, and regional-loss load, then pilot bounded
load shedding and degraded features before changing queue or admission policy.
Compare overprovisioning, queueing, and graceful degradation using p99/SLO
impact, recovery time, spare-capacity cost, and fairness across tenants. Tell
stakeholders the trigger thresholds, degraded experience, and incident
updates before a test or real failover. Stop before irreversible traffic
shedding, data deletion, or feature-disable automation if capacity evidence,
tenant fairness, and a human-approved recovery path are not in place.
