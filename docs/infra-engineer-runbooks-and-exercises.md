# Infra engineer runbooks and exercises

These are **training runbooks**. They stop at diagnosis, evidence, and an
approved change boundary. They do not authorize production mutation.

## A. Runbook — unreachable service

1. Record impact, client namespace, exact name, destination port, protocol, and UTC time.
2. Resolve the name from the failing context; record answer, TTL, and resolver.
3. Run `ip route get <destination>`; record source, interface, next hop, and policy table.
4. Check the local listener with `ss`; do not restart it as a first step.
5. Run one bounded TCP probe from an authorized client.
6. Capture a short packet sample if approved; classify SYN silence, reset, retransmit, or completion.
7. Compare NAT/conntrack, firewall policy, return route, and listener evidence.
8. State hypothesis, falsifier, owner, containment, rollback boundary, and verification.

## B. Runbook — wrong certificate or TLS failure

1. Confirm the exact hostname, VIP, port, terminating hop, and intended SNI.
2. Capture served leaf and chain metadata with `openssl s_client`.
3. Compare SAN, issuer, validity, trust bundle, EKU, clock, ALPN, and profile.
4. Test each proxy TLS leg separately; do not assume backend plaintext.
5. Preserve redacted evidence and never disable verification to “prove” reachability.
6. If approved, canary the profile or certificate reference and retain rollback state.
7. Verify representative clients, negative cases, expiry telemetry, and both legs.

## C. Runbook — intermittent 503 or 504

1. Identify the responding hop using headers, logs, timing, and correlation ID.
2. Compare successful and failed requests by resolver, region, tenant, and protocol.
3. Inspect pool eligibility, monitor request/receive rules, persistence, SNAT, queues, and retries.
4. Compare origin latency, connection age, dependency status, and resource saturation.
5. Avoid clearing persistence or raising timeouts until the mechanism is evidenced.
6. Propose the smallest reviewed correction with a canary and rollback.
7. Verify error rate, p99 latency, member balance, retry amplification, and dependency load.

## D. Runbook — suspected change regression

1. Build a timeline of deploys, config diffs, DNS, certificates, routes, alerts, and clock uncertainty.
2. Compare intended state, effective state, API task status, and observed data-plane behavior.
3. Define reversible containment and identify incident, service, and change owners.
4. Check whether rollback dependencies also changed; reverse commands are not automatically safe.
5. Canary containment or rollback, then verify the complete request path.
6. Preserve evidence and record what changed, who approved it, and why recovery is believed complete.

## E. Implementation exercise set

These are implementation-oriented assignments, not prompts to run arbitrary
commands against production. Each exercise should produce a small repository
artifact: code or a captured lab result, automated tests, a README, and a short
diagnostic explanation. Use Python’s standard library unless the exercise says
otherwise.

### E.1 Socket census and saturation report

**Goal:** Build `socket_census.py` that reads a fixture containing listener and
connection rows and classifies socket state, ownership, and risk.

**Input contract:** Accept JSON lines with `pid`, `process`, `local`, `peer`,
`state`, `age_seconds`, and `bytes`. Support missing `peer` for listeners and
unknown states without crashing.

**Requirements:** Report counts by state, top local ports, oldest connections,
and a warning when `CLOSE-WAIT`, `SYN-RECV`, or file-descriptor use exceeds a
configurable threshold. Keep the report deterministic and never inspect a live
host by default.

**Required tests:** empty input; malformed row; multiple processes on one port;
IPv4 and IPv6 addresses; `CLOSE-WAIT` versus `TIME-WAIT`; threshold exactly at,
below, and above the limit. Explain why a socket count is evidence, not proof
of a kernel or application defect.

**Deliverable:** code, at least eight tests, sample input/output, and a note
mapping each warning to a falsifying observation. Target **O(n)** processing and
bounded memory proportional to the number of retained summaries.

### E.2 Longest-prefix route lookup

**Goal:** Implement `route_lookup.py` for IPv4 and IPv6 using standard-library
`ipaddress`.

**Input contract:** `lookup(destination, routes)` returns the next hop for the
most-specific matching prefix. A route contains `prefix`, `next_hop`, `source`,
and optional `metric`. For equal prefixes, choose the lowest metric; if still
tied, preserve explicit source precedence.

**Requirements:** Distinguish route installation from forwarding lookup in the
README. Reject invalid prefixes, support a default route, and return an
explicit “no route” result. Do not claim this models every vendor’s RIB/FIB
algorithm.

**Required tests:** `/32` over `/24` and `/0`; IPv6 `/128`; equal-prefix
metrics; overlapping private ranges; invalid addresses; no route; and a route
present in the input but marked `installed=false`.

**Deliverable:** implementation, tests, complexity analysis, and a table showing
RIB candidates versus installed FIB entries. Target **O(r)** lookup first, then
describe how a trie could improve repeated lookups.

### E.3 DNS cache with expiry and negative answers

**Goal:** Implement a deterministic in-memory DNS cache model with injected
time, not a resolver or network client.

**Input contract:** `put(name, record_type, answer, ttl, now, negative=False)`
and `get(name, record_type, now)` return a cache hit, remaining TTL, or miss.
Normalize names case-insensitively and treat a trailing dot consistently.

**Requirements:** Never return expired data; distinguish positive and negative
entries; expose remaining TTL; support replacement; and keep a query log that
records cache hit/miss without recording secrets.

**Required tests:** TTL zero; time exactly at expiry; case and trailing-dot
normalization; negative caching; replacement before expiry; empty answer; and
large time jumps. Explain why lowering an authoritative TTL cannot invalidate
an already cached response.

**Deliverable:** module, tests, example timeline, and a short explanation of
authoritative versus recursive versus local cache evidence. Target **O(1)**
average lookup and make time fully injectable for repeatable tests.

### E.4 TCP evidence timeline classifier

**Goal:** Implement `tcp_timeline.py` that classifies a simplified packet
fixture into connection outcomes without pretending to identify root cause.

**Input contract:** Events contain timestamp, direction, flags, source, and
destination. Support `SYN`, `SYN-ACK`, `ACK`, `RST`, `FIN`, and retransmission
markers.

**Requirements:** Detect completed handshake, SYN silence, reset before
handshake, incomplete final ACK, and retransmission. Identify the reset sender
and observation point. Keep packet parsing separate from interpretation.

**Required tests:** normal handshake; repeated SYN; server reset; client reset;
SYN-ACK with no ACK; simultaneous close; reordered timestamps; and an empty
capture. The report must list at least two possible causes for each non-success
classification and one falsifier.

**Deliverable:** code, fixture corpus, tests, and an annotated timeline. Target
**O(n log n)** if sorting is needed; document assumptions about clock accuracy.

### E.5 TLS certificate and SNI inventory

**Goal:** Build `tls_inventory.py` for supplied certificate metadata fixtures.
Do not fetch endpoints or handle private keys.

**Input contract:** JSON records contain hostname, SNI, SANs, issuer, not-before,
not-after, ALPN, trust-store name, and termination hop.

**Requirements:** Detect hostname/SAN mismatch, expiry window, duplicate
certificate assignments, missing ALPN, and inconsistent trust-store ownership.
Produce a redacted report with no key material.

**Required tests:** exact SAN match; wildcard boundary; expired leaf; valid leaf
with wrong issuer; multiple SNI names; two TLS legs; clock at boundary; and
missing fields. Explain why a valid certificate does not prove backend health or
application authorization.

**Deliverable:** code, tests, sample report, and an SDE2/Staff change plan for
overlap rotation. Target **O(n log n)** for sorting expiry and document the
hostname-matching assumptions.

### E.6 MTU and encapsulation calculator

**Goal:** Implement `mtu_model.py` that calculates safe inner payload size
from underlay MTU and explicit encapsulation overhead.

**Input contract:** `effective_mtu(underlay_mtu, overhead)` plus optional TCP
header and MSS values. Reject negative overhead and payload larger than the
underlay.

**Requirements:** Show the arithmetic, distinguish IPv4 and IPv6 assumptions,
and model fragmentation/PMTUD as evidence states rather than silently “fixing”
the network. Include VXLAN as a named example only with documented overhead
assumptions.

**Required tests:** zero overhead; exact boundary; oversized payload; IPv4 and
IPv6 headers; multiple encapsulation layers; and invalid values. Explain why
small probes can succeed while large responses stall.

**Deliverable:** calculator, tests, a table of inputs/results, and a safe lab
experiment plan with a stop condition. Target **O(1)** calculation.

### E.7 Proxy tuple and SNAT capacity model

**Goal:** Implement `tuple_model.py` to render client-side and server-side
five-tuples and estimate translation-port capacity.

**Input contract:** Source/destination address, ports, protocol, proxy address,
translation addresses, and concurrent-flow count. Preserve IPv4/IPv6 text and
protocol identity.

**Requirements:** Show that a proxy creates separate legs; calculate usable
ports per translation address for a stated destination tuple; flag collisions;
and make assumptions about port range and reuse explicit.

**Required tests:** no SNAT; one SNAT address; multiple destination tuples;
long-lived flows; port exhaustion; IPv6 clients; and invalid port ranges. Explain
why adding translation addresses changes capacity and may change source identity.

**Deliverable:** implementation, tests, tuple tables, and a staged capacity
recommendation. Target **O(n)** for flow evaluation.

### E.8 Incident replay and reconciliation

**Goal:** Turn one existing case study into a replayable fixture and implement
`incident_replay.py` that orders evidence, hypotheses, tests, and decisions.

**Input contract:** Timestamped observations, owners, hypotheses, falsifiers,
actions, authorization boundaries, and verification results.

**Requirements:** Reject an action without scope or owner; distinguish observed
facts from inferences; mark unknown outcomes; and generate a timeline plus
decision record. The tool must never execute the recorded commands.

**Required tests:** missing timestamp; duplicate observation; conflicting
hypotheses; unsafe mutation; failed rollback; and verification that contradicts
the initial hypothesis.

**Deliverable:** fixture, code, tests, a postmortem-style report, and a Staff
reflection covering ownership, customer impact, cost, migration, and durable
prevention. Target **O(n log n)** timeline ordering and explain clock skew.

## F. Exercise submission template

```markdown
# Exercise: <name>

## A. Scope and authorization
## B. Assumptions and topology
## C. Commands and timestamps
## D. Observed evidence
## E. Competing hypotheses
## F. Falsifier and next safe test
## G. Decision, owner, and rollback boundary
## H. Verification and lessons
```

## G. Interview answer checklist

For SDE2, state the mechanism, evidence, trade-off, falsifier, and safe next
step. For Staff, also explain service ownership, customer/business impact,
capacity and cost, migration sequencing, adoption, and what evidence would
change the design. Never substitute a long command list for a causal model.

## H. Safety boundary

Do not flush caches, restart services, alter routes or firewall rules, inject
loss, scan broad ranges, delete Kubernetes objects, or test credentials as a
default exercise. Those actions require explicit authorization, target scope,
rate limits, stop conditions, an owner, and recovery verification.
