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
