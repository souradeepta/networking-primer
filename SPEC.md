# Networking Primer Specification

## Audience and outcome

This repository teaches the networking knowledge an SDE1 needs to debug an
application request and the additional SDE2 knowledge needed to reason about
availability, traffic policy, and operational failure modes. It emphasizes F5
BIG-IP Local Traffic Manager (LTM) and BIG-IP DNS, historically called Global
Traffic Manager (GTM).

## Required deliverables

- A navigable README with a four-session learning path.
- Networking foundations: layered model, addressing/routing, TCP/UDP, TLS,
  HTTP, DNS, and observability.
- A request-path explanation and LTM object model (virtual server, pool,
  member, node, monitor, profile, SNAT) plus an LTM troubleshooting flow.
- A GTM/BIG-IP DNS explanation (Wide IP, pool, virtual server, server,
  data center, monitor, DNS TTL, and steering methods) plus failure semantics.
- A DDI module covering DNS, DHCP, IPAM ownership and their consistency risks.
- Automation guidance, a read-only F5 Python SDK example, and security material
  for SSH, encryption, certificates, TLS, and mTLS.
- Three safe hands-on labs for DNS/GTM observation, LTM request-path diagnosis,
  and TLS/mTLS certificate diagnosis.
- At least two ASCII-only Mermaid diagrams, an interview question bank,
  glossary, references with a fact/inference ledger, and a runnable standard
  library Python exercise.
- A validator that checks required files and Mermaid ASCII-only content.

## Non-goals

- This is not a production BIG-IP configuration guide. Examples use simplified
  object names and do not include credentials, tenant-specific commands, or
  a claim that a policy is universally appropriate.

## Acceptance checks

`./scripts/validate.sh` passes, internal Markdown links resolve, and
`python3 examples/request_path.py` emits a successful request-path trace.

## Book-depth expansion (edition 2)

The compact primer is being expanded into a book-style reference. The expanded
edition must contain at least 12 chapters, with every chapter including:

- 1,200 or more prose words (excluding tables, code, and diagrams).
- Learning objectives, prerequisites, a mental model, and a “when this breaks”
  section.
- At least one worked example, one operational checklist, and one detailed
  ASCII-only Mermaid diagram.
- At least 8 chapter-specific questions with answers and explanations.

Required chapter coverage: OSI/TCP-IP and packet journeys; IPv4/IPv6 and
subnetting; Ethernet/ARP/ND/VLAN/routing; TCP/UDP/QUIC; HTTP and APIs; DNS;
DHCP/IPAM/DDI; TLS/certificates/mTLS/PKI; reverse proxies and load balancing;
F5 LTM; F5 GTM/BIG-IP DNS; observability/troubleshooting; and automation,
SSH, and safe change management. Chapters may combine adjacent topics only if
the acceptance checks remain satisfied.

The validator must check chapter count, required headings, approximate prose
minimums, Q&A counts, Mermaid presence, and local-link integrity. Central claims
that depend on protocol standards or vendor behavior must be represented in a
fact/inference ledger with primary references; recommendations must be labeled
as engineering inferences.

## Infrastructure case-study expansion (edition 3)

Add at least four case studies, each at least 1,500 prose words, using fictional
addresses and service names. Each case study must contain context and goals,
architecture/topology, a timestamped incident or change timeline, evidence
collected, competing hypotheses, decision points and trade-offs, remediation,
verification, rollback or recovery, postmortem lessons, a detailed ASCII-only
Mermaid diagram, and at least 10 explained Q&A. Required subjects are (1) an
LTM VIP and certificate migration, (2) GTM/BIG-IP DNS multi-site failover, (3)
DDI/IPAM-DHCP-DNS drift causing an outage, and (4) certificate automation and
F5 change safety. Case studies must distinguish observed facts from inferred
causes and cite primary protocol/vendor references.

## Focused files and demos (edition 4)

The book must also expose focused topic files rather than hiding all detail in
combined chapters. Add at least six focused references covering VIPs/virtual
servers, certificates and SNI, LTM monitors/pools, GTM Wide IPs and TTL,
DDI/IPAM ownership, SSH/F5 automation, LB device lifecycle/upgrades, proxy
architecture, and comprehensive F5 SDK usage. Each focused file must include a
worked configuration or diagnostic example and at least 5 Q&A. Add at least
four safe demos under `demos/`: shell DNS observation, shell TLS/certificate
inspection, a Python VIP/LTM decision model, and a Python certificate or F5
state audit. Demos must use reserved/local targets, fail clearly, avoid secrets,
and run without modifying production systems.

The demonstration stack is Python for networking models and audits, Linux/macOS
CLI tools for experiments, Wireshark or tshark for packet inspection, Docker
for reproducible local client/server environments, and Markdown/Mermaid for
the teaching material. Docker and packet-capture exercises must be optional,
local, and clearly separated from production targets.

Include an implementation-exercise track with at least six exercises spanning
DNS answer parsing, VIP/LTM selection, certificate inventory, request tracing,
retry budgets, and F5 SDK plan generation. Exercises must specify edge cases,
tests, and safety boundaries.

Focused topic files and case studies must use Markdown tables when a matrix is
clearer than prose (for example object mappings, evidence matrices, timelines,
or decision trade-offs); each file must contain at least one such table.

Add at least two self-contained, dependency-free browser animations under
`demos/animations/`: one packet/request journey and one DNS/GTM failover
timeline. They must include play/pause controls, explanatory labels, a reduced-
motion fallback, and fictionalized real-world context. Case studies should use
multiple diagrams where sequence, topology, and state transitions materially
clarify the incident.
