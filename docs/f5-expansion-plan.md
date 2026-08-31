# F5 coverage gap analysis and implementation plan

## Goal

Make the F5 material useful to an SDE1 debugging a request and an SDE2
designing, automating, upgrading, or recovering an LTM/GTM estate. The target
is a vendor-aware learning guide, not an instruction to change a production
BIG-IP. Examples use reserved or fictional names and distinguish documented
behavior from engineering inference.

## Current coverage

The repository already covers the basic LTM object model, VIPs, pools,
members, nodes, monitors, persistence, SNAT, client/server TLS profiles, GTM
Wide IPs and TTL, DDI, HA/failover, upgrades, SDK reads and idempotent writes,
SSH safety, and several incident case studies. It also has an LTM lab and
Python audit examples.

## Prioritized gaps

| Priority | Gap | Why it matters | Planned treatment |
| --- | --- | --- | --- |
| P0 | F5 traffic-processing order and packet tuples | Engineers often blame the wrong profile, policy, or NAT leg | New request-flow chapter with client/server tuple tables and debug transcript |
| P0 | HA state, config sync, traffic groups, mirroring, and split brain | “Standby is healthy” does not prove failover safety | Failure scenario plus state-transition diagram and recovery runbook |
| P0 | SDK/iControl REST production patterns | Basic examples do not cover auth tokens, pagination, transactions, async tasks, version drift, or unknown writes deeply enough | Dedicated SDK workbench with typed Python plan/apply/reconcile code and tests |
| P1 | TMM, CMP, SNAT/connection capacity, OneConnect, and route domains | These explain scaling, source-port exhaustion, and unexpected backend connection behavior | Architecture reference, capacity example, and packet evidence matrix |
| P1 | iRules versus Local Traffic Policies | Teams need to choose the least risky programmable control | Comparison table, migration example, and safe observability patterns |
| P1 | GTM/BIG-IP DNS probe and decision semantics | DNS steering is commonly treated as instantaneous load balancing | Resolver/LDNS/probe debug session with TTL, topology, and fallback evidence |
| P1 | DNSSEC, DNS listeners, synchronization, and delegated zones | Security and control-plane failures can look like application outages | GTM/DNS incident case study and validation commands |
| P1 | AS3, DO, TS, Ansible, and Terraform boundaries | SDK is only one automation surface in modern F5 estates | Tool-selection matrix and plan artifact examples |
| P2 | Route domains, VLAN/self-IP design, floating addresses, and admin/data-plane separation | Incorrect scope and return routing cause subtle outages | Layered architecture diagram and configuration-reading exercise |
| P2 | TLS profile inheritance, SNI/default certificates, re-encryption, OCSP, and mTLS at scale | Certificate success on one leg can hide failure on another | Multi-leg certificate debug session and rotation case |
| P2 | Health monitor design and false positives | A monitor can mark a usable member down or pass a broken app | Monitor contract examples, failure matrix, and test harness |
| P2 | Upgrade/rollback validation and observability | Version changes alter defaults, profiles, SDK fields, and state behavior | Preflight/postflight runbook and evidence checklist |

## Implementation units

1. Add a detailed F5 architecture and packet-processing reference covering
   TMM, VLANs, self IPs, route domains, virtual servers, profiles, policies,
   iRules, pools, monitors, persistence, SNAT, OneConnect, and both traffic
   tuples.
2. Add an HA and lifecycle reference covering device-service clustering,
   config-sync versus state mirroring, traffic groups, failover triggers,
   connection draining, split-brain symptoms, upgrades, and rollback.
3. Add an F5 SDK/iControl REST workbench with read-only discovery, typed
   normalization, pagination, token/TLS handling, transactions, async task
   polling, retries, idempotency, optimistic concurrency, mocks, and plan
   artifacts. Include an example that never contacts a device by default.
4. Add GTM/BIG-IP DNS operations material for LDNS behavior, monitors, Wide IP
   methods, topology records, DNSSEC, TTL migration, delegation, and resolver-
   specific debug sessions.
5. Add a toolchain comparison for SDK, REST, AS3, DO, TS, Ansible, Terraform,
   tmsh, and SSH, including ownership and rollback boundaries.
6. Add at least four case studies: asymmetric return/SNAT exhaustion,
   split-brain or failed HA failover, GTM/DNSSEC steering failure, and an SDK
   partial-write/version-drift incident.
7. Add exercises that make learners produce a packet tuple map, monitor
   contract, SDK plan, certificate-chain report, and upgrade go/no-go decision.

## Acceptance criteria

- Every new reference has objectives, prerequisites, mental model, architecture
  diagram, worked scenario, failure modes, checklist, exercise, table, and at
  least eight explained interview questions.
- Every debug session identifies the symptom, timestamp, observations,
  competing hypotheses, commands or API reads, decision, fix, verification,
  and rollback.
- Every code sample is read-only or uses a local mock by default, validates TLS,
  avoids secrets, uses type hints, and handles unknown write outcomes.
- Mermaid diagrams are ASCII-only and show the relationship between control
  plane, data plane, and evidence sources.
- `./scripts/validate.sh`, Python compilation, request-path simulation, and
  internal-link checks pass before commit.

## This implementation pass

Completed topics 28–33: traffic processing/TMM, SDK workbench, LTM selection
and capacity, BIG-IP DNS operations, read-only troubleshooting, and the API
toolchain. The existing case-study set supplies certificate, monitor,
persistence, HA, GTM, SDK drift, and upgrade scenarios. The remaining
follow-up work is to add dedicated split-brain, DNSSEC/listener, and
partial-write case studies plus local F5 fixture demos.
