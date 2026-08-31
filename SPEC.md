# Networking Primer Specification

## Audience and outcome

This repository teaches the networking knowledge an SDE1 needs to debug an
application request, the additional SDE2 knowledge needed to reason about
availability and traffic policy, and Staff-level skills for platform strategy,
ownership, migration, and cross-team technical leadership. It emphasizes F5
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

Add at least nineteen case studies, each at least 1,500 prose words, using fictional
addresses and service names. Each case study must contain context and goals,
architecture/topology, a timestamped incident or change timeline, evidence
collected, competing hypotheses, decision points and trade-offs, remediation,
verification, rollback or recovery, postmortem lessons, a detailed ASCII-only
Mermaid diagram, and at least 10 explained Q&A. Required subjects are (1) an
LTM VIP and certificate migration, (2) GTM/BIG-IP DNS multi-site failover, (3)
DDI/IPAM-DHCP-DNS drift causing an outage, and (4) certificate automation and
F5 change safety. Case studies must distinguish observed facts from inferred
causes and cite primary protocol/vendor references.

Diagram requirement: each infrastructure case study must include at least two
diagrams (topology plus sequence, timeline, or state); core F5 LTM, GTM,
transport-security, DDI, proxy, and automation articles should include both a
topology/architecture view and a packet, control-flow, or state view where the
relationship is material.

The 15 additional cases must cover distinct scenarios: firewall/TCP timeout,
MTU black hole, IPv6 migration, DNSSEC validation failure, DHCP exhaustion,
duplicate IP detection, LTM persistence hotspot, false-positive LTM monitor,
LTM HA failover, GTM topology misrouting, GTM TTL migration, expired TLS
intermediate, mTLS trust rotation, F5 SDK idempotency drift, and a failed LB
upgrade with rollback.

## Curriculum expansion (edition 5)

The book now extends beyond the core 14-chapter foundation into production
platform networking. Add at least three new chapters covering cloud networking
and Kubernetes ingress, BGP/anycast/multi-region routing, and WAF/API security
and zero-trust boundaries. New chapters follow the edition-2 chapter contract
and must be at least 1,500 words with a worked operational example, a table,
an ASCII-only Mermaid diagram, and eight explained Q&A items.

Add at least six new focused references covering observability and SLOs,
BGP/anycast policy, Kubernetes ingress/service mesh, WAF/API security and rate
limits, network testing/chaos, and capacity/performance engineering. These
files must be at least 1,200 words and include a table, diagram, worked
example, checklist, and six explained Q&A items.

All existing chapters and focused references should be expanded when a topic
is already present: add concrete packet or control-plane reasoning, F5 LTM or
GTM mappings, DDI implications, automation examples, failure evidence, and
interview-quality Q&A rather than repeating definitions.

## Interview-answer depth (edition 6)

Every numbered interview answer in the book, focused topics, case studies, and
the quick-start interview bank must be explanatory rather than flash-card
length. Each answer must contain at least 35 words after the bold question
(30 words for a case-study answer), and should explain mechanism, trade-offs,
an observable diagnostic or example, and a relevant caveat. The validator
checks this minimum so future edits cannot silently regress to one-line
answers.

## Platform networking additions (edition 7)

Add at least five additional focused references so the curriculum continues
from classic F5/DDI operations into modern service platforms. Cover HTTP/2 and
HTTP/3/QUIC, network virtualization and VXLAN overlays,
firewalls/security groups/NACLs, service discovery and configuration
distribution, and NTP/time synchronization. Each reference must include
objectives, a mental model, a worked example, an ASCII-only Mermaid diagram, a
Markdown table, failure modes, an operational checklist, an implementation
exercise, and at least six interview questions with answers of at least 35
words. Connect each topic to F5 LTM/GTM, DDI, automation, and layered
troubleshooting where relevant, and distinguish measured evidence from
inference.

## Granular platform references (edition 8)

Split bundled platform subjects into individually navigable references when
their protocol, state model, or failure evidence differs materially. The next
set covers HTTP/2, HTTP/3/QUIC, NAT/conntrack/SNAT, CDN/edge caching,
gRPC/WebSockets/RPC, and network automation/testing. Each file must include a
diagram, table, worked example, failure section, checklist, implementation
exercise, and six interview questions. These are focused references rather
than replacement book chapters; the validator enforces a 600-word minimum and
24-word minimum per answer while preserving the deeper chapter contracts.

## F5 interview bank (edition 9)

Maintain a dedicated `docs/f5-interview-bank.md` with at least 30 role-specific
questions, detailed answers, follow-up prompts, and eight debugging exercises.
Coverage must include LTM, GTM/BIG-IP DNS, TLS/mTLS, HA/upgrades, SDK/iControl
REST, AS3/DO/FAST/TS, observability, and failure diagnosis. Answers should
state mechanism, evidence, trade-offs, and caveats; exercises must provide
symptoms, clues, expected reasoning, and a safe resolution boundary. Current
F5 terminology and toolchain claims must link to official documentation.

Maintain a parallel `docs/networking-interview-bank.md` of comparable depth
with at least 60 protocol/platform questions and 16 debugging exercises. Cover
Ethernet/IP/IPv6, TCP/UDP/QUIC, DNS/DHCP/IPAM, HTTP/proxies, TLS/PKI/mTLS,
cloud/Kubernetes, overlays/BGP, observability/SLOs, automation, and security.
Answers must explain mechanism, evidence, trade-offs, and uncertainty rather
than provide flash-card definitions.

Maintain `docs/interview-dialogue-exercises.md` with at least twelve
interviewer/interviewee scenarios spanning operational debugging, authorized
penetration testing, and controlled network testing. Each scenario must state
scope and authorization, clarifying questions, evidence and commands, competing
hypotheses, safe containment or test boundaries, follow-up questions, and
verification. Security exercises must remain defensive and non-destructive.

## Focused files and demos (edition 4)

## Interview practice system (edition 10)

In addition to question banks, maintain a calibrated practice layer: a 0–4
answer rubric, 20 progressive interviewer simulations, 15 timed whiteboard
drills, 10 network system-design exercises, and a measurable 4/6/2-week study
plan. Simulations must include follow-ups, plausible wrong paths, safe testing
boundaries, and scoring. Whiteboard and design drills must require assumptions,
failure domains, evidence, trade-offs, and rollback. Security exercises must
remain authorized and non-destructive.

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

The LTM implementation track must include a dedicated lab chapter covering
self IPs, VLANs, VIPs/virtual servers, pools, members, nodes, monitors,
profiles, SNAT, persistence, iRules/policies, client/server SSL profiles, and
the exact source/destination IP:port tuple on both sides of the proxy. It must
walk through basic balancing, member failure, SNAT, HTTPS offload,
persistence, and symptom-driven troubleshooting.

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
