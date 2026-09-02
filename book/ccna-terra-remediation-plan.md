# Terra remediation plan: CCNA-to-Staff expansion

## A. Status

This is the implementation contract for the three remaining Terra blockers.
The quality gate remains **NOT APPROVED** until a fresh independent Terra audit
verifies the saved artifacts. Local fixture output is **observed** only for the
fictional emulator; AWS, GCP, Terraform, NSO, NDFC, F5, and A10 API examples
are **illustrative**.

## B. Remediation contract

1. **Implemented locally, pending Terra:** `fixtures/runner.py` runs 15 named
   mechanism-shaped scenarios from separate control and data-plane state,
   retains setup, baseline, bounded fault, assertion, repair, rollback,
   cleanup, and content-hash manifest files in a unique run bundle.
2. **Implemented locally, pending Terra:** each module has a completed
   submission record whose four criteria resolve to retained JSON artifacts,
   pointers, observed values, thresholds, arithmetic, and SDE2/Staff follow-ups.
3. **Implemented locally, pending Terra:** `ownership-records.json` contains
   24 field-level records with one writer, named approver/evidence/rollback
   owners, collision rules, correlated request/read-back fields, and positive
   plus request-success/data-plane-failure negative controls.

## C. Acceptance commands

```bash
python3 book/ccna-networking/fixtures/runner.py --all
python3 book/ccna-networking/fixtures/runner.py --all \
  --artifacts-dir book/ccna-networking/fixtures/observed
./scripts/validate.sh
python3 examples/request_path.py
python3 scripts/check_internal_links.py
git diff --check
```

The runner must end with `modules=15`, `temporary_workspace_removed=True`, and
`no_leak=True`. No credentials, sockets, provider SDKs, or production targets
are permitted. The repository validator creates a fresh temporary capture and
checks the actual bundles, not only the output token.

## D. Terra re-audit checklist

- [x] Confirm every module calls the shared runner scenario and names its JSON artifacts.
- [x] Confirm every module’s completed score cites observed fixture output, not expected output alone.
- [x] Confirm every ownership row has exactly one writer and all required owners.
- [x] Confirm request, authoritative read-back, and independent forwarding/service assertions are paired.
- [ ] Confirm the TODO retains **NOT APPROVED** until this checklist is independently signed off.
