# Book material review handoff

**Updated:** 2026-09-07

The Terra book-material remediation plan is complete. The implementation status
is recorded in [the review plan](book-material-review-plan.md), and the
repository-wide handoff is in [HANDOFF.md](../HANDOFF.md).

## Completed gates

- Chapters 2, 15, 16, and 17 have corrected routing, NetworkPolicy, evidence,
  and WAF/TLS explanations.
- Focused topics 01–39 are indexed and represented in the evidence ledger.
- All numbered answers have explicit direct-answer boundaries and duplicate or
  short-answer reporting.
- Staff practice is distributed across focused topics and six worked Staff
  answer keys cover the major domains.
- Local anchors, Mermaid theme settings, role contracts, and advanced-topic
  evidence labels are validated.

## Handoff commands

```bash
./scripts/validate.sh
python3 examples/request_path.py
git diff --check
```

Treat passing local validation as repository evidence, not vendor or Terra
approval. Pin target provider, controller, appliance, browser, and resolver
versions before applying a recommendation.
