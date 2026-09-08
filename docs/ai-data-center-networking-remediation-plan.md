# AI data-center networking remediation plan

## Status and decision

This is the Terra remediation plan for the AI-era data-center networking
curriculum introduced in commit `9b02668`. It is an implementation-ready
contract for Luna. This plan itself is the only change authorized in the Terra
planning pass. Luna may make the implementation changes enumerated below only
after this plan is accepted.

The curriculum remains an educational, deterministic, offline model. It must
teach readers how to form and test hypotheses; it must not become a production
network runbook, a hardware benchmark, a configuration recipe, or a claim
about a particular vendor's behavior.

The review found that the theory and interview material are broadly complete,
but the practical fixture does not yet satisfy its own claim that observations
derive from its topology and scenario state. The remediation therefore starts
with model correctness and proof of execution before expanding content.

## Scope, ownership, and file map

### Luna implementation scope

| Priority | Files Luna changes | Outcome |
| --- | --- | --- |
| P0 | `book/topics/fixtures/ai-data-center/runner.py` | Schema-v2 graph, state-derived outcomes, evaluated assertions, and observable lifecycle behavior. |
| P0 | `book/topics/fixtures/ai-data-center/test_runner.py` | Regression, topology, fault-state, assertion, lifecycle, and manifest-verification tests. |
| P0 | `book/topics/fixtures/ai-data-center/README.md` | Accurate schema/lifecycle/artifact contract and safe execution examples. |
| P1 | `book/topics/fixtures/ai-data-center/runner.py` | Independent workload objective, evidence confidence, and an inference workload model. |
| P1 | `book/topics/fixtures/ai-data-center/test_runner.py` | Objective/evidence and inference-specific contract tests. |
| P1 | `book/topics/fixtures/ai-data-center/README.md` | Training and inference input/output definitions and interpretation limits. |
| P1 | `book/topics/40-ai-data-center-networking.md` | Version-bounded terminology and practical-inference cross-reference. |
| P1 | `book/case-studies/20-ai-training-fabric-straggler.md` | Schema-v2 fixture references only if existing schema/version claims change. |
| P1 | `exercises/15-ai-fabric-capacity-and-failure-model.md` | A safe inference exercise variant and schema-v2 output interpretation. |
| P1 | `docs/references.md` | Version/release/date boundaries and verification procedure for vendor terminology. |
| P1 | `book/FACT-INFERENCE-LEDGER.md` | Version-qualified evidence row and explicit re-verification fields. |
| P2 | `book/topics/40-ai-data-center-networking.md` | Transition-authority and capacity-sensitivity tables. |
| P2 | `book/topics/fixtures/ai-data-center/README.md` | "write-once, hash-manifested" wording and manifest-verification command. |
| P2 | `exercises/README.md` | Correct the AI-fabric entry label from Exercise 7 to Exercise 15. |

### Explicitly out of scope

- `scripts/validate.sh` and every other script outside the fixture are not
  changed by this remediation. Existing repository validation remains the
  gate; fixture-specific tests supply the new semantic coverage.
- No live devices, sockets, cloud APIs, credentials, privileged commands,
  RDMA libraries, packet capture, GPU jobs, or hardware counters are used.
- No PFC, ECN, QoS, switch-buffer, NIC, routing, or collective-library tuning
  values are introduced. The fixture remains qualitative and fictional.
- Do not renumber topics, exercises, case studies, or change unrelated
  curriculum material.

### Implementation order and rollback point

Luna works in this order: P0 graph and derivation model; P0 tests and lifecycle
proof; P1 objective/evidence separation; P1 inference and evidence boundaries;
P2 documentation accuracy and tables. After each priority group, run the
fixture tests and the repository-required checks. Commit boundaries should be
separate by priority so P1 or P2 can be reverted without restoring a known
incorrect P0 model.

If a P0 replacement cannot preserve deterministic JSON output for equivalent
baseline inputs, stop at the failing fixture test. Revert only the incomplete
Luna change set, retain the current educational fixture as the last known
baseline, and do not publish schema-v2 references. Never paper over a failed
derivation with a fault-name special case.

## P0: make the fixture model true to its declared state

### P0.1 Topology and path consistency

**Files:** `runner.py`, `test_runner.py`, `README.md`.

Replace the implicit fixed-path assumption with a validated graph model. The
current schema allows an attachment such as `gpu-b1 -> leaf-b` on `rail-a`,
while only `leaf-b` links on `rail-b` are declared; `_path_map()` nevertheless
selects a nonexistent leaf/spine/rail combination. Schema-v2 must prevent such
paths rather than documenting around them.

Use the following state representation:

| State object | Required fields | Rule |
| --- | --- | --- |
| `host_attachment` | `host`, `rail`, `leaf` | One attachment for every `(host, rail)` pair; the leaf must be declared. |
| `link` | `id`, `from`, `to`, `rail`, `capacity_bps`, `mtu`, `available` | Endpoints must be declared leaves/spines; IDs unique; capacity and MTU valid. |
| `eligible_links` | derived list of link IDs | A link is eligible only when available, on the rank rail, and attached to the rank's leaf. |
| `selected_path` | rank, host, rail, leaf, spine, link ID, path nodes | Select deterministically from eligible links; no hop may be emitted unless represented by the graph. |
| `per_link_load` | link ID, offered load, capacity, utilization | Allocate each rank's rail share to its selected eligible link; report zero for an available but unused link. |

Luna may choose either of these equivalent designs, but must document the
choice in the fixture README:

1. Make each leaf participate in both rails by declaring every required
   leaf-spine rail member; or
2. Keep rail-specific leaf membership, but constrain every host attachment to
   a leaf that has an eligible link on the same rail.

The runner must build an adjacency/index from declared links, derive eligible
links for each rank, select an ECMP member deterministically from the scenario
seed plus rank, and include the selected `link_id` in output. `validate_scenario`
must reject a topology in which any declared rank has no available path on its
rail. It must also reject duplicate link IDs, links with invalid endpoint
classes, and rail/attachment combinations with no declared eligible member.

Do not claim that this is a physical forwarding implementation. The graph is a
small explanatory model of a two-hop leaf-spine path, not a routing protocol,
ASIC queue, or collective algorithm.

### P0.2 Derived fault semantics

**Files:** `runner.py`, `test_runner.py`, `README.md`.

Make fault injection a state mutation followed by normal derivation. A fault
name is a test-input shorthand, never evidence and never a branch that creates
the outcome by itself. Implement a pure transformation such as
`apply_fault(baseline_state, fault) -> mutated_state`, then derive baseline,
fault, repair, and rollback from that state through the same graph, capacity,
MTU, dependency, and objective functions.

| Allowlisted fault | Only permitted mutation | Required derived consequence |
| --- | --- | --- |
| `none` | No mutation | Baseline state derives normally. |
| `link_unavailable` | Mark one deterministic declared link unavailable. | Paths reselect among remaining eligible members, or the affected ranks become unreachable when no member remains; capacity/load follows selected links. |
| `rail_imbalance` | Change a declared workload rail-demand distribution. | Per-link and per-rail offered load changes through normal allocation. |
| `mtu_reduced` | Reduce the MTU of one selected/eligible declared link. | Effective path MTU is the minimum along the selected path; payload/required-MTU incompatibility is derived without checking the fault label. |
| `queue_pressure` | Increase a declared offered-load input. | Link utilization and ordinal queue state derive from load/capacity/policy. |
| `storage_saturation` | Reduce storage capacity or increase storage demand. | Storage bound derives independently of fabric path health. |
| `placement_skew` | Change rank-to-rail or rank-to-leaf workload placement within validated topology. | Selected links and load distribution reflect the mutated placement. |
| `control_blocked` | Set one required control dependency unavailable. | Admission/connectivity state blocks according to dependency rules. |
| `telemetry_clock_offset` | Reduce timestamp ordering confidence only. | Workload health remains derived from workload state; attribution confidence becomes low/inconclusive. |
| `pause_propagation` | Enable a policy plus a derived overloaded traffic class/path. | Pause state is possible only when the policy is enabled and the derived threshold condition exists. |

`identity_available` and `dns_available` are required dependencies, not dead
fields. Define their effect precisely: either false value blocks the relevant
admission/connection state with a dependency-specific evidence signal. Likewise
`pause_enabled` changes the derived pause eligibility and cannot be ignored.

The P0 output must include both `effective_state` (the normalized state after a
bounded mutation) and `derived_observation`. This makes it possible to teach
the difference between an injected scenario condition and a conclusion.

### P0.3 Executed assertions

**Files:** `runner.py`, `test_runner.py`, `README.md`.

Define an assertion grammar and execute it after fault derivation. Permit only
safe, read-only comparison operators: `eq`, `ne`, `lt`, `lte`, `gt`, `gte`,
`contains`, and `exists`. Values are looked up from a fixed output allowlist:

- `workload_result.health_state`
- `workload_result.objective_state`
- `workload_result.deadline_met`
- `evidence_assessment.confidence`
- `derived_observation.effective_mtu`
- `derived_observation.control_dependencies.<name>`
- `derived_observation.selected_paths`
- `derived_observation.per_link_load.<link-id>.state`
- `derived_observation.storage_bound`

Reject unknown paths, malformed operators, type-incompatible comparisons, and
assertion objects with extra executable-like fields. The assertion phase must
return one result per supplied assertion, with `passed`, actual value, expected
value, and a deterministic explanation. A failed assertion must make the
scenario result `assertion_state: "FAILED"`; `run_scenario` must raise a
documented `AssertionError` or return a non-success execution result, selected
consistently and tested. The CLI must exit nonzero for a failed assertion.

The baseline remains a scenario with assertions, but a deliberately false
expectation must not be silently accepted. Negative-control assertions remain
separate from learner-provided assertions.

### P0.4 Real lifecycle and cleanup proof

**Files:** `runner.py`, `test_runner.py`, `README.md`.

Replace hard-coded cleanup claims with observable lifecycle state. Use an
actual temporary workspace for default runs and write phase data there before
reading it back and removing it. Return a lifecycle record containing:

- workspace mode (`temporary` or `retained`),
- a generated workspace/bundle identifier, not an absolute host path,
- phase write/read completion booleans,
- cleanup attempted/completed booleans, and
- `exists_after_cleanup`, obtained after deletion.

For retained bundles, preserve data only under the existing scoped `observed/`
root and never overwrite files. Replace all claims of "immutable" with
"write-once, hash-manifested". Add `verify_bundle(path)` that recomputes every
phase hash, validates manifest phase order/schema/correlation ID, and returns
a pass/fail report. The manifest is evidence of integrity checking, not proof
that a local user could never alter a file.

The retained lifecycle includes setup, baseline, fault, assertion, repair,
rollback, and cleanup records. Repair must derive from an explicitly restored
state; rollback must prove the fault mutation was removed by comparing a
stable baseline fingerprint with the post-rollback derived fingerprint. A
retained cleanup record must truthfully say that the retained bundle remains
by user request while transient workspace material was removed.

## P1: complete operational semantics and practical coverage

### P1.1 Separate workload objectives from evidence confidence

**Files:** `runner.py`, `test_runner.py`, `README.md`,
`book/topics/40-ai-data-center-networking.md`.

Replace the overloaded workload `status` with independent result dimensions:

| Dimension | Values | Derived from | Must not be derived from |
| --- | --- | --- | --- |
| `health_state` | `COMPLETED`, `DEGRADED`, `BLOCKED`, `FAILED` | Reachability, dependency, MTU, storage, and congestion state. | Telemetry-clock confidence alone. |
| `objective_state` | `MET`, `MISSED`, `NOT_EVALUABLE` | Workload-specific objective calculation and health state. | A fault name. |
| `deadline_met` | `true`, `false`, `null` | Completion estimate versus declared deadline. | Evidence confidence. |
| `evidence_assessment.confidence` | `HIGH`, `MEDIUM`, `LOW` | Timestamp ordering and model-evidence completeness. | Workload health result. |
| `evidence_assessment.attribution_state` | `SUPPORTED`, `INCONCLUSIVE` | Confidence plus independent signals. | A direct root-cause label. |

For training, calculate the step completion estimate from modeled phase work,
selected-path capacity, derived queue factor, and independently derived storage
or MTU effects. Compare it to `step_deadline_seconds`, including a deadline
smaller than the baseline estimate. For a blocked workload, deadline is `null`
and objective is `NOT_EVALUABLE`, unless the scenario explicitly defines an
admission-time objective.

For telemetry clock offset, retain the same health/objective result as the
equivalent workload state, reduce evidence confidence, and mark attribution
`INCONCLUSIVE`. This teaches the correct diagnosis boundary: weak telemetry
limits causal attribution; it does not itself prove application degradation.

### P1.2 Add a bounded inference scenario

**Files:** `runner.py`, `test_runner.py`, `README.md`,
`exercises/15-ai-fabric-capacity-and-failure-model.md`,
`book/topics/40-ai-data-center-networking.md`.

Implement a second schema-v2 workload branch for `kind: "inference"`. It uses
the same fictional topology and offline state model, but it must not reuse a
training rank/step deadline as its only semantics. Minimum inference fields:

| Input | Meaning |
| --- | --- |
| `requests` | Positive count of fictional requests in the modeled cohort. |
| `batch_size` | Positive bounded batch size used to derive batches/queue work. |
| `arrival_rate_rps` | Qualitative offered request rate. |
| `target_p99_seconds` | Synthetic tail-latency objective. |
| `stages` | At least gateway, prefill, decode, and model/cache dependency fields with positive synthetic work estimates. |
| `model_cache_available` | Required serving dependency; false produces a dependency-specific outcome. |

The inference result must report request count, batches, estimated p50/p99
completion, target p99, objective state, queue state, selected service/fabric
path, and whether the blocker is fabric, model/cache, or another dependency.
It remains a simple deterministic teaching calculation, not an LLM latency
predictor. Include at least one non-network competing fault, such as an
unavailable model/cache dependency or prefill-stage saturation. The exercise
must require comparison with a fabric fault so the learner cannot attribute a
tail-latency symptom to the network by default.

### P1.3 Establish release/version evidence boundaries

**Files:** `docs/references.md`, `book/FACT-INFERENCE-LEDGER.md`,
`book/topics/40-ai-data-center-networking.md`, `README.md`, and the case study
only where it names vendor/runtime terminology.

For each release-sensitive term or claim about NCCL, RoCE, RDMA, InfiniBand,
rail behavior, collective selection, or lossless Ethernet, use one of these
acceptable evidence patterns:

1. A primary, versioned vendor/standards document with product/runtime version
   and documentation date/revision; or
2. A clearly marked unpinned terminology entry with a concrete verification
   procedure: record runtime, driver, firmware, NIC/switch generation, topology,
   documentation revision/date, and authorized test evidence before relying on
   the term operationally.

Add fields or prose labels equivalent to `source version/revision`,
`verified on`, and `re-verification trigger`. The trigger includes a runtime,
driver, firmware, hardware, topology, provider, or workload-mix change. Do not
retroactively state that generic current documentation proves any behavior.

## P2: finish Staff-level artifacts and documentation accuracy

### P2.1 Transition authority table

**File:** `book/topics/40-ai-data-center-networking.md`.

Add a table immediately following or replacing the current conceptual state
diagram. It must cover `SUBMITTED -> ADMITTED`, `ADMITTED -> PLACED`,
`PLACED -> CONNECTING`, `CONNECTING -> RUNNING`, `CONNECTING -> BLOCKED`,
`RUNNING -> DEGRADED`, `DEGRADED -> RUNNING`, `RUNNING -> DRAINING`,
`DRAINING -> COMPLETED`, and terminal failure/cancellation transitions.

For every transition, specify the authoritative owner, minimum evidence,
whether the state is fail-closed/degrade/queue/shed, and safe behavior when
evidence is missing or contradictory. Names such as ML platform, network
platform, storage, identity/security, and service owner are role boundaries,
not real organizations or product controls.

### P2.2 Capacity sensitivity table

**File:** `book/topics/40-ai-data-center-networking.md`.

Add a compact table based on the existing fictional capacity worksheet. Include
at least four rows varying one assumption at a time: utilization guardrail,
concurrent jobs, workload overlap, and largest failed rail/member capacity.
Show resulting usable/failure-safe bandwidth and headroom classification. Mark
all values as synthetic inputs, show units, and state that the table is a
sensitivity exercise rather than a procurement recommendation.

### P2.3 Correct lifecycle and index language

**Files:** `book/topics/fixtures/ai-data-center/README.md`,
`exercises/README.md`.

Rename "immutable artifact" and "immutable manifest" language to
"write-once, hash-manifested bundle." Explain that subsequent manifest
verification detects changed phase content only while the verifier and
manifest are trustworthy. Correct the exercises index row to `15.`.

## Required Luna test matrix

All tests use Python standard library only, fictional inputs, and no external
access. Add these to `test_runner.py`; retain useful existing tests after
updating their expected schema/status names.

| ID | Scenario | Required assertion |
| --- | --- | --- |
| T01 | Baseline training | Every selected path has an existing available link of the same rail and attached leaf; per-link loads sum to per-rail loads. |
| T02 | Alternate valid attachment/topology | Deterministic ECMP selection uses only eligible declared members; no hard-coded spine choice leaks through. |
| T03 | Missing compatible leaf/rail member | Validation rejects the scenario before execution. |
| T04 | Single selected link unavailable with alternate member | Fault mutation changes effective state; selected path reroutes; affected load/capacity changes from topology. |
| T05 | All eligible members unavailable | Affected ranks are unreachable and workload health is `BLOCKED` or `FAILED` under documented semantics. |
| T06 | Lower an MTU directly with fault `none` | Effective path MTU and MTU compatibility change; result does not depend on the `mtu_reduced` label. |
| T07 | Disable DNS or identity directly | Admission/connection blocks with dependency-specific evidence, proving both inputs are live. |
| T08 | Enable pause with derived overload; then disable pause | Pause is present only in the eligible policy/state combination. |
| T09 | Telemetry clock offset | Health/objective match equivalent workload state; confidence is lower and attribution is `INCONCLUSIVE`. |
| T10 | Deadline shorter than baseline estimate | Health can remain completed while `deadline_met` is false and objective is `MISSED`. |
| T11 | Deliberately false expected assertion | Assertion outcome fails and CLI/execution is non-success; actual/expected/operator are returned. |
| T12 | Valid comparison operators | Each supported operator succeeds/fails deterministically; unknown path/operator/type mismatch is rejected. |
| T13 | Temporary execution | Real phase files are written/read in a temporary workspace and the workspace is absent after cleanup. |
| T14 | Retained execution | Phase files, manifest, repair, rollback, and truthful retained cleanup record exist under scoped `observed/`. |
| T15 | Manifest tamper | Modify a retained phase file in the test workspace; `verify_bundle` returns failure and names the mismatch. |
| T16 | Repair and rollback | Fault state differs from baseline; repair/rollback re-derive baseline-equivalent output fingerprint. |
| T17 | Baseline inference | Request/batch/stage fields produce p50/p99 and a met/missed objective independently of training rank semantics. |
| T18 | Inference model-cache or prefill fault versus fabric fault | Both can affect tail objective, but output evidence/ownership/blocker differ. |
| T19 | Determinism | Equivalent scenario inputs produce canonical-equivalent semantic output after excluding generated run/workspace IDs. |
| T20 | Caller-supplied conclusion | Existing forbidden conclusion-field rejection still holds for both training and inference branches. |

## Acceptance criteria

Luna may mark this remediation complete only when all conditions below are
true.

1. The fixture declares a schema-v2/version migration and rejects any path
   that its own graph cannot carry.
2. Every reported selected hop/link is graph-backed, rail-compatible,
   attachment-compatible, and represented in per-link load output.
3. Faults mutate one bounded input state and all affected results are derived
   from that state. Direct changes to MTU, dependencies, availability, and
   pause policy have the documented effects without relying on a fault name.
4. Learner assertions execute, produce per-assertion evidence, and make an
   intentionally false scenario fail visibly.
5. Temporary and retained lifecycle records are based on actual writes,
   read-backs, cleanup, and post-cleanup inspection. Hash verification detects
   a modified retained phase; no "immutable" claim remains.
6. Workload health, objective attainment/deadline, evidence confidence, and
   attribution confidence are independent fields with documented semantics.
7. Both training and inference have executable local scenarios. Inference
   covers requests, batching, tail objective, service stages, model/cache
   dependency, and a non-network competing fault.
8. Release-sensitive terminology is version-pinned or explicitly unpinned
   with a date/version capture and re-verification procedure.
9. The topic contains the transition-authority and capacity-sensitivity tables,
   and the exercise index calls the AI fabric work Exercise 15.
10. `python3 book/topics/fixtures/ai-data-center/test_runner.py`,
    `./scripts/validate.sh`, `python3 examples/request_path.py`, and
    `git diff --check` all pass. No validator script is modified for this
    remediation.

## Safe educational boundaries and handoff

Every changed learner-facing file must preserve these boundaries:

- The topology, hosts, capacities, workload values, rack/rail names, and
  evidence are synthetic. Output is an **Observed lab result** only for the
  stated schema, runner version, scenario, and retained artifact if present.
- A path model, capacity formula, or queue state is not a prediction of ASIC,
  NIC, GPU, runtime, or production behavior.
- Vendor terminology must be clearly distinct from portable fact and
  engineering inference. It must carry a release verification boundary.
- No production commands, configuration thresholds, procurement decisions, or
  privileges are added. Changes are local deterministic computation and
  documentation only.
- A weak clock/evidence signal produces uncertain attribution, not an invented
  root cause. A scenario fault is a controlled premise, not proof about a
  deployment.

Luna's handoff must report the schema/runner version, the test-matrix result,
the four repository-required checks, any compatibility behavior retained for
schema-v1 inputs, and the exact docs where release evidence was pinned or
marked unpinned. If any P0 criterion cannot be demonstrated with a test, the
handoff must say the curriculum remains incomplete and must not claim full
practical coverage.
