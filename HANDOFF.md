# Repository handoff

**Updated:** 2026-09-07  
**Branch:** `main`  
**Latest pushed commit:** `8e1965e Remediate AI data center fixture semantics`

## Current state

The networking primer remediation, including the AI data-center networking
review and fixture remediation, is complete and pushed to the public remote.
The repository maintains 17 book chapters, 39 focused topics, 19 case
studies, cloud/Terraform/platform tracks, and distributed SDE2/Staff practice.

The curriculum includes explicit answer boundaries, Staff role calibration,
expected interview artifacts, evidence labels, focused-topic ledger coverage,
local-anchor checking, Mermaid light-theme checking, and broader-track contract
validation. Modern DNS/IPv6 and edge-abuse-defense topics are included.

## Verification

```text
./scripts/validate.sh                         PASS
python3 examples/request_path.py              PASS
python3 -m unittest discover -s book/topics/fixtures/ai-data-center -p 'test_*.py'  PASS (21 tests)
git diff --check                              PASS
```

The validator checks the current focused topics, answer entries, Mermaid
diagrams, role/evidence contracts, index parity, local anchors, duplicate
answers, and AI data-center fixture safety/lifecycle contracts.

For the AI data-center work, see the [focused handoff](docs/ai-data-center-networking-handoff.md)
and [Terra remediation plan](docs/ai-data-center-networking-remediation-plan.md).

## Ownership and next steps

Content owners should verify vendor behavior against deployed releases before
using examples operationally. Curriculum maintainers should preserve the
Fact/Vendor terminology/Engineering inference boundary and update the ledger
when adding platform claims. Future additions should be justified by a
distinct learning objective and evidence contract rather than file count.
