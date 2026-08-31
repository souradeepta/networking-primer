# Interview study plan

Use this plan with the [Staff rubric](staff-interview-rubric.md), [Staff design
review pack](staff-design-review-pack.md), and [Staff behavioral exercises](staff-behavioral-exercises.md).
Choose the SDE2 or Staff gate before starting; the same topic can be practiced
at different depths.

## Four-week plan

Week 1: Ethernet, IPv4/IPv6, routing, TCP/UDP/QUIC, DNS and DDI. Draw one
packet journey daily and answer five fundamentals questions.

Week 2: HTTP, proxies, LTM, BIG-IP DNS, TLS, mTLS, and caching. Run local
fixtures, build tuple tables, and practice three 10-minute drills.

Week 3: Kubernetes, overlays, BGP, observability, SLOs, capacity, and security.
Design one system and conduct two evidence-led simulations.

Week 4: REST/SDK, AS3/DO/TS, rollback, authorized testing, and incident
communication. Complete a full mock interview and review weak rubric scores.

## Six-week extension

Add week 5 for advanced F5 TMM/CMP, persistence, SNAT, iQuery, DNSSEC, and HA.
Add week 6 for system-design trade-offs, failure injection planning, and a
second mock interview with unfamiliar scenarios.

## Two-week sprint

Days 1-4 cover fundamentals and packet evidence. Days 5-8 cover DNS, LTM,
TLS, and Kubernetes. Days 9-11 cover automation and security. Days 12-14
complete drills, debugging exercises, and a timed design review.

## Measurement

Track rubric scores for mechanism, evidence, safety, trade-off, and verification.
Set a target of 3 or 4 in every category and no safety score below 3. Keep a
fact/inference ledger and revisit any answer that relied on an unverified
vendor default.

## Practice sources and gates

Use the [F5 bank](f5-interview-bank.md), [networking bank](networking-interview-bank.md),
[dialogue exercises](interview-dialogue-exercises.md), [simulation pack](interview-simulation-pack.md),
[whiteboard drills](interview-whiteboard-drills.md), and [system-design exercises](network-system-design-exercises.md)
as the weekly sources. A week is complete only when its answer, timed-drill,
lab, and self-score targets are recorded with dates and evidence. Do not move
to the next track if safety is below 3 or if the candidate cannot name a
falsifier for two consecutive scenarios.

## Role gates

| Gate | SDE2 | Staff |
| --- | --- | --- |
| Technical answers | Average 3/4; mechanism, evidence, safety, trade-off, verification | Average 3.5/4; add framing, ownership, quantification, and evolution |
| Design | Three timed designs with failure domains and rollback | Two designs with cost, migration, adoption, ownership, and failback |
| Implementation | Two tested Python exercises and one safe reconciliation exercise | Two reconciliation/design-oriented exercises with complexity and ambiguous-outcome handling |
| Incident | One evidence-led simulation with a falsifier | One ambiguous incident with stakeholder communication and durable prevention |
| Behavioral | Clear scope, action, and result | Influence across teams, dissent, measurable outcome, and durable change |

Record each attempt in a small log:

```text
date | role | prompt | assumptions | score by dimension | missed concept | next experiment
```

Do not claim readiness from reading completion alone. The exit gate requires
the relevant timed artifacts and a second attempt on an unfamiliar scenario.
