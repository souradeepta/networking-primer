# Independent Terra quality-gate audit: CCNA-to-Staff expansion

**Audit date:** 2026-09-01 (MST)
**Decision:** **NOT APPROVED**  
**Audit type:** Fresh execution plus strict semantic review of the saved working tree.

This independent audit reviewed the collection index and all 15 modules,
`fixtures/runner.py`, `fixtures/evaluator.py`, every retained v3 run bundle,
`completed-submissions.json`, `ownership-records.json`,
`ownership-matrix.md`, `scripts/validate.sh`, the TODO, remediation plan,
handoff, and the prior review. It changed only this report; it did not alter
learning material or validators.

## A. Decision summary

The implementation now has strong **structural** evidence: 15 retained module
bundles, 15 artifact-linked submission records, 24 ownership records,
correlation IDs, reconciliation-shaped metadata, hashes, cleanup evidence, and
passing repository checks. The rendered modules also link to their fixture
evidence and completed-submission material.

It is still not possible to approve the semantic quality gate. The key issue is
that the fixture code declares the expected outcomes instead of deriving them
through independently evolving local state:

1. Every module accepts a runner-supplied `mechanism_fault` argument that
   directly overrides an evaluator result.
2. Every retained effective read-back is a wrapper around the desired state;
   there is no controller store, defaulting, rejection, drift, or collision
   transition to observe.
3. Every score is written as `PASS` and `25/25`; threshold text is not executed
   as a predicate against the retained artifacts.
4. Every ownership row supplies a declarative single-writer rule, but none
   exercises enforced ownership or derives an object/field-specific assertion
   from a separately reconciled service/forwarding state.

This is a vendor-aware learning repository, not an operational runbook. The
remaining gate does **not** require credentials, production targets, cloud
accounts, real appliances, sockets, or privileged network namespaces. It does
require a bounded local emulator whose state transitions—not the runner's
expected-result inputs—produce the saved evidence.

## B. Execution record

Executed from the repository root during this audit:

```text
python3 book/ccna-networking/fixtures/runner.py --all
FIXTURE_PASS modules=15 temporary_workspace_removed=True no_leak=True

Independent evaluator audit
modules=15
baseline_healthy=15
direct_mechanism_input_flips=15
mechanism_key_in_traffic=0

Retained-artifact audit
run=20260901T172659.876804Z-b746b7bb
module_transactions=60
readback_equals_desired=60
ownership_records=24
ownership_readback_equals_request=24
enforced_collision_records=0
submission_records=15
criteria=60
static_full_pass_criteria=60

./scripts/validate.sh                    PASS
python3 examples/request_path.py         PASS
python3 scripts/check_internal_links.py  PASS
git diff --check                          PASS
```

The runner's default capture is temporary and is removed after the run. The
retained tracked capture named above was separately inspected, including all
eight files per module bundle: setup, baseline read-back, control fault,
assertion, repair read-back, rollback, cleanup, and manifest.

## C. Quantified gate results

| Quality gate | Result | Strict conclusion |
| --- | --- | --- |
| Collection/index/modules and artifact links | **Pass: 15/15** | All modules are present, ordered, and link to retained evidence and the worked-submission document. |
| Fresh fixture execution and cleanup | **Pass: 15/15** | The runner completed all modules and reported temporary workspace removal and no leak. |
| Retained v3 lifecycle bundles, hashes, correlation IDs | **Pass: 15/15** | The retained run has all lifecycle files and manifests; the repository validator also verifies a fresh temporary capture. |
| Repository validation, Python example, internal links, diff check | **Pass: 4/4** | All required repository checks passed. |
| Control-only bounded configuration fault | **Partial: 15/15 structural** | `fault_control` changes only control/configuration fields. |
| Independently derived data-plane behavior and negative controls | **Fail: 0/15 strict** | A runner-selected `mechanism_fault` parameter directly changes evaluator branches in all 15 scenarios. That is a separate code path, not independently evolving local traffic/service state. |
| Reconciliation-derived read-backs | **Fail: 0/60 module transactions; 0/24 ownership records** | All 60 module `effective_state.module_control` values equal their desired request, and all 24 ownership `effective_state.owned_field` values equal the request. The wrapper is not a separately reconciled state. |
| Module-specific artifact pointers | **Pass: 15/15 structural** | All 15 records point at named module observations such as MTU, VLAN admission, OSPF neighbor state, FIB result, or cloud next hop. |
| Module-specific artifact-backed criterion scoring | **Fail: 0/15 strict** | All 60 criteria contain static `PASS`, `pass: true`, and `25/25`; the code stores threshold prose but does not evaluate a predicate before awarding points. |
| Ownership row schema and paired correlations | **Pass: 24/24 structural** | All rows name a platform/object field, writer, approver, evidence and rollback owners, request/read-back pair, and negative-control shape. |
| Enforced field ownership and read-back behavior | **Fail: 0/24 strict** | There is no state store keyed by object/field, no second-writer attempt, no rejection/exception record, and no effective-value/default/drift transition. |
| Object/field-specific independent assertion | **Fail: 0/24 strict** | Each row calls a module-level evaluator over static traffic and a direct `mechanism_fault`; the asserted behavior is not derived from the owned field's reconciled effective value. |
| Vendor/evidence labels | **Partial** | The files appropriately call requests illustrative and outputs local-emulator evidence, but words such as *authoritative* and *derived negative control* must remain bounded to the emulator until the state model is real. |

## D. Exact residual findings

| Severity | Finding | Verified evidence | Required repair |
| --- | --- | --- | --- |
| **High** | Negative controls are runner-selected outcome overrides, not independent mechanism observations. | `derive_dataplane()` accepts `mechanism_fault`; the audit showed that this single direct parameter flips baseline health in **15/15** modules. The `mechanism_fault` key is not in the baseline traffic fixture, so the evaluator itself supplies the outcome override. | Replace the override argument with a bounded topology/service state model. A negative case must change a separately retained path dependency, then derive its observation from that state; the runner must not pass an expected failure name to the evaluator. |
| **High** | Reconciliation read-backs are request echoes. | `_transaction()` constructs `effective_state.module_control` by copying `desired`; all **60/60** module read-backs matched desired state exactly. Ownership records construct `effective_state.owned_field` from `requested`; all **24/24** matched exactly. | Add a controller store with current, desired, effective, task, and immutable change records. Model at least one defaulted/effective value, rejected write, or drift case per platform family. A retained read-back must be generated from the store, not from the request object. |
| **High** | Ownership is declared but never enforced. | All **24** records carry one writer and a collision-rule string, but the audit found **0** collision-result artifacts and no keyed owner registry. | Enforce one writer per `(platform, object, field)` in the controller store. Attempt a second writer for every row (or a representative row per platform family with coverage evidence), retain the rejection or approved exception record, and bind the linked change record to before/effective/after state. |
| **High** | Ownership probes do not depend on the owned field's effective value. | Every row uses a module-level base control and static traffic; the ownership field is only checked for equality with the request. For example, an AWS route table field is not used to derive a route decision, and an ADC member field is not used to derive member selection. | Define an object/field-to-probe adapter for all **24** rows. The positive assertion must consume the reconciled field; the negative control must preserve request/read-back success but alter a separate path dependency that the adapter reads. Retain adapter input and output. |
| **Medium** | Rubric scores are formatted as results, not computed results. | `_submission_records()` writes `threshold_decision: PASS`, `pass: true`, and `points_awarded: 25` for all **60** criteria. Thresholds are descriptive strings rather than evaluated predicates. | Implement explicit per-criterion predicates with retained operands, boolean result, awarded points, and arithmetic. The validator should replay the predicates over the artifacts instead of trusting recorded pass fields. |
| **Medium** | Handoff/TODO claims should not imply the semantic gates are closed. | The TODO marks several semantic-remediation rows complete even though this audit measures **0/15**, **0/60**, and **0/24** on the corresponding strict gates. | After the implementation repair, distinguish structural completion from Terra semantic approval and retain the latest measured counts. |

## E. Disposition of the four requested semantic blockers

| Prior blocker | Strict result | Why |
| --- | --- | --- |
| Control-only injection, derived behavior, and negative controls | **Not resolved** | Control-only `fault_control` exists, but the data-plane negative branch is directly selected by a runner argument in **15/15** scenarios. |
| Reconciliation read-backs not request echoes | **Not resolved** | **60/60** module and **24/24** ownership read-backs are copies of the desired/requested values inside a wrapper. |
| Module-specific artifact-backed criterion scoring | **Not resolved** | Pointers are module-specific, but **60/60** scores are statically awarded rather than predicate-derived. |
| Field-level ownership/request/read-back/independent assertions | **Not resolved** | Schema coverage is **24/24**, but enforced ownership, controller-derived read-back, and field-specific assertions are **0/24**. |

## F. Approval gates

The collection may be marked **APPROVED** only when a later independent audit
verifies all of the following:

1. **15/15 causal fixtures:** no direct result/failure argument enters the
   evaluator; a control change or retained independent path condition produces
   the forwarding/service observation through a bounded local state model.
2. **15/15 derived negative controls:** a successful request and effective
   read-back can coexist with a failure derived from a separately retained
   topology, traffic, service, or device-observation state.
3. **60/60 computed criteria:** every criterion stores its operands, predicate,
   result, points, and reproducible arithmetic; no static pass/score fields are
   trusted.
4. **24/24 controller records:** each owned field has enforced single-writer
   behavior, a retained collision/rejection or approved-exception proof, an
   immutable change record, and a controller-generated effective read-back.
5. **24/24 field-to-probe assertions:** the positive and negative assertions
   consume the reconciled owned field and a separate path condition, respectively.
6. **Accurate status and labels:** TODO, plan, handoff, matrix, and rendered
   modules distinguish illustrative vendor requests, observed local-emulator
   state, and genuinely independently derived evidence.
7. **Clean re-audit:** all required repository checks pass and an independent
   Terra review reports no high-severity semantic or labeling gap.

Until these gates are closed, the independent Terra quality-gate decision is
**NOT APPROVED**.
