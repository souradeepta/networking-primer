# AI data-center networking handoff

**Updated:** 2026-09-07
**Branch:** `main`
**Latest pushed commit:** `8e1965e Remediate AI data center fixture semantics`

## Outcome

Terra’s remediation plan was implemented by Luna and pushed to the public
remote. The AI-era data-center networking material now combines theory,
practical fixture work, failure analysis, and interview-oriented exercises.

The implementation covers:

- schema-v2 topology and graph-consistent selected paths;
- state-derived fault outcomes rather than scenario-label conclusions;
- executable assertions with pass/fail reporting;
- scoped artifact lifecycle, readback, cleanup, and bundle verification;
- separate workload health, objective, deadline, evidence confidence, and
  attribution states;
- a bounded inference path with request, batching, queue, stage, and p99
  signals;
- transition-authority and capacity-sensitivity guidance; and
- corrected lifecycle, exercise-index, evidence, and immutable-state wording.

## Primary artifacts

- [Terra remediation plan](ai-data-center-networking-remediation-plan.md)
- [AI data-center networking topic](../book/topics/40-ai-data-center-networking.md)
- [Offline fixture README](../book/topics/fixtures/ai-data-center/README.md)
- [Fixture runner](../book/topics/fixtures/ai-data-center/runner.py)
- [Fixture tests](../book/topics/fixtures/ai-data-center/test_runner.py)
- [Capacity and failure exercise](../exercises/15-ai-fabric-capacity-and-failure-model.md)
- [Fact/inference ledger](../book/FACT-INFERENCE-LEDGER.md)

## Verification evidence

The following checks passed before push:

```text
./scripts/validate.sh                                      PASS
python3 -m unittest discover -s book/topics/fixtures/ai-data-center \
  -p 'test_*.py'                                          PASS (21 tests)
python3 examples/request_path.py                           PASS
python3 -m py_compile book/topics/fixtures/ai-data-center/runner.py \
  book/topics/fixtures/ai-data-center/test_runner.py      PASS
git diff --check                                           PASS
```

The fixture CLI also generated baseline and inference bundles beneath its
scoped `observed/` directory, and retained-bundle verification passed hashes,
phase order, schema, and correlation-ID checks.

## Handoff boundaries

This is vendor-aware educational material and an offline qualitative fixture,
not a production runbook or a physical performance benchmark. Validate vendor
terminology, release behavior, NIC/fabric capabilities, and operational
commands against the target environment before use. Preserve the fact,
vendor-terminology, and engineering-inference labels when extending the
material.

## Suggested next work

1. Keep fixture scenarios small and evidence-oriented; add a test whenever a
   new fault or assertion operator is introduced.
2. Add provider-specific references only when the release and product boundary
   are explicit in `docs/references.md`.
3. Re-run the repository validator and fixture tests for every curriculum or
   runner change.
