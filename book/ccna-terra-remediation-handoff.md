# Terra Remediation Handoff

**Updated:** 2026-09-01  
**Implementation status:** Semantic remediation saved locally and validated  
**Terra quality gate:** **NOT APPROVED** pending a fresh independent audit

This document is the checkpoint for another agent or review pass. The local
validator passing is not Terra sign-off.

## A. Four semantic blockers addressed

### A.1 Control-only fault injection

`fixtures/runner.py` now mutates only `fault_control` configuration. There is
no paired plane-fault state in a scenario. `fixtures/evaluator.py` derives
module-specific observations from effective control and a separate traffic
fixture. Each assertion records a metadata-only control change that remains
healthy and an evaluator-only mechanism fault that fails the derived path.

### A.2 Derived ownership probes

`evaluate_ownership()` now consumes the retained effective controller state and
a separate `traffic_path`. It rejects caller-supplied health/probe status and
derives the observation through the module evaluator. The negative ownership
records retain an accepted request and active read-back while the separate
mechanism input produces a failed data-plane result.

### A.3 Reconciliation-model read-backs

Every transaction retains:

1. desired-state request;
2. controller reconciliation result;
3. computed changed fields, status, effective-state hash, and task ID;
4. authoritative effective read-back;
5. device/service observation derived from the effective state.

The read-back is no longer an `effective_fields` copy of the request.

### A.4 Module-specific evidence scoring

All 15 completed submissions now point to domain observations such as
`path_mtu`, `hop_admission`, `rib_result`, `ordered_decision`,
`forwarding_next_hop`, or `metric_ms`. Each pointer has a module-specific
threshold and an explicit threshold decision. Generic health-only pointers are
rejected by `scripts/validate.sh`.

## B. Retained evidence

The authoritative tracked run is:

```text
run=20260901T172659.876804Z-b746b7bb
schema=ccna-fixture-bundle/v3
modules=15
phase_files_per_module=8
ownership_records=24
submission_records=15
```

The bundle is under
`book/ccna-networking/fixtures/observed/runs/<run>/modules/<id>/` and includes
setup, baseline, control fault, assertion, repair, rollback, cleanup, and
manifest files. Older v2 generated bundles were removed so stale evidence
cannot be mistaken for the current capture.

## C. Verification completed

```text
./scripts/validate.sh                                      PASS
python3 book/ccna-networking/fixtures/runner.py --all       PASS
python3 examples/request_path.py                            PASS
python3 scripts/check_internal_links.py                     PASS
git diff --check                                            PASS
```

The validator executes a fresh temporary capture, checks v3 schemas and hashes,
checks reconciliation fields and task IDs, rejects old coupled-fault and
caller-probe patterns, resolves all 60 module-specific criterion pointers,
checks 24 ownership negative controls, and verifies cleanup.

## D. Remaining Terra work

1. Run a fresh independent Terra audit against the current working tree and
   retained run.
2. Confirm that each evaluator branch is mechanism-faithful enough for the
   learning objective rather than merely structurally valid.
3. Confirm that the 24 ownership records are sufficiently exclusive and that
   the separate traffic paths are credible negative controls.
4. Confirm every module-specific threshold and the reconciliation model in the
   rendered documentation.
5. Keep this status **NOT APPROVED** until Terra publishes a dated approval.

## E. Handoff rule near usage limits

If another implementation pass approaches its usage limit, update this file
first with the exact run ID, changed files, last successful commands, current
Terra status, and remaining gates. Do not claim Terra approval because local
checks pass.
