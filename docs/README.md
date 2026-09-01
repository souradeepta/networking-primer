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
| Study CCNA-to-Staff networking | [CCNA networking expansion](../book/ccna-networking/00-README.md) | Switching, routing, wireless, security, cloud, automation, troubleshooting, and design |
| Prepare for cloud networking interviews | [Cloud networking interview track](../cloud-networking-interview/00-README.md) | AWS/GCP comparisons, hybrid networking, debugging, capacity, DR, migration, and Staff mock loops |
| Compare deployment models | [Cloud deployment models](../cloud-deployment-models/00-README.md) | Private, public, hybrid, and on-premises networking, connectivity, challenges, labs, case studies, and Q&A |
| Prepare for Terraform/IaC interviews | [Terraform interview track](../terraform-interview/00-README.md) | Terraform execution, state, plans, imports, AWS, GCP, F5, CI/CD, rollback, and Staff design loops |
| Practice network automation platforms | [Terraform platform modules](../terraform-interview/16-a10-load-balancers-and-terraform.md) | A10 ADCs, Cisco automation, spine-leaf fabrics, NDFC, and Cisco NSO service models |
| Practice integrated platform labs | [Integrated network platform labs](../platform-integration-labs/00-README.md) | End-to-end labs combining ADCs, routers, switches, nodes, clouds, NSO, and Terraform |
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

## E. Repository map

```text
docs/       quick concepts, troubleshooting, interviews, labs, and plans
book/       long-form chapters, focused topics, and case studies
cloud-*/    ordered AWS/GCP cloud networking interview track
terraform-*/ ordered Terraform and network automation track
platform-*/ integrated multi-vendor labs and system design
demos/      runnable local or fixture-based experiments
exercises/  implementation assignments and edge cases
examples/   small dependency-free reference programs
scripts/    repository validation and link checks
```

The numeric prefixes on the original quick-start files are retained for
backward-compatible links. This index supplies the logical grouping; do not
infer that a higher filename number is always more advanced.

## F. Discoverability map

| If you want to... | Start here | Next |
| --- | --- | --- |
| Learn the request path quickly | [Foundations](01-foundations.md) | [Request path](02-request-path.md) -> [Troubleshooting](05-troubleshooting.md) |
| Study cloud networking | [Cloud track](../cloud-networking-interview/00-README.md) | AWS/GCP modules -> synthesis and mocks |
| Study Terraform and IaC | [Terraform track](../terraform-interview/00-README.md) | state -> providers -> cloud -> platform automation |
| Practice complete platform designs | [Integrated labs](../platform-integration-labs/00-README.md) | topology -> exercises -> system-design discussions |
| Debug as an infrastructure engineer | [Toolkit](infra-engineer-toolkit.md) | Unix sessions -> tools -> cheatsheets -> runbooks |
| Prepare for SDE2 | [Study plan](interview-study-plan.md) | question banks -> dialogue -> simulations -> design |
| Prepare for Staff | [Staff rubric](staff-interview-rubric.md) | design review -> behavioral -> platform labs |
| Find evidence and terminology | [References](references.md) | [Glossary](glossary.md) -> book ledger |

The [CCNA-to-Staff expansion](../book/ccna-networking/00-README.md) is ordered
through [01](../book/ccna-networking/01-network-models-and-physical.md),
[02](../book/ccna-networking/02-ethernet-switching-and-vlans.md),
[03](../book/ccna-networking/03-stp-lacp-and-layer2-resilience.md),
[04](../book/ccna-networking/04-ipv4-subnetting-nat-and-ipv6.md),
[05](../book/ccna-networking/05-routing-static-ospf-and-vrf.md),
[06](../book/ccna-networking/06-bgp-policy-and-hybrid-wan.md),
[07](../book/ccna-networking/07-network-services-and-operations.md),
[08](../book/ccna-networking/08-acls-aaa-and-network-security.md),
[09](../book/ccna-networking/09-wireless-and-qos.md),
[10](../book/ccna-networking/10-multicast-and-service-delivery.md),
[11](../book/ccna-networking/11-data-center-fabrics.md),
[12](../book/ccna-networking/12-cloud-networking-aws-gcp.md),
[13](../book/ccna-networking/13-private-public-hybrid-and-onprem.md),
[14](../book/ccna-networking/14-automation-sdn-and-iac.md), and
[15](../book/ccna-networking/15-observability-troubleshooting-and-design.md).

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
