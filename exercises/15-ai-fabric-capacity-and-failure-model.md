# Exercise 15: AI-fabric capacity and failure model

This exercise turns [topic 40](../book/topics/40-ai-data-center-networking.md)
into a safe theory-to-practice artifact. The fixture is an explanatory local
model. It does not contact a GPU, NIC, switch, cloud account, scheduler,
storage service, or production endpoint.

## Scenario

The fictional `atlas-lab` cluster has four dual-rail hosts, two leaves, two
spines, and separate scheduler, storage, and telemetry services. Four ranks run
a training step with an all-reduce phase and a checkpoint phase. A step that
normally completes is reported as slower after a topology change. Your task is
to determine whether the leading explanation is rail skew, path loss, MTU,
queueing, storage, placement, control, or ambiguous telemetry.

## Constraints and provided fixture

Use only the standard-library fixture:

```bash
python3 ../book/topics/fixtures/ai-data-center/runner.py --scenario baseline
python3 ../book/topics/fixtures/ai-data-center/runner.py --scenario baseline --fault rail_imbalance
python3 ../book/topics/fixtures/ai-data-center/runner.py --scenario baseline --fault storage_saturation
python3 ../book/topics/fixtures/ai-data-center/runner.py --scenario inference
python3 ../book/topics/fixtures/ai-data-center/runner.py --scenario inference --fault prefill_saturation
python3 ../book/topics/fixtures/ai-data-center/test_runner.py
```

The fixed allowlist is local data only. Do not add a production command, tune
an ECN or PFC threshold, enable a pause policy, capture tenant traffic, or
claim that a fixture result is a device measurement. Retained artifacts may be
written only below `book/topics/fixtures/ai-data-center/observed/`.

**Fact:** the runner validates and derives JSON from its input. **Observed lab
result:** record the fixture schema, runner version, scenario, and artifact
path. **Engineering inference:** use the result to choose the next falsifier,
not to declare a physical root cause.

## Deliverables

Submit one review record containing:

1. A topology and rail map naming ranks, hosts, NIC rails, leaves, spines,
   storage, scheduler, telemetry, and failure domains.
2. A workload path for the all-reduce and checkpoint phases, with training
   objective, units, deadline, concurrency, and placement assumptions.
3. A capacity worksheet using installed bandwidth, utilization guardrail,
   concurrent jobs, per-job peak, overlap factor, failure reserve, and
   headroom. Show sensitivity for at least two assumptions.
4. A hypothesis tree for `RAIL_SKEW`, `PATH_UNAVAILABLE`,
   `MTU_INCOMPATIBLE`, `QUEUE_PRESSURE`, `STORAGE_BOUND`, `PLACEMENT_SKEW`,
   `CONTROL_BLOCKED`, and `OBSERVABILITY_AMBIGUOUS`.
5. An evidence order beginning with rank/runtime timestamps and ending with a
   bounded fixture repair. State which owner supplies each evidence item.
6. Baseline, one fault, repair, and rollback fixture outputs. Include the
   negative control and explain why metadata-only input cannot establish a
   causal change.
7. A confidence statement that separates derived observation, fixture
   assumption, engineering inference, and unknown physical behavior.

## Rubric

| Criterion | SDE1 | SDE2 | Staff |
| --- | --- | --- | --- |
| Mechanism | Names components and traces one collective path | Explains rail/path selection, queueing, MTU, and storage alternatives | Defines architecture boundaries and assumptions that survive team changes |
| Evidence | Requests rank, host, path, and storage evidence | Provides competing hypotheses and falsifiers | Assigns retention, privacy, ownership, and decision gates |
| Quantification | Uses bytes, bits, seconds, and stated units | Computes capacity, failure-safe bandwidth, and sensitivity | Compares reserve, lost accelerator time, power/cooling, optics, storage, and operator cost variables |
| Safety | Avoids production actions | Uses the bounded local fixture and reversible repair | Defines migration scope, adoption plan, rollback authority, and irreversible stop |

## Answer key

The baseline should show two balanced modeled rails, available paths, clear
qualitative queues, high evidence confidence, and a completed workload. The
`rail_imbalance` scenario should change the derived rail load and selected
link utilization through state derivation; the `storage_saturation` scenario
may show a similar degraded health state but a different storage signal. The
result also reports objective/deadline state separately from evidence
confidence. That distinction is the important answer: a shared symptom does
not collapse ownership or prove a fabric fault.

For the capacity worksheet, use the topic's synthetic example or state your
own values. With `400 Gb/s` installed, guardrail `0.70`, two jobs at `80
Gb/s`, overlap `0.80`, and a `100 Gb/s` failure domain:

```text
usable = 400 * 0.70 = 280 Gb/s
required = 2 * 80 * 0.80 = 128 Gb/s
failure_safe = 280 - 100 = 180 Gb/s
headroom = 180 / 128 = 1.40625
```

This is a planning bound, not a benchmark. A good answer states that
effective bandwidth changes with placement, ECMP, queueing, software, host
limits, payload framing, and synchronized phases. It does not recommend a
universal oversubscription ratio or a PFC setting.

The safe evidence sequence is: rank map and monotonic runtime timestamps;
host/NIC counters; path and control state; authorized queue/mark/pause
telemetry; storage and scheduler evidence; metadata-only negative control; and
one bounded local fault removal. The repair is restoring the fictional input
and comparing read-back. A retry is not a rollback. Stop if tenant isolation,
data integrity, authority, or the declared objective is uncertain.

## SDE2 extension

Use the executable `--scenario inference` branch. It defines requests,
batching, arrival rate, gateway/prefill/decode/model-cache stages, and a p99
objective. Compare `--fault prefill_saturation` and a fabric fault such as
`link_unavailable`: both can affect tail behavior, but the blocker and owner
evidence differ. A model-cache-unavailable input is a second non-network
competing fault. Explain which evidence can be shared and which labels must
remain workload-specific; inference output is a deterministic teaching
calculation, not an LLM latency predictor.

## Staff extension

Write a design review with two viable options: an isolated training slice and
a shared fabric with admission/headroom controls. For each, state topology and
failure-domain assumptions, scheduler and network ownership, power/cooling and
optics variables, cross-domain transfer and storage variables, operator
complexity, migration stages, adoption/training needs, communication plan,
rollback versus forward-repair criteria, and an irreversible stop. Include a
trigger to revisit the decision when workload mix, hardware generation, or
software release changes.

## Interview prompts

1. **[SDE1] What is the first evidence you request?**

   **Answer:** Request the job identifier, rank map, workload phase, monotonic runtime timestamps, and objective before interpreting a fabric counter. This shows whether the symptom is synchronized training delay, inference tail latency, storage delay, or admission failure.

2. **[SDE2] Why run both rail and storage faults?**

   **Answer:** They can create a similar completion symptom while changing different evidence and owners. Comparing them prevents a single-counter diagnosis and demonstrates that the learner can use a negative control and a falsifier rather than choose the loudest metric.

3. **[Staff] What makes the answer safe?**

   **Answer:** It is scoped to fictional local data, names release and topology uncertainty, uses reversible inputs, preserves evidence, assigns owners, and stops when authority, isolation, integrity, or the workload objective is not safe. It never turns a model into a production tuning recipe.
