# SDE2 and Staff interview curriculum improvement spec

## Status and intent

This is a curriculum change specification, not an implementation checklist for
production networking. It records the review of the current repository and the
work needed to make the material credible preparation for SDE2 and Staff-level
software engineering interviews with a networking, edge, or platform focus.

The repository is already a strong networking primer. The gap is that its
coverage is wider than its role calibration: it teaches many protocols and
vendor surfaces, while senior interviews also test distributed-systems design,
capacity reasoning, software implementation, migration leadership, and the
ability to make uncertainty and trade-offs explicit. The plan below adds that
layer without turning the repository into a BIG-IP operations runbook.

## Review baseline

The review found the following current inventory:

| Area | Current evidence | Assessment |
| --- | --- | --- |
| Long-form foundations | 17 book chapters | Broad and generally deep; needs stronger senior-level synthesis |
| Focused references | 33 topic files | Good protocol/vendor decomposition; several adjacent topics still overlap |
| Incident practice | 19 case studies | Strong evidence-led habit; add business impact, organizational decisions, and recovery economics |
| Interview banks | 85 broad questions; 94 F5 questions | Excellent breadth; role progression and coding/design calibration are uneven |
| Design practice | 10 system-design exercises | Good scenarios; needs explicit Staff review criteria, cost, ownership, and evolution |
| Simulation practice | 20 numbered scenarios in the simulation pack | Good diagnostic format; add coding, behavioral, and ambiguous-design sessions |
| Study plan | 2-, 4-, and 6-week paths | Useful sequence; add entry assessment, exit gates, and separate SDE2/Staff outcomes |
| Evidence discipline | `docs/references.md` and fact/inference ledgers | Preserve and extend to cloud-provider and distributed-systems claims |

The current role map in `docs/networking-interview-bank.md` names SDE1, SDE2,
and automation, but not Staff. The repository specification and README likewise
frame the primary audience through SDE2. That is the clearest product-level gap:
Staff expectations are currently implied in a few design and communication
exercises rather than represented as a first-class track.

## Outcomes by level

### SDE2 outcome

After completing the SDE2 track, a candidate should be able to trace a request
across DNS, routing, transport, TLS, HTTP, proxy/load-balancer, service, and
dependency boundaries; design a resilient service edge; estimate capacity and
failure load; write a small correct implementation or automation tool; debug
from evidence; and propose a safe, reversible change. The candidate should
explain at least two alternatives and identify a falsifier for the leading
hypothesis.

### Staff outcome

After completing the Staff track, a candidate should be able to frame an
ambiguous problem, define an SLO and business constraint, choose boundaries
and ownership, reason about multi-region and multi-tenant failure, quantify
cost and capacity, lead a migration, create an adoption plan, and communicate
risks to engineers and stakeholders. The candidate should show how the design
evolves from the current state, how it is operated by other teams, and what
evidence would change the decision.

### Shared answer contract

Every senior answer exercise should prompt for: assumptions, request/control
path, state and ownership, capacity model, failure domains, security boundary,
observability, rollout, rollback, and one explicit trade-off. Protocol facts,
vendor terminology, and engineering inferences must remain labeled and cited
according to `AGENTS.md`, `docs/references.md`, and `book/FACT-INFERENCE-LEDGER.md`.

## Gap analysis

### 1. Existing topics need senior synthesis

The current material is strong on individual mechanisms—TCP, DNS, TLS, LTM,
GTM/BIG-IP DNS, Kubernetes ingress, BGP, overlays, security, and observability.
It is less explicit about how an engineer composes those mechanisms into a
service with a stated availability target, cost limit, and migration plan.

Improve the existing chapters and focused topics with cross-topic “design
bridge” sections. Each bridge should connect the packet path to control-plane
convergence, application semantics, data ownership, and the operational
decision. Priority bridges are:

- DNS/GTM plus client caching, connection reuse, data replication, and write
  fencing.
- LTM/proxy plus retries, deadlines, backpressure, queueing, and idempotency.
- Kubernetes ingress plus service discovery, endpoint churn, rollout safety,
  and network policy.
- BGP/anycast plus stateful sessions, regional capacity, route convergence,
  and traffic evacuation.
- TLS/mTLS plus identity lifecycle, authorization, secret rotation, and clock
  dependencies.
- Observability plus SLOs, error-budget policy, sampling bias, and incident
  command.

### 2. Distributed-systems foundations are underrepresented

Add explicit coverage of replication and consistency, partition behavior,
leader election and fencing, queues and event delivery, rate limiting,
backpressure, retries and deadlines, idempotency, leases, failure detectors,
and transactional boundaries. These are not “extra networking topics”: they
are the semantics that determine whether a DNS failover, retry policy, or
multi-region edge is safe.

The new material must use networking examples and avoid pretending that one
consistency model or failover policy is universally correct. It should include
small state machines, timing diagrams, and interview prompts that distinguish
availability from correctness.

The multi-region section must go beyond a single-primary example. It should
cover active-active conflict handling, replication lag, read/write routing,
deduplication, quorum choices, data residency, failback, and fencing. DNS or
anycast traffic movement is only one part of a stateful failover; the answer
must establish when a region is allowed to accept writes.

### 3. Cloud networking is too abstract for platform interviews

Expand cloud coverage from security groups/NACLs and Kubernetes ingress to
provider-neutral VPC/VNet design: route tables, subnets, gateways, NAT and
egress, private connectivity, peering/transit, load-balancer classes, DNS
boundaries, identity-aware access, quotas, and cross-zone cost. Add one
provider-specific comparison appendix only where behavior is documented and
version-sensitive.

The focus is not memorizing console names. Candidates should draw the packet
path, identify the stateful boundary, explain return routing, estimate NAT and
load-balancer limits, and state what must be verified in the target cloud.

Split this from Kubernetes rather than adding more paragraphs to the combined
chapter. The cloud file should own tenant routing, subnets, gateways, private
connectivity, egress, quotas, cross-zone cost, and provider-neutral load
balancer classes. The Kubernetes file should own CNI, kube-proxy/IPVS/eBPF
models, EndpointSlice propagation, NetworkPolicy, Gateway API, ingress/mesh
ownership, controller failure, and multi-cluster traffic.

### 4. Host and runtime behavior is a missing diagnostic layer

Add Linux and application-runtime fundamentals relevant to SDE2 interviews:
socket lifecycle, listen and accept queues, ephemeral ports, file descriptors,
conntrack, DNS resolver behavior, TLS/session reuse, thread/event-loop limits,
GC or process pauses, and graceful shutdown. Keep commands read-only or local
fixture-based. The goal is to explain why a healthy network path can still
produce connection failures or tail-latency spikes.

### 5. Software implementation practice is not a first-class track

The repository has useful Python demos and exercises, but the interview system
does not yet specify coding problems, test expectations, or review criteria.
Add language-neutral implementation prompts with Python reference solutions:

- CIDR aggregation and longest-prefix lookup.
- DNS cache with TTL, negative caching, and deterministic clock injection.
- Token-bucket and distributed-rate-limit model with clock and burst caveats.
- Retry/deadline budget simulator with idempotency classification.
- Consistent-hash ring with membership change analysis.
- Connection-pool and load-balancer selection model with health transitions.
- Config diff/reconcile engine with idempotent retries and ambiguous outcomes.
- Trace/span interval aggregation and critical-path calculation.

Each exercise needs API contract, edge cases, tests, complexity discussion,
failure injection, and a review rubric. It must remain standard-library-only
unless a separate optional environment is documented.

### 6. Staff-level influence and behavioral preparation is thin

Technical scenarios include communication and change safety, but there is no
dedicated Staff loop for strategy, conflict, prioritization, mentoring,
incident leadership, or cross-team adoption. Add behavioral prompts grounded in
the repository’s technical scenarios: negotiate a shared SLO, reject an unsafe
global rollout, resolve ownership for DNS/IPAM drift, persuade teams to adopt a
common edge platform, and explain a postmortem without blame.

Require Situation/Task/Action/Result plus scale, alternatives, dissent,
measured outcome, and what changed in the system or organization. Do not reward
heroics without durable prevention.

### 7. Edge and protocol extensions need focused treatment

Add focused coverage for modern DNS and IPv6 client behavior (DoH/DoT,
SVCB/HTTPS, NAT64/DNS64, split-horizon consequences, and dual-stack rollout),
edge resilience and abuse defense (volumetric versus application attacks,
scrubbing/CDN/WAF placement, bot signals, safe degradation, and incident
communication), and the routing underlay (ECMP, BFD, IGP versus BGP, VRFs,
route domains, and convergence budgets). These are optional specialist
extensions, but each is a common follow-up in platform and edge interviews.

The conceptual layer should be vendor-neutral first. Add equivalence matrices
for F5 LTM/GTM, cloud load balancers, Envoy/NGINX, service meshes, WAFs, and
API gateways so a candidate can transfer the abstraction instead of reciting
one product’s vocabulary.

## Multi-point improvement plan

The work should be implemented in the following order. “Improve” means revise
an existing file; “split” means create a separately navigable focused file;
“add” means introduce a new topic or practice artifact.

| Priority | Action | Change type | Primary files | Definition of done |
| --- | --- | --- | --- | --- |
| P0 | Establish role map and competency matrix | Improve | `README.md`, `SPEC.md`, `docs/interview-rubric.md`, `docs/networking-interview-bank.md` | SDE2 and Staff have distinct outcomes, question tags, scoring, and exit gates |
| P0 | Add a cross-topic request-to-decision design method | Improve | `book/01-tcp-ip-and-packet-journeys.md`, `book/12-observability-and-troubleshooting.md`, `docs/network-system-design-exercises.md` | Every design traces data path, control path, state owner, SLO, capacity, rollout, and rollback |
| P0 | Upgrade existing topic Q&A from mechanism recall to senior reasoning | Improve | All `book/topics/*.md`, both interview banks | Questions include ambiguity, alternatives, quantitative follow-up, falsifier, and caveat |
| P0 | Add distributed-systems foundations | Add | `book/18-distributed-systems-for-networked-services.md` | Replication, consistency, leases, queues, retries, backpressure, fencing, and idempotency have worked examples and Q&A |
| P0 | Add Staff design and leadership rubric | Add | `docs/staff-interview-rubric.md`, `docs/staff-design-review-pack.md` | Designs score framing, ownership, evolution, adoption, cost, risk, and influence in addition to mechanism |
| P1 | Split cloud networking into a provider-neutral foundation and provider comparison | Split | `book/topics/34-cloud-networking-primitives.md`, `book/topics/35-cloud-provider-networking-comparison.md` | VPC routing, gateways, private connectivity, LB classes, quotas, cost, and verification are independently navigable |
| P1 | Add Linux sockets and runtime failure modes | Add | `book/topics/36-linux-sockets-and-runtime-networking.md` | Queue, FD, port, conntrack, resolver, shutdown, and tail-latency mechanics are tied to packet evidence |
| P1 | Split traffic management policy from distributed service semantics | Split | `book/topics/37-retries-deadlines-and-backpressure.md`, `book/topics/38-replication-failover-and-fencing.md` | Retry storms, write safety, stale reads, and failover are modeled with timelines and state transitions |
| P1 | Add coding track | Add | `exercises/07-cidr-routing-lookup.md` through `exercises/14-trace-and-reconcile.md`, `docs/interview-coding-rubric.md` | Eight exercises have tests, complexity, edge cases, and interviewer follow-ups |
| P1 | Add multi-tenant and cost design | Improve/add | `book/16-bgp-anycast-and-multi-region.md`, `book/17-network-security-waf-zero-trust.md`, `book/topics/39-multi-tenancy-cost-and-quotas.md` | Isolation, noisy neighbors, quota exhaustion, data residency, and cost allocation are explicit |
| P1 | Expand failure and migration practice | Improve | `book/case-studies/`, `docs/network-system-design-exercises.md` | At least six cases include migration stages, stakeholder constraints, blast-radius math, and recovery economics |
| P1 | Add vendor-neutral traffic-platform mapping | Add | `book/topics/40-traffic-platform-equivalence.md` | Portable concepts map to F5, cloud LB, Envoy/NGINX, mesh, WAF, and API gateway without implying identical behavior |
| P1 | Add modern DNS/IPv6 client behavior | Add | `book/topics/41-modern-dns-and-ipv6-client-behavior.md` | DoH/DoT, SVCB/HTTPS, NAT64/DNS64, Happy Eyeballs, split-horizon, and dual-stack migration are tested with evidence |
| P2 | Add Staff behavioral and influence practice | Add | `docs/staff-behavioral-exercises.md`, `docs/interview-simulation-pack.md` | At least 12 prompts use technical context and score influence, learning, and durable outcomes |
| P2 | Add edge abuse and underlay extensions | Add | `book/topics/42-edge-abuse-defense.md`, `book/topics/43-routing-underlay-and-convergence.md` | DDoS/bot defense, ECMP, BFD, IGP/VRF, route leaks, and convergence trade-offs have bounded exercises |
| P2 | Add interview scheduling and assessment gates | Improve | `docs/interview-study-plan.md` | Entry diagnostic, weekly evidence log, timed coding/design/mock gates, and SDE2/Staff completion criteria exist |
| P2 | Extend references and validator contracts | Improve | `docs/references.md`, `book/FACT-INFERENCE-LEDGER.md`, `scripts/validate.sh` | New claims have primary sources; new files, headings, Q&A depth, links, diagrams, tests, and word budgets are validated; duplicate/generic answers are flagged |

## Topic split and addition map

Do not split topics merely to increase file count. Split when the protocol or
state model, evidence, or interview follow-ups differ materially.

| Current area | Keep and deepen | Split/add | Reason |
| --- | --- | --- | --- |
| `05-ddi` and DNS topics | Ownership, TTL, negative answers, DNSSEC, drift | Add leases, dynamic updates, and failure ownership module | DDI correctness and service discovery have different operators and state |
| `08-proxy`, LTM, HTTP topics | Hop boundaries and tuple tables | Add retries/deadlines/backpressure | Proxy behavior is unsafe without application semantics |
| `12-bgp` and `16-bgp-anycast` | Policy, RIB/FIB, convergence | Add anycast state and regional evacuation lab | Route reachability does not equal application correctness |
| `13-kubernetes` and service discovery | Endpoint and ingress debugging | Split cloud primitives from cluster abstractions | Cloud routing failures often precede Kubernetes state |
| `14-waf` and security | Trust boundaries and safe testing | Add multi-tenancy, quotas, abuse economics | Staff interviews test platform policy and business trade-offs |
| `16-capacity` | SLO, saturation, failure load | Add queueing, cost, and load-test interpretation | Capacity needs equations and economic constraints |
| F5 SDK/API topics | Idempotency, task polling, version drift | Add generic reconciliation/coding exercise | The transferable skill is safe distributed control, not only SDK syntax |
| F5 and edge products | LTM/GTM mechanisms | Add vendor-neutral equivalence matrix and abuse-defense track | Staff candidates must explain portable platform choices and safe degradation |

## Required content contract for new or substantially revised topics

Every topic should contain:

1. Learning objectives and prerequisites.
2. A mental model separating data plane, control plane, and state ownership.
3. A packet or request path plus a control/state transition diagram where useful.
4. A worked example with explicit assumptions and at least one calculation.
5. Failure modes with observed evidence, competing hypotheses, and falsifiers.
6. Security, privacy, and authorization boundaries.
7. Operational checklist, rollout, rollback, and verification.
8. One implementation exercise with edge cases and tests.
9. At least eight explained SDE2/Staff questions, tagged by level and skill.
10. Primary references and fact/inference labels; vendor defaults must be
    version-qualified.

For Staff-only artifacts, add ownership, migration/adoption, cost, stakeholder
trade-offs, and an architecture decision record. Mermaid diagrams must remain
ASCII-only and use the repository’s light theme with dark text.

## Practice-system design

Tag every prompt with one or more of `fundamentals`, `debugging`, `coding`,
`system-design`, `operations`, `security`, `behavioral`, `staff`, and `f5`.
The candidate’s scorecard should separately record mechanism, evidence,
quantification, safety, trade-off, communication, and verification.

Recommended gates:

- SDE2: average 3/4, no safety score below 3, two passing coding exercises,
  three passing design drills, and one incident simulation with a falsifier.
- Staff: average 3.5/4, no safety or ownership score below 3, two designs that
  include migration and adoption, two coding/reconciliation exercises, one
  cross-team behavioral scenario, and one design defended against changing
  requirements.

The study plan should begin with a diagnostic rather than a fixed reading
sequence. Record date, prompt, assumptions, score, missed concept, and the next
experiment. Re-test weak areas with an unfamiliar scenario so memorization is
not mistaken for readiness.

The design pack should contain detailed answer keys for all ten current design
exercises and at least twelve new Staff scenarios. Every Staff key must include
requirements discovery, capacity units, control/data-plane state, a
failure-domain matrix, rejected alternatives, ownership/RACI, migration and
failback, cost or risk constraints, and measurable verification criteria.

## Delivery phases

### Phase 0: calibration and contracts

Define tags, score dimensions, role outcomes, naming, and validator rules.
Update navigation and references first so later additions have a stable
contract.

### Phase 1: senior synthesis

Revise the existing core chapters, banks, design exercises, and study plan.
Add distributed-systems foundations and the Staff rubric. This phase should
make the current inventory more useful before adding many files.

### Phase 2: missing technical layers

Add cloud primitives, Linux/runtime behavior, retries/deadlines/backpressure,
replication/fencing, multi-tenancy, cost, and the coding track. Link each new
topic to at least two existing chapters and one case study.

### Phase 3: practice and validation

Add Staff behavioral/design packs, run timed pilots, collect scores, and tune
question difficulty. Extend `scripts/validate.sh` for role tags, required
sections, internal links, Q&A depth, and exercise tests.

## Acceptance criteria

The improvement is complete when:

- README and SPEC explicitly describe SDE2 and Staff outcomes.
- Every existing topic has an identified role tag and at least one senior-level
  follow-up or is marked for consolidation.
- The new distributed-systems, cloud, Linux/runtime, resilience-semantics,
  multi-tenancy/cost, vendor-neutral edge, modern DNS/IPv6, coding, and Staff
  practice artifacts exist and are linked.
- The practice system has measurable SDE2 and Staff gates, not only reading
  schedules.
- At least three end-to-end designs connect DNS/edge, service semantics, data
  correctness, observability, security, cost, and migration.
- All ten existing design exercises have detailed answer keys, and at least
  twelve additional Staff scenarios test ambiguity, influence, and evolution.
- At least eight coding exercises pass automated tests and discuss complexity.
- New protocol/vendor claims appear in `docs/references.md` or the appropriate
  fact/inference ledger, with engineering recommendations labeled as such.
- Mermaid content remains ASCII-only and light-themed.
- `./scripts/validate.sh` passes, `python3 examples/request_path.py` emits a
  successful trace, and every new exercise has a documented test command.

## Risks and guardrails

- **Breadth inflation:** prioritize synthesis and practice before adding files;
  consolidate duplicate HTTP/2 material if navigation becomes confusing.
- **Vendor drift:** keep provider and F5 behavior version-qualified and avoid
  operational commands that imply universal defaults.
- **False seniority:** require calculations, falsifiers, migration, and
  verification; do not equate long answers with Staff reasoning.
- **Unsafe experimentation:** use local/reserved targets, explicit
  authorization, bounded failure injection, and reversible changes.
- **Unmaintainable validator:** validate stable contracts and representative
  quality signals; avoid brittle exact prose tests that encourage padding.

## Out of scope

This plan does not promise preparation for every company’s coding algorithm
loop, language-specific interview, or domain-specific architecture. It does
not replace official F5, cloud-provider, RFC, or security documentation, and it
does not authorize changes to production networks.
