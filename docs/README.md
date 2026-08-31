# Documentation index

This is the **quick-start and interview-practice edition** of Networking
Primer. Use this page when the repository feels too large. Read one track in
order, then jump to the detailed reference or practice artifact linked from
that track.

## A. Choose a path

| Goal | Start | Then continue with |
| --- | --- | --- |
| Understand one request | [Foundations](01-foundations.md) | [Request path](02-request-path.md) -> [Troubleshooting](05-troubleshooting.md) |
| Prepare for SDE2 | [Interview study plan](interview-study-plan.md) | [Interview banks](networking-interview-bank.md), design exercises, and labs |
| Prepare for Staff | [Curriculum improvement spec](interview-curriculum-improvement-spec.md) | [Staff rubric](staff-interview-rubric.md), design pack, behavioral exercises |
| Become stronger at Unix/network diagnosis | [Toolkit index](infra-engineer-toolkit.md) | Unix sessions -> tools -> cheatsheets -> runbooks/exercises |
| Learn F5 LTM/GTM | [F5 LTM](03-f5-ltm.md) | [F5 GTM](04-f5-gtm.md), F5 bank, labs, and read-only troubleshooting |
| Review cloud-native networking | [Platform networking](10-platform-networking.md) | DDI, transport security, Kubernetes, overlays, BGP, and capacity |
| Prepare for cloud networking interviews | [Cloud networking interview track](../cloud-networking-interview/README.md) | AWS/GCP comparisons, hybrid networking, debugging, capacity, DR, migration, and Staff mock loops |
| Practice safely | [Hands-on labs](09-hands-on-labs.md) | Demos, implementation exercises, and case studies |

## B. Recommended reading sequence

### B.1 Foundation and request path

1. [01. Networking foundations](01-foundations.md) — layers, addressing,
   TCP/UDP, DNS, TLS, and HTTP.
2. [02. Request path](02-request-path.md) — follow a request across hops and
   identify the first failing boundary.
3. [05. Troubleshooting](05-troubleshooting.md) — use evidence, hypotheses,
   falsifiers, and safe escalation.
4. [08. Transport security](08-transport-security.md) — certificates, SNI,
   mTLS, SSH, and trust boundaries.

### B.2 Traffic delivery and platform networking

1. [03. F5 LTM](03-f5-ltm.md) — VIPs, pools, monitors, profiles, SNAT, and
   persistence.
2. [04. F5 GTM/BIG-IP DNS](04-f5-gtm.md) — Wide IPs, TTL, health, and DNS
   steering semantics.
3. [06. DDI](06-ddi.md) — DNS, DHCP, IPAM, ownership, and drift.
4. [10. Platform networking](10-platform-networking.md) — cloud, Kubernetes,
   overlays, BGP, observability, security, and performance.
5. [07. Automation](07-automation.md) — read-before-write, SDK/REST, SSH, and
   rollback boundaries.

### B.3 Reference and orientation

1. [Architecture diagrams](architecture.md) — request paths, control points,
   and system boundaries.
2. [Glossary](glossary.md) — concise terminology lookup while reading.
3. [F5 expansion plan](f5-expansion-plan.md) — planning material for additional
   vendor-focused depth; it is not a required reading chapter.

### B.4 Infra engineer practice

1. [Unix debugging sessions](unix-debugging-sessions.md).
2. [Networking tools and commands](networking-tools-and-commands.md).
3. [Networking issue cheatsheets](networking-issue-cheatsheets.md).
4. [Runbooks and implementation exercises](infra-engineer-runbooks-and-exercises.md).
5. [Hands-on labs](09-hands-on-labs.md).
6. [Request-path simulator](../examples/request_path.py).

## C. Interview preparation map

### C.1 Question and dialogue practice

- [Networking interview bank](networking-interview-bank.md) — broad protocol,
  cloud, Kubernetes, security, automation, and debugging questions.
- [F5 interview bank](f5-interview-bank.md) — LTM, BIG-IP DNS, TLS, HA,
  SDK/REST, declarative tooling, and failure diagnosis.
- [Interview questions](interview-questions.md) — compact quick-start review.
- [Dialogue exercises](interview-dialogue-exercises.md) — detailed interviewer
  and candidate conversations with SDE2/Staff answer guidance.
- [Interview rubric](interview-rubric.md) — mechanism, evidence, safety,
  trade-off, communication, and verification.

### C.2 Design and timed practice

- [Study plan](interview-study-plan.md) — two-, four-, and six-week sequences
  with role gates.
- [Whiteboard drills](interview-whiteboard-drills.md) — timed packet, DNS,
  TLS, routing, Kubernetes, automation, and security drills with answer keys.
- [System-design exercises](network-system-design-exercises.md) — ten
  end-to-end designs with capacity, failure, and rollback requirements.
- [Simulation pack](interview-simulation-pack.md) — progressive operational
  simulations and conversation transcripts.
- [Staff design review pack](staff-design-review-pack.md) — twelve ambiguous
  platform and migration designs.
- [Staff behavioral exercises](staff-behavioral-exercises.md) — influence,
  conflict, mentoring, incident leadership, and durable outcomes.

## D. Reference and governance map

| Need | Document |
| --- | --- |
| Protocol/vendor evidence | [References](references.md) |
| Book fact/inference map | [Book ledger](../book/FACT-INFERENCE-LEDGER.md) |
| Curriculum gaps and roadmap | [Curriculum improvement spec](interview-curriculum-improvement-spec.md) |
| Terra review findings and remediation | [Book material review plan](book-material-review-plan.md) |
| Formatting rules | [Markdown style guide](markdown-style-guide.md) |
| Safety, privacy, warranty, and generated content | [Repository disclosures](../DISCLOSURES.md) |
| Repository contract | [SPEC](../SPEC.md) and [AGENTS guidance](../AGENTS.md) |

## E. How the directories fit together

```text
docs/       quick concepts, troubleshooting, interviews, labs, and plans
book/       long-form chapters, focused topics, and case studies
demos/      runnable local or fixture-based experiments
exercises/  implementation assignments and edge cases
examples/   small dependency-free reference programs
scripts/    repository validation and link checks
```

The numeric prefixes on the original quick-start files are retained for
backward-compatible links. This index supplies the logical grouping; do not
infer that a higher filename number is always more advanced.

## G. Filename policy

- `01-` through `10-` are **stable quick-start identifiers**, not a complete
  difficulty ranking.
- Semantic filenames without numeric prefixes are supporting references,
  practice packs, governance documents, or plans.
- New documents should use descriptive semantic filenames and be added to the
  appropriate section of this index; do not start a second numeric series.
- Existing files remain at the repository root to preserve bookmarks and local
  links. A future subdirectory is appropriate only for a cohesive collection
  with its own README.

## H. Handoff checklist

Before treating a study artifact or change as complete:

1. Label facts, vendor terminology, observations, and inferences.
2. Use fictional, reserved, local, or explicitly authorized targets.
3. Include assumptions, evidence, a falsifier, trade-offs, and verification.
4. Run `./scripts/validate.sh` and `python3 examples/request_path.py`.
