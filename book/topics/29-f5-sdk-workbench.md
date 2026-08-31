# F5 SDK workbench

## Learning objectives

Design safe BIG-IP SDK automation with authentication, token handling,
pagination, transactions, asynchronous jobs, retries, idempotency, mocks, and
verification. Connect SDK objects to F5 LTM, DNS, DDI ownership, and change
review without exposing credentials.

## Prerequisites

Know Python, REST, JSON, HTTP status codes, TLS, Git review, and LTM object
relationships. Use only authorized lab endpoints and fictional names.

## Mental model

An SDK is a typed convenience layer over an API; it does not make a mutation
safe automatically. A workbench reads desired and observed state, authenticates
through an approved secret source, normalizes data, computes a diff, validates
invariants, applies a bounded transaction, and verifies effective behavior.
Tokens have lifetime and scope. Pagination means one response may not contain
all objects. Async tasks require polling and terminal-state handling. Retries
must distinguish transient transport errors from accepted mutations. These
facts imply an engineering rule: every write needs an idempotency strategy and
a recovery record.

## Diagram

```mermaid
%%{init: {"theme":"base", "themeVariables":{"primaryColor":"#ffffff","primaryTextColor":"#111111","lineColor":"#222222"}}}%%
flowchart LR
 D[Desired JSON] --> C[SDK client]
 C --> A[Auth token]
 A --> G[GET and pagination]
 G --> X[Diff and invariants]
 X --> T[Transaction or bounded write]
 T --> J[Async task status]
 J --> V[Verify and rollback record]
```

## Worked example

A job intends pool `pool_orders_lab` to contain two fictional members and a
specific monitor. It obtains a token through an environment-injected secret,
requests objects with explicit page size, and normalizes member ordering. The
diff identifies a missing monitor and stops for review. After approval, a
transaction groups dependent updates where supported; otherwise the job writes
one object and records the response. If the API returns an async task, polling
uses a deadline and backoff. Verification reads the effective pool, checks
member state and monitor association, and runs an authorized lab request.

| Concern | Safe workbench behavior | Evidence |
| --- | --- | --- |
| Auth | Scoped token, redacted logs | Token expiry and request ID |
| Read | Pagination and normalization | Complete object count |
| Apply | Transaction or ordered writes | Change version |
| Async | Deadline and terminal states | Task result |
| Verify | State plus behavior | Probe and rollback record |

## When this breaks

Expired tokens, clock skew, pagination omissions, stale reads, concurrent
operators, partial transactions, API version drift, non-idempotent retries,
and false-positive verification are common. A successful HTTP response may
mean only that a request was queued. SDK exceptions can hide a completed write,
so retrying blindly can duplicate objects or change an unintended target.
Mocks can also be too generous if they omit pagination, permission errors, or
async states. Test those cases explicitly with fixtures.

## Operational checklist

- Use TLS validation and scoped, injected credentials.
- Redact tokens, cookies, and sensitive device metadata from logs.
- Handle pagination, rate limits, and API version explicitly.
- Generate a normalized diff before mutation and require review.
- Use transactions or stable idempotent object identity where supported.
- Poll async jobs with deadlines and verify effective state afterward.
- Keep rollback state, request IDs, and mock regression fixtures.

## Implementation exercise

Write a standard-library fake SDK with `list_members(page)`, `apply_change`,
and `task_status`. Make pages return one member at a time. Test token expiry,
duplicate members, a timeout after accepted mutation, retry backoff, an async
failure, and a no-op rerun. Add a redacting logger assertion. Do not connect
the exercise to a live BIG-IP or include a real credential.

## Questions and answers

1. **Why use tokens carefully?** Tokens authorize API calls for a bounded scope and lifetime. They should be obtained from an approved secret mechanism, never committed or printed, and refreshed deliberately when expiry is detected.
2. **Why is pagination a correctness issue?** A first page can look complete while hiding members on later pages. Diffing incomplete data may remove valid objects or fail to detect drift, so automation must follow documented cursors or offsets.
3. **What is a transaction?** A transaction groups dependent configuration operations so the platform can validate and commit them together where supported. It is not a universal guarantee of rollback; verify platform semantics and handle partial or queued outcomes.
4. **How should retries work?** Retry only classified transient failures, use bounded exponential backoff and jitter, and include a stable idempotency key or object identity. After an ambiguous timeout, read state before deciding whether another write is safe.
5. **Why support async operations?** Large or distributed changes may return a task before completion. Polling needs a deadline, backoff, terminal-state parsing, and a final GET; treating task submission as success can hide failure.
6. **What makes a mock useful?** A useful mock models pagination, permissions, rate limits, malformed responses, token expiry, async transitions, and partial success. It should enforce the same invariants as production code without contacting a real target.
7. **How does idempotency prevent drift?** Stable names and desired-state comparisons make a rerun converge to one result instead of creating duplicates. Idempotency still requires verifying ownership and scope, because a stable name in the wrong partition can be harmful.
8. **What should post-change verification prove?** It should prove both effective configuration and intended behavior: object association, health state, listener response, and relevant DNS or certificate evidence. A 200 API response alone proves none of those end-to-end properties.

## SDK debug-session notes

When an SDK job fails, save the target hostname, BIG-IP software version,
partition, resource self-link, HTTP method, status code, elapsed time, and a
redacted correlation ID. Do not dump the request body if it may contain a
certificate key, token, or application secret. A 401 points to identity or
token expiry; a 403 points to role or partition authorization; a 404 requires
checking the tilde-qualified partition path and folder; a 409 commonly means
concurrent state or an existing object; a timeout means the write outcome is
unknown until a read reconciles it. These classifications are more useful than
retrying every exception.

A robust workbench has pure functions for normalization, diffing, and plan
generation, with a transport adapter behind an interface. Unit tests feed the
adapter fixtures for pagination, missing fields, asynchronous task states,
rate limiting, malformed JSON, and connection resets. A disposable BIG-IP
partition can provide contract tests for real resource paths, but CI should
default to mocks and fail if a live hostname or secret is present. Pin both the
SDK and Python versions, record the tested BIG-IP release, and detect
unsupported capabilities before planning a write.

For a change that creates a pool and attaches it to a virtual server, the plan
must include dependency order and rollback: verify or create the monitor,
create members, create or update the pool, attach the pool, then verify member
health and a safe listener probe. If a request times out after the pool create,
read the pool by stable partition-qualified name before repeating it. If the
virtual-server update partially applies, restore the captured prior pool
reference rather than deleting a shared pool. Transactions can reduce partial
state where supported, but they do not eliminate the need for read-back,
behavior checks, and an operator-approved recovery path.

An interview-quality SDK answer should always name the failure boundary. A
Python exception may mean DNS could not resolve the management host, TLS
validation rejected the certificate, authentication failed, the REST resource
was scoped to another partition, or the device accepted work that later
failed. Ask what was observed, what remains unknown, and which read-only call
will reduce that uncertainty. This is more reliable than memorizing one
manager class or assuming every BIG-IP release exposes identical fields.
The final report should state the exact API version, partition, owner, and
verification evidence so another engineer can reproduce the decision safely.

The same discipline applies to certificates and profiles. Uploading a
certificate object does not attach it to a client SSL profile, and attaching a
profile does not prove that the intended SNI name selects it. A plan should
model object dependencies, ownership, and verification separately. For a
server-side SSL change, verify the member hostname, trust store, SAN, chain,
and monitor behavior on the second leg. Keep the previous profile reference
until post-change probes and rollback evidence are complete.
