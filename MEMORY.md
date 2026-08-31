# Project memory

## Current state

- Local repository implementation, including hands-on labs, link validation,
  nineteen case studies, and the edition-5 platform expansion, is complete
  locally but not yet committed.
- The content target is SDE1/SDE2 networking, focused on F5 LTM and GTM
  (BIG-IP DNS).
- Public GitHub remote: https://github.com/souradeepta/networking-primer
- The book contains 17 chapters and 27 focused topic references. New coverage
  includes cloud networking/Kubernetes ingress, BGP/anycast/multi-region,
  WAF/API security/zero trust, observability/SLOs, network testing/chaos, and
  capacity/performance engineering. `docs/10-platform-networking.md` bridges
  those topics into the quick-start path.
- Current work: numbered interview answers have been expanded with mechanisms,
  trade-offs, diagnostics, examples, and caveats across the book, topics,
  case studies, and quick-start interview bank. The edition-6 validator
  enforces minimum answer word counts and heading integrity.
- Next handoff: run the final checks, commit, and push the public branch.

- New focused topics cover HTTP/2/HTTP/3/QUIC, VXLAN overlays, firewall policy,
  service discovery/configuration, and NTP/time synchronization. Edition 7
  requires these topics to include diagrams, tables, exercises, six detailed
  Q&A items, and at least 1,200 words each.
- Granular platform references 22–27 split HTTP transports and add NAT/
  conntrack, CDN edge caching, gRPC/WebSockets/RPC, and network automation.
  Edition 8 records their focused-reference contract and 600-word validator
  floor; deeper expansion remains a future content pass.
- F5 expansion plan is documented in `docs/f5-expansion-plan.md`. Topics 28–33
  now cover traffic processing/TMM, SDK workbench, LTM capacity, BIG-IP DNS
  debugging, read-only troubleshooting, and the API/declarative toolchain.

## Verification

- Run `./scripts/validate.sh`.
- Run `python3 examples/request_path.py`.
- Run `python3 -m py_compile examples/*.py demos/*.py demos/docker/*.py`.
