# Repository handoff

**Updated:** 2026-09-07  
**Branch:** `main`  
**Latest pushed commit:** `209aa73 Update learning path and handoff documentation`

## Current state

The networking primer remediation is complete and pushed to the public remote.
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
git diff --check                              PASS
```

The validator checks 39 focused topics, 663 answer entries, 147 Mermaid
diagrams, role/evidence contracts, index parity, local anchors, and
duplicate-answer warnings.

## Ownership and next steps

Content owners should verify vendor behavior against deployed releases before
using examples operationally. Curriculum maintainers should preserve the
Fact/Vendor terminology/Engineering inference boundary and update the ledger
when adding platform claims. Future additions should be justified by a
distinct learning objective and evidence contract rather than file count.
