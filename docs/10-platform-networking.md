# Platform networking: cloud ingress, routing, security, and SLOs

This bridge module connects the core request path to the platform concerns that
appear in an SDE2 on-call rotation. The long-form treatment is in the new
[cloud and Kubernetes chapter](../book/15-cloud-networking-and-kubernetes-ingress.md),
[BGP chapter](../book/16-bgp-anycast-and-multi-region.md), and
[WAF chapter](../book/17-network-security-waf-zero-trust.md).

## One request, several control planes

A browser request can cross a DNS control plane, a routing control plane, a
load-balancer data plane, a policy engine, and an application scheduler. Do
not assume that a successful DNS answer proves that the selected workload is
reachable. Each layer has its own state, timers, identity, and rollback.

```mermaid
%%{init: {"theme":"base", "themeVariables":{"primaryColor":"#eef6ff","primaryTextColor":"#111111","lineColor":"#333333"}}}%%
flowchart LR
  C[Client] --> R[Recursive DNS]
  R --> G[GTM or cloud DNS]
  G --> B[BGP or cloud route]
  B --> V[F5 VIP or ingress]
  V --> W[WAF and rate policy]
  W --> K[Kubernetes service]
  K --> A[Application pod]
  C -. telemetry .-> O[Metrics logs traces]
  V -. counters .-> O
  K -. events .-> O
```

| Layer | State to inspect | Typical owner | Evidence before changing it |
| --- | --- | --- | --- |
| DNS/GTM | answer, TTL, health result | network platform | `dig` from affected resolver locations |
| Routing | prefix, next hop, withdrawal | network/cloud | route table or BGP snapshot |
| LTM/ingress | VIP, policy, pool endpoints | traffic platform | virtual-server and endpoint counters |
| WAF/API | rule match, quota, identity | security platform | request ID and redacted event |
| Scheduler | service endpoints, readiness | platform team | Kubernetes events and endpoint slice |
| Application | latency, status, dependency calls | service team | trace and structured logs |

## Worked diagnostic path

Suppose `api.lab.example` resolves correctly, but clients receive intermittent
503 responses. First record a UTC timestamp, resolver, source location, VIP,
and request ID. Then compare three views:

1. `dig +short api.lab.example` and the authoritative answer. A stale GTM
   answer can send only some recursive resolvers to an unhealthy region.
2. LTM or ingress counters. A rising client-side 503 count with no matching
   server-side connection count suggests policy, endpoint, or admission
   failure before the application.
3. Service endpoint readiness. A pod can be running but absent from the
   endpoint set because its readiness probe failed.

The safe first action is a read-only comparison, not deleting endpoints or
lowering a health threshold. If the route and VIP are stable but endpoint
readiness flaps, inspect the probe path and dependency timeout. If only one
region is affected, compare its BGP advertisement and GTM health result with a
known-good region. “The load balancer is down” is a hypothesis, not evidence.

## Capacity and SLO connection

Define an SLI across the complete user path: an approved DNS answer, a
successful TCP/TLS connection, an acceptable HTTP response, and a latency
budget. Track saturation separately: VIP connection limits, SNAT port use,
WAF inspection CPU, ingress queue depth, node conntrack entries, and pod CPU.
An availability graph can remain green while latency burns the error budget.

For a monthly 99.9% availability target, the nominal budget is about 43.2
minutes. That number is useful only if failures are counted consistently. A
retrying client must not turn one user-visible outage into ten “successful”
internal attempts. Document whether planned maintenance, rejected policy
requests, and synthetic probes are included.

## Safe automation boundary

Automation should produce a plan before it changes a route, VIP, WAF policy, or
Kubernetes object. Include the current version, intended diff, blast radius,
pre-checks, post-checks, and rollback command. Use F5 SDK or REST for object
state, the Kubernetes API for declarative workload state, and SSH only for
approved read-only diagnostics when an API is unavailable. Never put tokens,
private keys, or certificate key material in logs.

## Questions and answers

1. **Why can DNS be healthy while the service is down?** DNS only returns a
   name-to-address answer; it does not guarantee the route, VIP, policy, or
   workload behind that address is healthy.
2. **What does a BGP withdrawal change?** It removes a path from route
   selection. Existing connections may still fail or drain; BGP is not an
   application health check.
3. **Why separate readiness from liveness?** Readiness controls traffic
   eligibility; liveness controls restart behavior. Conflating them can cause
   a restart storm during a dependency outage.
4. **When should WAF block versus observe?** Start in a measured, logged mode
   for a new rule, confirm false positives, then enforce with an explicit
   rollback threshold.
5. **What is a useful SLO symptom?** “99.9% successful HTTPS requests under
   750 ms” is testable; “the network is reliable” is not.
6. **Why inspect SNAT ports?** A VIP can be reachable while the proxy cannot
   open new backend flows because its translated source-port pool is exhausted.
7. **What does a 503 identify?** It identifies a response class, not a root
   cause. Correlate it with endpoint selection, policy events, and backend
   connection attempts.
8. **Why keep routing and application evidence together?** Their clocks and
   state transitions explain whether a failure is a path problem, an admission
   problem, or an application problem.
