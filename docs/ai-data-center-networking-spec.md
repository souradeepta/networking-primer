# AI-era data-center networking curriculum specification

## 1. Implementation contract

This specification turns the companion Terra plan into an implementation-ready
contract for Luna. It defines what the new AI data-center networking treatment
must teach, model, test, index, and hand off. It authorizes only educational
documentation and a local, deterministic fixture. It does not authorize
production network changes, hardware testing, vendor account access, privileged
commands, credentials, or real workload execution.

The feature is complete only when a learner can connect a job-level symptom to
the relevant compute, host, fabric, storage, control, and security boundaries;
can distinguish supported facts from vendor naming and engineering judgment;
and can produce evidence-backed SDE1, SDE2, or Staff interview answers.

## 2. Deliverables and exact contracts

| Deliverable | Required contract |
| --- | --- |
| `book/topics/40-ai-data-center-networking.md` | Full focused-topic contract, at least 1,500 prose words, at least two Mermaid diagrams, one worked capacity calculation, one local-lab exercise, one failure matrix, and at least eight numbered explained Q&A. Use the next available topic number if 40 is occupied. |
| `book/topics/fixtures/ai-data-center/README.md` | Defines fixture version/schema, safety boundary, input model, outputs, phases, fault allowlist, command examples, expected-result interpretation, and cleanup. |
| `book/topics/fixtures/ai-data-center/runner.py` | Python standard library only. Validates JSON-like scenario input, derives observations, writes optional immutable local artifacts, and does not contact external systems. |
| `book/topics/fixtures/ai-data-center/test_runner.py` | Runs without external dependencies and proves deterministic output, input validation, negative controls, no direct outcome injection, manifest integrity, and cleanup. |
| `exercises/15-ai-fabric-capacity-and-failure-model.md` | A theory-to-practice exercise with scenario, constraints, provided fixture, deliverables, rubric, answer key, SDE2 extension, and Staff extension. |
| `book/case-studies/20-ai-training-fabric-straggler.md` | A narrative evidence-led simulated incident with a bounded fault, hypothesis tree, decision, safe repair, rollback, and retrospective. |
| Index/evidence/validation updates | Add topic/case-study/exercise navigation entries, a ledger row, references-map entries, and proportional structural validation after all content contracts are stable. |

All names, IPs, hostnames, cluster identifiers, tenant IDs, metrics, hardware
models, and costs in examples must be fictional, reserved, or explicitly
synthetic. Do not use an apparent customer name or a real endpoint. A default
run may write only to a temporary directory. A retained run requires an explicit
local `--artifacts-dir` below the fixture's `observed/` directory.

## 3. Required topic outline

The primary topic must use the following headings or semantically equivalent
headings that preserve validator-recognizable phrases.

1. `## Learning objectives`
2. `## Prerequisites`
3. `## Interview scope`
4. `## Mental model`
5. `## Topology and traffic paths`
6. `## Transport and congestion terminology`
7. `## Workload communication models`
8. `## Capacity and cost model`
9. `## Observability and safe diagnosis`
10. `## Security and ownership boundaries`
11. `## When this breaks`
12. `## Operational checklist`
13. `## Local fixture exercise`
14. `## Questions and answers`
15. `## Evidence and scope`

The topic's metadata must state SDE1, SDE2, and Staff scope and name an
expected artifact: an AI-fabric design and verification record containing a
topology/rail map, workload assumptions, capacity worksheet, failure-domain
map, evidence plan, owners, rollout, rollback, and stop condition.

## 4. Theory curriculum requirements

### 4.1 Planes, state, and ownership

The mental model must show that an accelerator cluster is several interacting
systems. It must distinguish each state from the packet path instead of saying
that “the network” owns all outcomes.

| State model | Authoritative state | Consumer | Failure question |
| --- | --- | --- | --- |
| Job admission | requested resources, priority, quota, identity, and placement constraints | Scheduler and tenant | Was a job admitted or placed into an unsuitable failure domain? |
| Rank membership | rank-to-process/device/host map and collective membership/epoch | Runtime/job controller | Did a missing or slow rank block synchronization? |
| Rail/topology | host-to-NIC-to-leaf/spine reachability and eligible equal-cost paths | Fabric control plane | Is a rank using an intended rail/path, and is that state converged? |
| Congestion | offered load, queue occupancy, marking/pause state, loss/recovery observations | Host/fabric telemetry | Is congestion causal, correlated, or absent? |
| Storage/checkpoint | data placement, read/write authority, durability, queue depth, throughput and error state | Storage/data platform | Is data movement the limiting path rather than the fabric? |
| Service/inference | request, batch, model version, cache state, deadline, response and error | Serving platform | Is user latency caused by queueing, compute, data, or network? |
| Identity/policy | workload identity, tenant authorization, segmentation and secrets/certificates | Security/service owner | Was access intentionally denied, expired, or misconfigured? |
| Evidence | timestamps, clock quality, metric/log/trace/flow provenance and retention | Observability owner | Can the observed sequence support a causal claim? |

Include a state-transition diagram for job lifecycle:
`SUBMITTED -> ADMITTED -> PLACED -> CONNECTING -> RUNNING -> DRAINING ->
COMPLETED`, plus `BLOCKED`, `DEGRADED`, `FAILED`, and `CANCELLED` branches.
Define the transition authority and minimum evidence for every transition.
The diagram must make clear that fabric reachability alone does not authorize a
job to start and that a completed TCP/IP-level flow alone does not prove a
collective or model-serving success.

### 4.2 Underlay, overlay, and Clos

Explain a leaf-spine/Clos fabric as a scalable set of leaf-to-spine paths that
can support ECMP. Include rack, leaf, spine, border/service, management, and
storage/control roles in a path diagram. Show two logical rails and use labels
such as `rail-a` and `rail-b` rather than a product-specific definition.

Required distinctions:

- **Fact:** Ethernet frames and IP packets have defined layering; IP routing
  and ECMP select forwarding paths according to effective local policy.
- **Engineering inference:** a chosen Clos radix, blocking ratio, LAG/ECMP
  hash, cabling plan, and maintenance domain meet a workload objective only
  after measurement.
- Underlay is the routed physical/logical transport that establishes reachability.
  Overlay is optional encapsulation/control abstraction for isolation or
  mobility; it consumes MTU and introduces control-state dependencies. Neither
  implies a specific vendor implementation.
- Include MTU accounting, BUM/control traffic boundary, ECMP symmetry caveat,
  failure-domain mapping, and a note that fabric management and data-plane
  reachability are different paths.

The normal-path Mermaid diagram must be ASCII-only and start with the
repository light-theme/dark-text init directive. It needs two training ranks,
two host NIC rails, two leaves, two spines, a storage service, and a scheduler
or control service. It must avoid Unicode arrows, symbols, or smart quotes.

### 4.3 Ethernet/IP, RDMA/RoCE/InfiniBand terminology

Use the following matrix and keep its evidence boundary explicit.

| Term | Teaching meaning | Label and release boundary | Do not infer |
| --- | --- | --- | --- |
| Ethernet/IP | General packet/frame and routed-fabric vocabulary used by the portable model. | **Fact** only when tied to a cited standard/RFC; platform forwarding behavior is release-specific. | That identical QoS, buffer, or ECMP behavior exists on all Ethernet gear. |
| RDMA | A family of direct-memory-access communication concepts and implementations used in high-performance workloads. | **Vendor terminology** unless a cited implementation/standard establishes the exact behavior. Pin NIC, OS, driver, and runtime release. | That RDMA by itself guarantees losslessness, latency, ordering, security, or performance. |
| RoCE | A named RDMA-over-Ethernet technology family. | **Vendor terminology** with official vendor/release documentation and topology verification. | That a RoCE version, congestion control, PFC policy, counters, or configuration is interchangeable across vendors. |
| InfiniBand | A named fabric technology/ecosystem with its own architecture and management terminology. | **Vendor terminology** with official specification/vendor release boundary. | That its addressing, routing, congestion, partitioning, or operations map one-to-one to Ethernet/IP. |

Explain why naming technology is not a substitute for declaring the actual
transport, control plane, addressing, congestion behavior, telemetry source,
and test boundary. Do not provide commands to configure any technology.

### 4.4 ECN, PFC, queues, and congestion control

Use a causal chain, not a tuning guide:

`offered load -> egress contention -> queue growth -> marking/pause/loss ->
sender/runtime reaction -> rank or request delay -> job or SLO symptom`.

Define ECN as congestion signaling where applicable, PFC as priority-scoped
link-level pause behavior in relevant Ethernet deployments, and congestion
control as a sender/network response policy. Explain that all are conditional
on standards, hardware, configuration, and software release. The content must
include microbursts, head-of-line blocking risk, pause propagation, false
attribution from counter correlation, and why average utilization can hide a
tail event. It must not prescribe thresholds, buffer reservations, QoS maps,
or enablement steps.

Provide a table mapping observation to competing explanations and falsifiers:
queue/mark counter increase, pause counter increase, retransmission/retry or
runtime stall, one-rail skew, storage latency, and clock/timestamp mismatch.

### 4.5 Training, inference, and collective communication

Describe, compare, and keep separate:

| Dimension | Training | Inference |
| --- | --- | --- |
| Dominant success measure | Job throughput, step time, utilization, completion/cost subject to correctness. | Request availability, tail latency, quality/correctness, and cost per useful response. |
| Common traffic shape | Often sustained east-west exchanges plus bursts/checkpoints; exact shape depends on model, parallelism, and runtime. | Usually client-to-service and service-to-service traffic, batching/queueing, and model/data/cache movement; exact path is deployment-specific. |
| Synchronization risk | A slow or unavailable rank can delay a collective phase. | A slow shard, queue, dependency, or cache path can affect a request cohort. |
| Capacity question | How many concurrent jobs and collective phases fit with failure headroom? | How many requests, tokens, batches, or sessions fit within tail-SLO and degradation policy? |

Teach all-reduce, all-gather, reduce-scatter, ring, tree, hierarchical, and
topology-aware communication as abstract patterns. Include a simple two-phase
example and state that an actual collective runtime/library selects algorithms
according to its own version and environment. Cover GPU/accelerator-to-host,
host-to-rack, rack-to-fabric, and cross-domain communication boundaries without
asserting a universal hardware hierarchy.

Explain model-weight distribution, checkpoint traffic, and KV-cache movement
as possible inference-related data paths. State that cache ownership,
replication, invalidation, residency, and transport must be determined from
the serving design; the term does not prove remote cache movement occurs.

### 4.6 Storage, control plane, observability, capacity, cost, and security

The topic must make storage and control-plane networking first-class:

- Storage: ingestion, training data reads, checkpoints, model artifact
  distribution, replication/durability, queueing, and access policy.
- Control plane: scheduler, registry, DNS/service discovery, identity,
  configuration, admission/quota, orchestration, telemetry collection, and
  their failure modes.
- Observability: correlate job/runtime events, rank maps, host/NIC data,
  fabric/control state, queue/congestion signals where authorized, storage
  metrics, traces/logs, and synthetic fixture checks. Record timestamp origin,
  clock confidence, cardinality, sampling, retention, tenancy/privacy, and
  whether a source is measured or inferred.
- Capacity/cost: use variables for accelerator count, rails, link capacity,
  effective bandwidth, oversubscription, usable headroom, job concurrency,
  checkpoint bandwidth, failure reserve, power/cooling, ports/optics, storage,
  cross-domain transfer, and operator complexity. Calculate a bound and show
  a sensitivity table, avoiding real-price claims.
- Security: include tenant/project segmentation, management-plane isolation,
  workload identity, least privilege, data/model/checkpoint access, secrets,
  telemetry privacy, supply-chain context, and incident authority. Include
  fail-closed, queue, degrade, and shed-work decision boundaries.

## 5. Required worked models

### 5.1 Capacity worksheet

Use fictional values and show units. Required equations:

```text
usable_fabric_bandwidth = installed_bandwidth * utilization_guardrail
required_training_bandwidth = concurrent_jobs * per_job_peak * overlap_factor
failure_safe_bandwidth = usable_fabric_bandwidth - largest_planned_failure_domain
headroom_ratio = failure_safe_bandwidth / required_training_bandwidth
communication_lower_bound_seconds = payload_bytes / effective_bytes_per_second * phases
```

State that `overlap_factor`, `utilization_guardrail`, effective bandwidth,
largest planned failure domain, and phases are assumptions to validate. The
answer must not present `communication_lower_bound_seconds` as a measured
step time. Include an inference showing how a job-placement or rail imbalance
can reduce effective bandwidth despite unchanged installed capacity.

### 5.2 State and failure models

Provide a table for these required failure states. Every row names the symptom,
direct evidence, competing hypotheses, safe local test, owner, reversible
action, and irreversible stop condition.

| State | Required scenario |
| --- | --- |
| `RAIL_SKEW` | One rail carries disproportionate traffic or a rank mapping is uneven. |
| `PATH_UNAVAILABLE` | A link/member or route/control state removes an eligible path. |
| `MTU_INCOMPATIBLE` | Effective MTU is smaller than an assumed payload/encapsulation path. |
| `QUEUE_PRESSURE` | Offered load creates queue/marking/pause behavior in the model. |
| `STORAGE_BOUND` | Checkpoint/data latency dominates apparent job delay. |
| `PLACEMENT_SKEW` | Scheduler placement creates resource or topology contention. |
| `CONTROL_BLOCKED` | DNS, identity, policy, or scheduler control path blocks start. |
| `OBSERVABILITY_AMBIGUOUS` | Sampling, missing telemetry, or clock offset prevents a causal assertion. |

Required irreversible stop conditions include: a tenant/security boundary is
violated; evidence suggests potential data corruption or unsafe authority;
the simulated change broadens beyond its declared fault scope; or a defined
service/job SLO breach persists after the bounded rollback. Do not call an
automatic retry a rollback.

## 6. Practical fixture specification

### 6.1 Baseline scenario

The fixture's baseline uses only fictional identifiers:

```text
cluster: atlas-lab
hosts: gpu-a1, gpu-a2, gpu-b1, gpu-b2
rails: rail-a, rail-b
leaves: leaf-a, leaf-b
spines: spine-1, spine-2
services: scheduler-1, storage-1, telemetry-1
```

Its semantic topology is four dual-rail hosts, two leaves, two spines, and
separate logical storage/control services. It does not emulate real cabling,
switch ASICs, or GPU devices. A scenario must contain:

- schema/version and deterministic seed;
- declared workload (`training` or `inference`), ranks/requests, phase payloads,
  deadline or step objective, and topology-placement map;
- links with capacity, MTU, availability, and eligible rail/path identifiers;
- congestion policy with named qualitative thresholds or ordinal states, not
  production configuration values;
- storage/control demand and availability;
- an optional one-element fault from the fixed allowlist; and
- expected assertions that reference derived fields, never a desired health
  conclusion.

### 6.2 Output and lifecycle

The runner returns JSON with: input digest; normalized topology; selected paths;
per-link/rail offered load; qualitative queue/congestion state; rank/request
completion estimates; workload result; evidence timeline; hypothesis hints;
ownership boundaries; and a negative-control result. A result must clearly
separate `derived_observation`, `fixture_assumption`, and
`engineering_interpretation`.

Lifecycle phases are `setup`, `baseline-readback`, `fault`, `assertion`,
`repair-readback`, `rollback`, and `cleanup`. A retained bundle has these JSON
files plus `manifest.json` listing SHA-256 values, schema version, correlation
ID, phase order, and cleanup proof. Default mode uses `tempfile` and removes
its workspace. `--artifacts-dir` must reject an absolute path outside the
fixture's `observed/` root and reject traversal components.

### 6.3 Safety and test requirements

The runner must not import networking clients, shell runners, cloud SDKs, or
third-party packages. It must not use `socket`, `subprocess`, `os.system`,
`urllib`, privileged operations, device APIs, environment credentials, or
network namespaces. It must not serialize secrets. A code review should make
the no-external-side-effect boundary obvious.

Tests must demonstrate:

1. Same scenario produces byte-for-byte equivalent normalized result except for
   a documented non-semantic run ID.
2. Missing or invalid topology, unknown rail, negative capacity, invalid MTU,
   multiple faults, or unsupported workload is rejected.
3. Each allowlisted fault yields a derived difference from baseline.
4. Metadata-only input changes can preserve a healthy result (negative
   control), while an independently modeled path/fault change can degrade it.
5. Caller fields such as `healthy`, `root_cause`, `success`, or `outcome` are
   rejected and cannot set a result.
6. Retained phase files have matching manifest hashes and correlation IDs.
7. Temporary and retained runs prove cleanup without deleting unrelated paths.
8. A storage/control fault and a fabric fault can produce similar job symptoms
   but different evidence, preventing single-counter diagnosis.

## 7. Exercise and case-study requirements

The exercise gives a baseline training scenario and one provided fault scenario.
The learner must submit a topology/rail map, workload path, capacity worksheet,
rank-straggler hypothesis tree, evidence order, safe fixture command/output,
repair and rollback choice, and confidence statement. Score separately:

| Criterion | SDE1 | SDE2 | Staff |
| --- | --- | --- | --- |
| Mechanism | Names components and follows a path. | Explains path selection, queueing, and state. | Sets architecture boundaries and assumptions. |
| Evidence | Requests relevant first evidence. | Differentiates hypotheses and falsifiers. | Designs evidence ownership, retention, and decision gates. |
| Quantification | Uses stated units. | Computes capacity/headroom with caveats. | Compares cost, failure reserve, and business trade-offs. |
| Safety | Avoids unsafe production action. | Uses bounded reversible simulation. | Defines migration scope, authority, adoption, and stop conditions. |

The case study begins with a fictional training-step regression and a single
fixture fault. It must include timestamps, initial observations, at least four
competing hypotheses, a false lead, evidence collection order, smallest safe
repair, rollback replay, verification, customer/business effect, and a durable
prevention item. The resolution cannot be “increase buffers,” “enable PFC,”
or “buy more bandwidth” without evidence, a vendor/release boundary, cost,
and alternative analysis.

## 8. Interview bank requirements

Include at least twelve questions in total: four SDE1, five SDE2, and three
Staff. Each must have a direct `**Answer:**`, a likely wrong turn, evidence to
seek, and one follow-up. Required prompts include:

1. SDE1: Draw a training collective path and name data/control/storage paths.
2. SDE1: Explain why a slow rank does not prove the switch is faulty.
3. SDE1: Compare a training and inference symptom in plain language.
4. SDE1: Explain ECN/PFC terms with a version/deployment caveat.
5. SDE2: Compare a nonblocking and oversubscribed Clos design using stated workload assumptions.
6. SDE2: Diagnose one-rail skew versus storage saturation from a given evidence bundle.
7. SDE2: Explain what effective MTU must include and why an overlay changes the question.
8. SDE2: Design telemetry that can correlate rank, host, and fabric evidence without leaking tenant data.
9. SDE2: Make a safe decision when counters rise but SLO impact is absent.
10. Staff: Plan a training-fabric expansion while inference traffic shares constrained resources.
11. Staff: Lead migration from one topology/release boundary to another with adoption, fallback, and procurement risk.
12. Staff: Define ownership and stop conditions for a suspected congestion incident that might be storage or scheduler contention.

Staff answers must explicitly include objective/SLO, stakeholders and ownership,
two viable options, capacity/cost variables, migration stages, communication,
rollback versus forward-repair criteria, and an irreversible-failure stop.

## 9. Evidence, citations, diagrams, and integration

Add a ledger row for the new topic. It must list source category/version
boundary and concrete verification actions, for example inspecting the chosen
release's NIC/switch/runtime documentation and measuring the target topology.
Add associated source entries to `docs/references.md` rather than burying URLs
only in prose. Do not cite a vendor source as proof of another vendor's
behavior.

All diagrams must be Mermaid, ASCII-only, use the repository light theme with
dark text, and have a pedagogical caption that says whether it is a conceptual
model or a fixture model. Required diagrams are:

- Normal topology/path diagram.
- Job/rank and control-state transition diagram.
- Failure/ownership escalation diagram.

After content creation, update the focused-topic index and its topic count,
case-study and exercise indexes, learning path/handoff references if those
documents enumerate all major tracks, and any relevant book/docs navigation.
Extend `scripts/validate.sh` proportionally to assert: the new topic index
entry; topic role/artifact/evidence headings; minimum diagram count/theme;
fixture safety markers; runner/test invocation; and valid local links. The
validator should never inspect live systems or validate volatile vendor claims.

## 10. Definition of done and handoff

Implementation is accepted when every deliverable in section 2 exists, the
topic matches section 3, all required conceptual material is present, the
fixture/test safety rules pass, and the integration requirements are complete.
Luna must run:

```bash
./scripts/validate.sh
python3 examples/request_path.py
python3 book/topics/fixtures/ai-data-center/test_runner.py
python3 book/topics/fixtures/ai-data-center/runner.py --scenario baseline
git diff --check
```

If a command differs because the final fixture interface needs a documented
argument change, the README and validator must be updated together. Before
handoff, report changed paths, topic number, source/release boundaries,
fixture schema and scenario results, validation output, limitations, remaining
assumptions, and rollback point. Commit only after all checks pass. The final
handoff must reiterate that this is an educational model and that actual AI
fabric behavior must be validated against the deployed hardware, software,
topology, workload, and operational controls.
