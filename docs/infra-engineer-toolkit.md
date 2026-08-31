# Infra engineer toolkit

This toolkit is a **study and lab curriculum** for Unix and network debugging.
It is not authorization to inspect or change a system. Use a local fixture,
disposable lab, or explicitly approved target; record scope and timestamps;
redact credentials, private keys, customer data, and sensitive topology.

## A. Start here

| Track | Use it to practice | Main artifact |
| --- | --- | --- |
| Unix diagnostics | Process, socket, route, DNS, TLS, and resource evidence | [Unix debugging sessions](unix-debugging-sessions.md) |
| Tools and commands | Choose the smallest safe tool and interpret its limits | [Tools and commands](networking-tools-and-commands.md) |
| Symptom lookup | Move from a symptom to evidence and a falsifier | [Networking cheatsheets](networking-issue-cheatsheets.md) |
| Applied practice | Work bounded incidents and submit reviewable artifacts | [Runbooks and exercises](infra-engineer-runbooks-and-exercises.md) |

## B. Shared debugging contract

Use this frame before every session:

```text
impact | scope | timestamp | request path | tuple | observation
hypotheses | falsifier | authorization boundary | owner | next safe test
```

The preferred sequence is **scope -> observe -> localize -> hypothesize -> test
safely -> obtain approval -> change -> verify -> document**. A timeout is an
observation, not a root cause. A successful health check proves only its own
probe path.

## C. Evidence and safety

**Fact:** Unix and network tools observe particular layers and observation
points. **Inference:** correlating independent evidence reduces diagnostic risk,
but does not prove causality without a falsifier. Commands that mutate state—
route edits, firewall changes, `tc`, restarts, cache flushes, configuration
writes, and packet injection—belong in a separate approved change or experiment
plan.

## D. Interview progression

Begin with the cheat sheets, complete one Unix session, then answer a runbook
without looking at its resolution. For SDE2, explain mechanism, evidence,
trade-off, and rollback. For Staff, add ownership, cost, migration, adoption,
and what evidence would change the decision.
