# AI-era data-center networking implementation plan

## Status, purpose, and boundary

This is the Terra planning artifact for a new, full-detail learning treatment
of AI-era data-center networking. Luna should use the companion
[`ai-data-center-networking-spec.md`](ai-data-center-networking-spec.md) as the
implementation contract. This repository remains a vendor-aware learning
repository, not a production deployment guide or a claim that a particular
accelerator, switch, NIC, provider, or fabric release behaves identically in
all environments.

The treatment explains why AI workloads make familiar data-center decisions
more consequential: synchronized collective phases amplify the slowest rank,
microbursts can create tail latency without sustained-link saturation, and one
lossy or misconfigured path can waste a large job allocation. It teaches the
reader to model and verify those effects. It does not provide instructions to
alter a production lossless fabric, enable PFC, tune congestion-control
thresholds, or run privileged packet capture against a live cluster.

The implementation goal is a connected curriculum spanning theory, safe local
practice, and interviews for SDE1, SDE2, and Staff candidates. The primary
audience is a software, platform, network, or infrastructure engineer who
already knows IP networking and wants to reason credibly about accelerator
clusters without treating vendor terminology as portable protocol behavior.

## Scope and non-goals

### In scope

- A new focused topic for the conceptual and interview treatment.
- A deterministic, standard-library-only local fixture that simulates topology,
  traffic phases, congestion signals, failures, and evidence. It must not open
  sockets, require hardware, credentials, cloud accounts, kernel RDMA support,
  or root privileges.
- A hands-on exercise and answer key based on fixture outputs rather than a
  switch, GPU, DPU, NIC, or storage appliance.
- Clear treatment of Clos/leaf-spine, Ethernet/IP underlay and overlay choices,
  ECMP, GPU/rack/rail topology, training versus inference, collective traffic,
  storage, control planes, observability, capacity/cost, security, and failure
  isolation.
- SDE1, SDE2, and Staff interview prompts with increasing expectations for
  mechanism, evidence, design, ownership, migration, adoption, and risk.
- Ledger, source, index, and validator integration after the teaching material
  exists and has stable headings.

### Non-goals

- A performance claim, tuning recipe, benchmark, or hardware procurement
  recommendation for a real cluster.
- Replacement of vendor release notes, OEM design guides, switch/NIC manuals,
  GPU framework documentation, or local change control.
- Fabric configuration for Ethernet, RoCE, InfiniBand, VXLAN/EVPN, PFC, ECN,
  BGP, routing, telemetry, or storage.
- A claim that RDMA, RoCE, InfiniBand, NCCL, UCC, MPI, Kubernetes, a cloud
  managed AI service, or a vendor feature has the same semantics across
  versions, SKUs, or providers.
- Simulating packet timing, switch buffers, PCIe/NVLink, firmware, DMA,
  GPU kernels, or collective-library internals at physical fidelity. The local
  model is explanatory and deterministic, not a benchmark.

## Learner outcomes and prerequisites

| Level | Completion outcome | Required artifact |
| --- | --- | --- |
| SDE1 | Trace a training or inference request through named control, storage, and data paths; distinguish throughput from latency; identify the first safe evidence to gather. | Annotated path diagram and symptom-to-evidence table. |
| SDE2 | Design and test a bounded fabric model, explain congestion and collective stragglers, quantify a capacity assumption, and propose a reversible repair. | Fixture report, topology/capacity worksheet, and failure hypothesis tree. |
| Staff | Frame a multi-team AI fabric decision, choose failure and ownership boundaries, stage migration/adoption, quantify cost and risk, and define stop conditions. | Design review record with options, rollout, rollback, RACI, and decision gates. |

Prerequisites are the repository's data-center fabrics, BGP/anycast,
overlays, capacity/SLO, observability, Kubernetes/cloud networking, and
retries/backpressure materials. The new topic links to those foundations rather
than repeating their full content. A learner who cannot explain a five-tuple,
ECMP, MTU, congestion, or a control-plane/data-plane distinction should study
the prerequisites before interpreting the AI-specific examples.

## Curriculum architecture

Luna should create one focused topic, one safe fixture area, one exercise, and
one case study. This keeps the conceptual explanation navigable while making
the practical and interview work independently reusable.

| Unit | Planned path | Purpose and mandatory content |
| --- | --- | --- |
| Primary topic | `book/topics/40-ai-data-center-networking.md` | Full theory, diagrams, state models, worked calculations, failure analysis, operations boundary, questions, and an exercise brief. |
| Fixture README | `book/topics/fixtures/ai-data-center/README.md` | Safety model, inputs/outputs, schemas, fixture lifecycle, and interpretation limits. |
| Fixture runner | `book/topics/fixtures/ai-data-center/runner.py` | Deterministic local model with no network/device access; emits JSON evidence bundles. |
| Fixture tests | `book/topics/fixtures/ai-data-center/test_runner.py` | Standard-library tests for topology validation, deterministic results, negative controls, cleanup, and no caller-supplied health outcome. |
| Exercise | `exercises/15-ai-fabric-capacity-and-failure-model.md` | Learner task, input fixture, deliverables, rubric, answer key, SDE2 and Staff follow-ups. |
| Case study | `book/case-studies/20-ai-training-fabric-straggler.md` | Evidence-led incident involving a bounded simulated collective straggler and safe decision process. |

The proposed topic number deliberately follows the maintained 01-39 sequence.
Luna must confirm no number collision immediately before implementation. If a
concurrent addition uses 40, select the next free number and update every
planned reference consistently; do not renumber existing topics.

## Content work packages

### P0: portable model and terminology

The opening topic must separate the following planes and state owners:

| Plane or state | Core question | Representative owner |
| --- | --- | --- |
| Compute/job control | Which workload, rank set, placement constraint, retry, and admission decision is authoritative? | ML platform/scheduler team |
| Fabric control | Which topology intent, routing/ECMP policy, membership, and telemetry configuration is effective? | Network/platform team |
| Host transport | Which NIC/queue pair/transport policy and host limit is active? | Host/platform team |
| Data plane | Which packets or messages traverse which rails and paths at the time of the symptom? | Shared network/compute evidence boundary |
| Storage/data | Where do checkpoints, training data, model weights, and cache pages travel and who owns durability? | Storage/data platform team |
| Security/identity | Which workload identity, tenancy, segmentation, keys, and access policy permit this flow? | Security plus service owner |
| Observability | Which timestamped signal is authoritative enough to support a decision? | SRE/observability owner |

Teach Ethernet/IP as the common packet-underlay vocabulary first: links,
LAG/ECMP, MTU, IP routes, queueing, loss, congestion marking, telemetry, and
failure domains. Teach overlay choices as optional logical isolation or
mobility mechanisms layered over an underlay, not as a requirement for every
AI fabric. Explain Clos/leaf-spine as a topology family that creates multiple
equal-cost paths, while noting that cabling, radix, oversubscription, routing,
buffering, and failure-domain choices determine the realized behavior.

Define RDMA, RoCE, and InfiniBand in a terminology matrix. Mark each as
**Vendor terminology** or release-qualified technology terminology where that
is appropriate; do not imply that an implementation's loss behavior,
congestion algorithm, counters, queue model, deployment rules, or management
surface transfers to another device. Include a prominent rule: product and
framework observations must name the vendor, hardware/software release, NIC
or switch generation when relevant, and the test topology.

### P1: workload and topology reasoning

Build explanations and diagrams for:

- GPU/accelerator hierarchy: process/rank, device, host, NIC, rail, top-of-rack
  or leaf, spine, storage path, and management/control path.
- Rail-aware placement and failure domains. A rail is a design abstraction in
  this curriculum; its exact physical meaning must be declared per vendor and
  topology rather than presumed.
- Training: synchronized collectives, parameter/gradient exchange,
  checkpointing, all-reduce/all-gather/reduce-scatter as communication
  patterns, synchronization sensitivity, and the straggler effect.
- Inference: north-south requests, gateway/load balancing, prefill/decode or
  model-serving stages where applicable, batching/queueing, model/weight
  movement, cache/KV-cache considerations, latency and availability SLOs.
- Storage and control paths: dataset ingestion, checkpoint/read/write traffic,
  image/model distribution, scheduler/API/DNS/identity/telemetry paths. Make
  clear that their criticality, transports, and storage semantics are local
  design choices.
- Collective topology choices: ring, tree, hierarchical, or topology-aware
  communication as explanatory models. State that a library/runtime chooses
  algorithms according to its release and environment; do not teach a fixed
  selection rule as fact.

The main worked model should calculate a lower-bound communication time from
payload, effective bandwidth, and phases; then show why it is not a production
performance prediction. Add a capacity worksheet that makes units, bisection
bandwidth, oversubscription, active-job concurrency, headroom, and failure
load explicit. Require sensitivity analysis rather than a single magic ratio.

### P2: congestion, reliability, and safe diagnosis

Cover ECN, PFC, queueing, microbursts, loss, and congestion control with a
causal model: offered load and queue buildup can lead to marking, pausing,
backoff/recovery, and user-visible job delay; a counter alone does not prove
root cause. Explain why PFC can contain loss for a traffic class but can also
expand congestion failure domains. Do not offer production threshold values.

The topic and case study must use hypothesis/falsifier tables for at least:

1. A slow rank caused by a congested rail or ECMP imbalance.
2. A link/member failure with control-plane convergence or asymmetric reachability.
3. MTU/encapsulation mismatch or PMTU handling failure.
4. PFC pause propagation or congestion-marking growth.
5. A storage/checkpoint bottleneck that resembles a fabric issue.
6. Scheduler placement or noisy-neighbor contention that looks like a network failure.
7. Control-plane, identity, DNS, or certificate failure blocking job start.
8. Telemetry loss, clock skew, or sampling bias creating a false narrative.

For each, provide a safe evidence order: job/runtime timestamp and rank map;
host/NIC counters; fabric path/control state; queue/marking/paused-frame
telemetry if authorized; storage/control-plane evidence; an independent
negative control; then a bounded simulation repair. Observed fixture results
must never be described as a real hardware result.

### P3: security, economics, and operations

Teach segmentation and least privilege across tenant, project, management,
storage, registry, telemetry, and job-control boundaries. Include supply-chain
and image/model access as relevant context, but avoid turning the topic into a
general AI security guide. Require an explicit decision on whether a control
or data-plane failure fails closed, degrades, queues, or sheds work, and who is
authorized to make that call.

The Staff material must account for rack/power/cooling, optics/cabling,
switch/NIC capacity, reserved headroom, power-aware or region-aware placement,
cross-fabric/zone data transfer, lost accelerator time, storage costs, and
operational complexity. Values are variables in the worksheet, never universal
cost claims. Include an uncertainty register and a trigger to revisit a design
when workload mix, hardware generation, or release changes.

### P4: practice and interviews

The fixture shall model, in JSON, a fictional two-spine/two-leaf fabric with
two rails, four hosts, and a separated storage/control path. Inputs include
topology, link capacity, ECMP choices, offered phases, queue limits,
congestion-marking policy, optional pause behavior, and bounded injected
faults. Outputs include a path map, per-rail offered load, queue/marking or
pause state, rank completion estimates, job completion estimate, evidence
timeline, ownership hints, and negative-control comparison.

Fault injection is local data only, selected from a fixed allowlist such as a
single link unavailable, rail imbalance, reduced effective MTU, queue pressure,
storage saturation, scheduler placement skew, or telemetry clock offset. The
fixture cannot accept `healthy`, `root_cause`, `job_success`, or an equivalent
caller-supplied conclusion. It must derive outputs from topology and inputs.
Every execution has setup, baseline, one injected fault, assertion, repair,
rollback, cleanup, and a hash manifest; retained artifacts are optional and
written only below the fixture's local observed directory.

Interview coverage is distributed in the topic, exercise, and case study:

- SDE1: identify components, trace a collective or inference path, interpret a
  basic counter with a caveat, and explain why a network-looking symptom may
  originate elsewhere.
- SDE2: compare Clos and oversubscription choices, map ranks to rails, reason
  about ECN/PFC risk without tuning advice, derive a capacity estimate, debug
  with competing hypotheses, and design a safe local test.
- Staff: define service and job objectives, reconcile training and inference
  priorities, assign cross-team ownership, select a phased migration,
  articulate procurement/cost and adoption trade-offs, and state an
  irreversible-failure stop condition.

## Evidence and source governance

The implementation must follow the repository's `docs/references.md` and
`book/FACT-INFERENCE-LEDGER.md` conventions. Every substantive section should
include all three labels where applicable:

- **Fact:** stable protocol or standards-backed behavior, linked to a primary
  source such as IEEE Ethernet material where licensed/accessible, an RFC, or
  a standards-body publication.
- **Vendor terminology:** a named vendor, product, framework, cloud, NIC,
  switch, accelerator, or library term. Link to the primary documentation and
  pin the observed version/release boundary.
- **Engineering inference:** a design, operating, capacity, or troubleshooting
  conclusion that depends on workload, topology, measured evidence, and local
  risk tolerance.
- **Observed lab result:** only for the deterministic local fixture; name the
  fixture schema/version, scenario input, and artifact path. It must not be
  generalized to hardware behavior.

Luna must add a focused-topic ledger row with sources and verification steps,
then add only claims that can be supported by the selected primary sources.
Candidate source categories include IETF RFCs for IP/ECN and transport,
standards bodies for Ethernet where available, official InfiniBand Trade
Association material, official vendor documentation for RoCE/NIC/switch
behavior, and official framework/library documentation for collective or
orchestration behavior. Current product behavior is release-specific; no
release-sensitive sentence may be written without an explicit version boundary
and verification instruction. Source snippets or vendor marketing are not
sufficient evidence for a portable fact.

## Integration sequence and acceptance gates

Luna must make changes in this sequence to keep documentation and validation
consistent:

1. Create the topic and fixture README using the required headings and evidence
   labels.
2. Implement the local runner and tests, then run it in temporary mode and in a
   temporary artifact directory.
3. Add the exercise and case study, with answer key and role-tagged prompts.
4. Add the topic to `book/topics/README.md`, the broader book/docs navigation
   where comparable topics are indexed, and the learning path/handoff only if
   their current conventions call for new curriculum entries.
5. Add the ledger row and references-map additions, with primary links and
   release/verification boundaries.
6. Extend validator checks only for durable structural contracts: topic index
   parity, required role labels/artifact, evidence labels/link, fixture safety
   contract, Mermaid theme/ASCII requirements, and local links. Do not encode
   volatile vendor facts into the validator.
7. Run all repository-required validation and review the changed-file list
   against this plan before commit.

| Gate | Proof required |
| --- | --- |
| Scope | Only planned curriculum, evidence, index, fixture, exercise/case-study, and validator files changed; no production configuration. |
| Content | Topic has objectives, prerequisites, role scope, mental model, state models, diagrams, calculation, failures, security, operations, exercise, and at least eight explained Q&A. |
| Practice safety | Runner is stdlib-only, local/offline, deterministic, no socket/device/cloud access, no secrets, allowlisted faults, derived outcomes, retained-manifest verification, and cleanup proof. |
| Interview quality | Prompts are tagged SDE1/SDE2/Staff; answers distinguish observation from inference and include a common wrong turn plus evidence/follow-up. |
| Evidence | Fact, vendor terminology, engineering inference, and observed-lab boundaries are present; ledger and references include primary sources and release-specific verification. |
| Portability | Mermaid is ASCII-only with repository light theme/dark text; links and anchors are valid; terminology map does not claim equivalence. |
| Verification | `./scripts/validate.sh`, the Python request-path example, fixture tests/runner, and `git diff --check` pass. |

## Rollback and handoff

Documentation and fixture changes should land as one reversible commit where
practical. If a required acceptance gate fails, Luna should not update indexes
or validators to claim completion; revert only the new AI data-center files
from the candidate change, retain the failure evidence in the implementation
notes, and return to the smallest failed work package. Never delete a user
artifact outside the dedicated fixture output directory.

The implementation handoff must report: exact files changed; the selected
topic number; tested fixture scenario names; source and release boundaries;
validation commands/results; known model limitations; and any deliberate
deferrals. It must state explicitly that the materials are educational and
that production behavior requires vendor-release, hardware, topology, and
workload validation.
