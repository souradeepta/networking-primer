# Project memory

## Current state — 2026-09-07

- The public `main` branch is current and clean. The latest pushed commit is
  `209aa73 Update learning path and handoff documentation`.
- The content target is SDE1/SDE2 networking, focused on F5 LTM and GTM
  (BIG-IP DNS).
- Public GitHub remote: https://github.com/souradeepta/networking-primer
- The book contains 17 chapters and 39 focused topic references. New coverage
  includes cloud networking/Kubernetes ingress, BGP/anycast/multi-region,
  WAF/API security/zero trust, observability/SLOs, network testing/chaos, and
  capacity/performance engineering. `docs/10-platform-networking.md` bridges
  those topics into the quick-start path.
- Current work: numbered interview answers have been expanded with mechanisms,
  trade-offs, diagnostics, examples, and caveats across the book, topics,
  case studies, and quick-start interview bank. The edition-6 validator
  enforces minimum answer word counts and heading integrity.
- Phase 0–4 review remediation is complete: correctness fixes, evidence
  governance, explicit answer boundaries, Staff coverage, role contracts,
  local anchors, and Mermaid theme validation are implemented.
- Use `LEARNING_PATH.md` for the current study sequence and `HANDOFF.md` for
  repository ownership and verification context.

- Focused topics now also cover modern DNS/IPv6 migration and edge abuse
  defense. Their index and evidence-ledger rows are validated with the rest of
  the maintained topic inventory.
- Granular platform references 22–27 split HTTP transports and add NAT/
  conntrack, CDN edge caching, gRPC/WebSockets/RPC, and network automation.
  Edition 8 records their focused-reference contract and 600-word validator
  floor; deeper expansion remains a future content pass.
- F5 expansion plan is documented in `docs/f5-expansion-plan.md`. Topics 28–33
  now cover traffic processing/TMM, SDK workbench, LTM capacity, BIG-IP DNS
  debugging, read-only troubleshooting, and the API/declarative toolchain.
- A dedicated `docs/f5-interview-bank.md` now contains 34 core F5 questions,
  follow-up prompts, and eight debugging exercises. New local demos model
  partition-aware planning and REST pagination/task errors without contacting a
  device. Official AS3, DO, TS, and SDK references were added.
- A matching `docs/networking-interview-bank.md` contains 68 core networking
  questions plus detailed follow-ups and 16 debugging exercises across
  protocols, DDI, HTTP, TLS, cloud/Kubernetes, BGP, observability, automation,
  and security. The two banks are intentionally comparable in depth.
- `docs/interview-dialogue-exercises.md` now models 12 interviewer/ interviewee
  scenarios for full logs, unresponsive systems, expired certificates,
  vulnerability findings, suspected breach, DNS/TCP/MTU/F5/SNAT failures,
  authorized penetration testing, and controlled network chaos/load testing.
- Terra's interview-readiness review identified practice-structure gaps. The
  new rubric, 20-scenario simulation pack, 15 whiteboard drills, 10 system
  design exercises, and 4/6/2-week study plan are now in `docs/`. Validators
  enforce their minimum item counts and required files.
- The practice-system files now include role scoring, answer templates, five
  detailed interview transcripts, a worked DNS/GTM whiteboard drill, and a
  multi-region F5 design walkthrough. Validators check substantive markers in
  addition to item counts. Full per-item 350/600-word expansion remains tracked
  in TODO rather than being hidden behind a count-only pass.

## Verification

- Run `./scripts/validate.sh`.
- Run `python3 examples/request_path.py`.
- Run `python3 -m py_compile examples/*.py demos/*.py demos/docker/*.py`.
