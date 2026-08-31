# Networking issue cheatsheets

These tables are starting points, not root-cause lookup tables. For every
symptom, collect the tuple, time, observation point, and a falsifier.

## A. DNS and service discovery

| Symptom | First checks | Falsifier or caveat |
| --- | --- | --- |
| `NXDOMAIN` | Exact name/type, authority, delegation, negative TTL | Authoritative `NOERROR` for the same name/type |
| `SERVFAIL` | DNSSEC chain, upstream timeout, delegation, clock | Validating resolver returns a current answer |
| Wrong address | Authoritative, recursive, local, split-horizon views | All views agree while client reaches old IP |
| Intermittent address | Multiple records, steering, cache age, locality | Single authoritative answer and fresh cache everywhere |
| Host resolves, pod fails | Pod resolver, search path, DNS egress, CNI policy | Same query succeeds from pod namespace |

## B. TCP, UDP, and MTU

| Symptom | Evidence sequence | Common wrong move |
| --- | --- | --- |
| SYN timeout | Listener -> route -> ACL -> return path -> capture | Raise application timeout |
| Immediate RST | Identify sender, socket state, policy, listener | Blame firewall without packet evidence |
| Connect works, request stalls | TLS -> HTTP -> queue -> dependency -> MTU | Claim TCP proves service health |
| Large payload stalls | PMTU, ICMP, MSS, retransmits, inner/outer headers | Raise MTU globally |
| New flows fail, old work | NAT/conntrack/ephemeral ports/backlog | Clear every connection |
| UDP only fails | UDP policy, listener, response path, fallback rate | Assume the service is TCP-only |

## C. TLS and HTTP

| Symptom | Check | Caveat |
| --- | --- | --- |
| Wrong certificate | Exact VIP, SNI, SAN, profile, chain | Testing without SNI gives a misleading default cert |
| Trust failure | Chain, trust store, EKU, hostname, clock | Replacing only leaf may not fix chain trust |
| TLS succeeds, HTTP fails | ALPN, headers, policy, route, origin response | Certificate validity is not authorization |
| 503 | Responding hop, member eligibility, monitor, origin status | Edge and origin can use 503 differently |
| 504 | Deadline, queue, upstream timing, retry count | More timeout can increase resource pressure |
| HTTP/2 reset | SETTINGS, stream state, flow windows, proxy limits | Do not reduce a stream error to TCP failure |

## D. Load balancers and proxies

| Symptom | Evidence sequence |
| --- | --- |
| No eligible members | Pool -> monitor request/receive -> member port -> route |
| Hot member | Selection method -> persistence key -> connection age -> capacity |
| Backend sees wrong source | Client/server tuples -> SNAT -> return route -> ACL |
| Drain never completes | New assignments -> active connections -> long-lived protocol -> timer |
| Health green, users fail | Probe Host/SNI/path -> user path -> dependency coverage |
| Only one region fails | Resolver locality -> DNS/GTM state -> regional VIP -> origin capacity |

## E. Linux host pressure

| Signal | What it suggests | Pair it with |
| --- | --- | --- |
| High run queue | CPU scheduling pressure | p99 latency, `pidstat`, CPU saturation |
| Low memory/reclaim | Memory pressure or cache churn | Major faults, swap, process RSS |
| FD limit reached | Listener/client creation failures | `/proc/<PID>/limits`, socket counts |
| Many `CLOSE-WAIT` | Application close-path leak | Process logs and connection age |
| Many `TIME-WAIT` | Connection churn | Reuse, source ports, destination tuples |
| Full filesystem/inodes | Logging or write failures | Mount, rotation policy, evidence retention |

## F. Kubernetes and cloud

| Symptom | Inspect | Boundary |
| --- | --- | --- |
| Ingress 404 | Ingress class, host/path, default backend | Controller implementation and route precedence |
| Empty service | Selector, readiness, EndpointSlice | API state does not prove packet delivery |
| Policy blocks DNS | CNI enforcement, egress rule, CoreDNS path | NetworkPolicy support is CNI/version-dependent |
| Private connection one-way | Route tables, SG/NACL, NAT, return path | Stateful/stateless semantics vary by platform |
| Cross-zone latency/cost | Locality, LB policy, egress path, bytes | Provider billing and routing defaults vary |

## G. Evidence ladder

1. **Name:** resolver, record, TTL, and viewpoint.
2. **Route:** source, destination, interface, next hop, and return route.
3. **Connect:** SYN/SYN-ACK/RST/retransmission and socket state.
4. **Secure:** SNI, certificate, trust, ALPN, and clock.
5. **Request:** status, headers, timing, selected member, and trace ID.
6. **Capacity:** queue, concurrency, ports, CPU, memory, quota, and dependency load.

Moving down this ladder without evidence from the earlier layer creates layer
confusion. Moving up it without checking capacity can mistake overload for an
application bug.
