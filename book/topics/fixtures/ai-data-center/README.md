# AI data-center networking fixture

This fixture is a deterministic, standard-library-only teaching model for
topic 40, not a switch, NIC, GPU, RDMA, RoCE, InfiniBand, or performance
benchmark. Schema `ai-fabric-fixture/v2` uses only fictional identifiers
(`atlas-lab`, `gpu-a1` through `gpu-b2`, two leaves, two spines, and two
logical rails). It never contacts a device, cloud, service, account, or
external endpoint and it does not require privileges, credentials, kernel
support, or third-party packages. Schema-v1 (`ai-fabric-fixture/v1`) inputs are
rejected explicitly;
there is no compatibility claim for their path or lifecycle semantics.
For repository compatibility, the no-input bare `--scenario baseline` CLI
presentation retains a v1 envelope and a v2 `fixture_schema` marker; the
underlying `run_scenario` result, retained artifacts, inference branch, and
custom-input CLI outputs are schema-v2. This shim does not reinterpret v1
inputs or alter derived state.

## Safety and interpretation

The model derives observations from declared topology, qualitative load, MTU,
storage, control, and one allowlisted fault. The graph declares every leaf,
spine, rail member, attachment, and link ID. A selected path is emitted only
when its link is declared, available, rail-compatible, and attachment-
compatible; per-link load includes available but unused members. Fault names
mutate bounded state before normal derivation. It does not accept caller-supplied
`healthy`, `root_cause`, `success`, `outcome`, or equivalent conclusions.
`**Observed lab result:** an output is valid only for schema
`ai-fabric-fixture/v2`, runner `2.0.0`, the supplied fictional scenario, and
the generated local artifact; it must not be generalized to hardware behavior.

**Fact:** the fixture is local Python computation. **Engineering inference:**
the outputs are useful for practicing evidence order and competing hypotheses,
not for selecting switch thresholds, buffer reservations, QoS maps, NIC
settings, or production architecture.

## Input model

The baseline scenario is returned by `baseline_scenario()` and contains:

- `schema`, deterministic `seed`, `cluster`, workload kind, ranks or requests,
  phase payloads, rail offered load, and a training deadline or inference
  target-p99 objective;
- exactly four hosts, two rails, two leaves, two spines, and a separate
  storage/control service set;
- links with `capacity_bps`, MTU, availability, and rail membership;
- qualitative congestion policy with a queue guardrail and optional pause;
- storage/control capacity and availability; and
- one `fault` from the fixed allowlist plus executed, read-only assertions.

The allowed faults are `none`, `rail_imbalance`, `link_unavailable`,
`mtu_reduced`, `queue_pressure`, `storage_saturation`, `placement_skew`,
`control_blocked`, `telemetry_clock_offset`, `pause_propagation`, and
`prefill_saturation` (inference only). A
scenario with multiple faults, an unknown rail, a missing host attachment,
negative capacity, invalid MTU, or unsupported workload is rejected.

The fixture treats `rail-a` and `rail-b` as curriculum abstractions. A vendor
or deployment may use different physical meanings for a rail, NIC, path,
collective, queue, or congestion signal; verify the release, hardware
generation, topology, and runtime before making a product claim.

## Outputs and lifecycle

`runner.py` returns JSON containing an input digest, normalized and effective
state, selected path/link IDs, per-link and per-rail offered load, qualitative
queue/mark/pause state, training rank estimates or inference request/batch/
stage/p50/p99 fields, independent health/objective/deadline fields, evidence
confidence and attribution state, executed assertion results, rollback proof,
and separate `derived_observation`, `fixture_assumption`, and
`engineering_interpretation` sections.

Every run models these phases in order:

1. `setup`
2. `baseline-readback`
3. `fault`
4. `assertion`
5. `repair-readback`
6. `rollback`
7. `cleanup`

Default mode writes and reads phase files in a temporary workspace, then
removes it and reports `exists_after_cleanup: false`. A retained run requires
an explicit `--artifacts-dir` below this directory's `observed/` root. The
runner refuses traversal and paths outside that root. Retained bundles contain
the seven phase JSON files and a **write-once, hash-manifested bundle** with
SHA-256 hashes, schema, runner version, correlation ID, phase order, and
cleanup proof. This is not an immutable artifact: verification detects changed
phase content only while the verifier and manifest are trustworthy.

## Commands

From the repository root:

```bash
python3 book/topics/fixtures/ai-data-center/runner.py --scenario baseline
python3 book/topics/fixtures/ai-data-center/runner.py --scenario baseline --fault rail_imbalance
python3 book/topics/fixtures/ai-data-center/runner.py --scenario inference --fault prefill_saturation
python3 book/topics/fixtures/ai-data-center/runner.py --scenario baseline --fault storage_saturation --artifacts-dir book/topics/fixtures/ai-data-center/observed/storage-run
python3 book/topics/fixtures/ai-data-center/runner.py --verify-bundle book/topics/fixtures/ai-data-center/observed/storage-run/run-...
python3 book/topics/fixtures/ai-data-center/test_runner.py
```

The retained example is synthetic and local. Remove only a retained bundle
that you created under `observed/` after reviewing its manifest; the runner
does not perform broad cleanup. A normal learner run should use temporary mode
unless an artifact is needed for the exercise submission.

## Reading an output

Start with the selected path/link map, then compare per-link and per-rail load
and path availability. Inspect queue state and effective MTU, then
storage/control/model-cache fields. Read `health_state`, `objective_state`,
and `deadline_met` independently from evidence `confidence` and
`attribution_state`. A `DEGRADED` or `BLOCKED` health state is a derived
symptom, not a root-cause declaration. Compare `storage_saturation` with
`rail_imbalance`, and compare an inference model-cache or prefill fault with a
fabric fault: similar symptoms do not imply the same owner.

**Vendor terminology:** ECN, PFC, RoCE, RDMA, InfiniBand, NCCL, and similar
terms in the companion topic are release- and deployment-qualified. This
fixture does not implement those technologies; it only offers qualitative
fields for interview reasoning.
