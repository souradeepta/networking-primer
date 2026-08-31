# Project memory

## Current state

- Local repository implementation, including hands-on labs, link validation,
  nineteen case studies, and the edition-5 platform expansion, is complete
  locally but not yet committed.
- The content target is SDE1/SDE2 networking, focused on F5 LTM and GTM
  (BIG-IP DNS).
- Public GitHub remote: https://github.com/souradeepta/networking-primer
- The book contains 17 chapters and 16 focused topic references. New coverage
  includes cloud networking/Kubernetes ingress, BGP/anycast/multi-region,
  WAF/API security/zero trust, observability/SLOs, network testing/chaos, and
  capacity/performance engineering. `docs/10-platform-networking.md` bridges
  those topics into the quick-start path.
- Next handoff: run Terra review of the edition-5 expansion, fix any findings,
  then commit and push the public branch.

## Verification

- Run `./scripts/validate.sh`.
- Run `python3 examples/request_path.py`.
- Run `python3 -m py_compile examples/*.py demos/*.py demos/docker/*.py`.
