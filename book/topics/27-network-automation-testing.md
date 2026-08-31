# Network automation and testing

## Learning objectives

Design read-only discovery, declarative changes, validation, idempotency,
rollback, and synthetic tests for F5, DNS/DDI, and routed networks. Separate
what a script observed from what it inferred.

## Prerequisites

Know Python basics, REST and SSH concepts, Git review, DNS, load balancing, and
the difference between desired and observed state.

## Mental model

Automation is a controlled transformation from desired state to observed
state. A safe workflow authenticates through approved mechanisms, reads state,
computes a diff, validates invariants, obtains review, applies a bounded
change, and verifies behavior. Fact: an API returning success proves only that
the request was accepted. Inference: idempotency, dry runs, and independent
post-change tests reduce but never eliminate operational risk.

## Diagram

```mermaid
%%{init: {"theme":"base", "themeVariables":{"primaryColor":"#ffffff","primaryTextColor":"#111111","lineColor":"#222222"}}}%%
flowchart LR
 D[Desired state in review] --> V[Validator]
 V --> R[Read-only diff]
 R --> A[Approved change]
 A --> F[F5 or DDI API]
 F --> P[Post-change probes]
 P --> M[Evidence and rollback]
```

## Worked example

A job compares a fictional LTM pool's intended two members with a read-only
REST response. It normalizes ordering, detects a missing monitor, and fails
before sending a mutation. After review, the change is applied through the
documented API with a request ID. Verification checks member state, monitor
results, a lab request, and configuration version. DNS automation similarly
checks owner, TTL, and address overlap before publication. Secrets come from
approved injection, never source files or command history.

| Stage | Output | Safety property |
| --- | --- | --- |
| Read | Normalized state | No mutation |
| Diff | Explicit changes | Reviewable scope |
| Apply | Request and version | Auditable action |
| Verify | Health and behavior | Detect partial success |
| Recover | Known rollback | Bounded blast radius |

## When this breaks

Non-idempotent scripts, partial API success, stale reads, race conditions,
unbounded retries, missing permissions, and provider version drift cause
incidents. SSH command output can vary by prompt or release. A green pipeline
can still publish a wrong DNS answer if validation encoded the wrong intent.
Treat credentials, tenant names, and targets as sensitive; use fictional lab
fixtures in examples.

## Operational checklist

- Pin API schemas and validate provider version assumptions.
- Separate read, diff, approval, apply, and verify stages.
- Use idempotency keys or stable object identity where supported.
- Log request IDs and outcomes without secrets.
- Test rollback and partial failure in a disposable environment.
- Bound retries, timeouts, concurrency, and change scope.

## Implementation exercise

Implement a standard-library Python diff for two pool dictionaries. Normalize
member order, report additions and removals, and reject duplicate addresses.
Add tests for no-op rerun, malformed input, and partial verification. Extend
the exercise with a DNS TTL invariant and a dry-run report. Do not connect to
a live device or install packages.

## Questions and answers

1. **What makes automation idempotent?** Reapplying the same desired state produces no additional change after the first successful application. Stable identifiers, normalized comparisons, and explicit replace semantics help; blindly rerunning a command is not idempotency.
2. **Why separate validation from application?** Validation can reject unsafe scope, duplicate addresses, incompatible profiles, or missing ownership before a mutation. It also gives reviewers a concrete diff instead of asking them to trust implementation code.
3. **What is partial success?** A device may accept one object update while rejecting another, or a control plane may propagate slowly. Verification must inspect effective state and behavior, not only the final HTTP status from one request.
4. **When is SSH appropriate?** SSH can support approved read-only inspection or a documented emergency workflow when an API lacks a needed capability. Commands are version-sensitive and harder to parse, so they need constrained access and captured evidence.
5. **What should network tests assert?** Assert invariants such as intended listener, healthy member count, DNS ownership, certificate validity, and bounded response behavior. A single successful ping is not an end-to-end application test.
6. **How does rollback differ from undo?** Rollback restores a known-good desired state and verifies it; undo merely reverses the last command. A dependency may have changed meanwhile, so rollback plans need versioned state, ownership, and independent probes.

## Design notes and evidence

A useful automation repository keeps desired state, schemas, validators, test
fixtures, and operator documentation together. Read-only discovery should
normalize API ordering and omit secrets before producing a diff. Tests should
cover no-op reruns, duplicate members, malformed addresses, monitor ownership,
DNS TTL bounds, certificate expiry, and partial API responses. A deployment
should publish request IDs and configuration versions so an operator can match
device evidence to a Git review. F5 REST and SDK calls vary by release, while
SSH output is especially fragile; pin versions and fail closed on unknown
fields. Automation can validate a change but cannot infer business intent, so
ownership and approval remain explicit. The safest synthetic probes use
reserved addresses and disposable services, never credentials or real targets.
