# Project memory

## Current state

- Local repository implementation, including hands-on labs and link validation,
  is complete at commit `b9fb612`.
- The content target is SDE1/SDE2 networking, focused on F5 LTM and GTM
  (BIG-IP DNS).
- Public GitHub remote: https://github.com/souradeepta/networking-primer
- Expansion in progress: book chapters 1-14 are complete; infrastructure case
  studies 1-2 and focused topic/demo scaffolding are in progress. The current
  validator will intentionally fail until all four cases and six focused topics
  exist.
- Next handoff: finish case studies 3-4 and focused topics, then run Terra review
  and commit/push the edition-3/4 expansion.

## Verification

- Run `./scripts/validate.sh`.
- Run `python3 examples/request_path.py`.
