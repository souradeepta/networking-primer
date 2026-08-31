# 3. F5 BIG-IP LTM: local traffic

**Local Traffic Manager (LTM)** is the BIG-IP module commonly used to expose a
virtual server (often called a VIP), apply traffic policy, and select a local
backend. “Local” means its decision scope is typically a site or traffic
domain, not that packets are physically short-distance.

## Object model

| Object | Meaning | SDE question |
| --- | --- | --- |
| Virtual server | Listener and policy entry point, usually an IP:port | Which address/port did the client reach? |
| Pool | Candidate backend group | Which service instances are eligible? |
| Pool member | Backend address and service port in a pool | Is this instance enabled and healthy? |
| Node | Address-level backend object | Is the host reachable? |
| Monitor | Active health test assigned to a node/member/pool | Does it test meaningful readiness? |
| Profile | Protocol/traffic behavior, such as TCP, HTTP, or TLS | What behavior changes at the VIP? |
| SNAT | Source-address translation toward the backend | Can backend replies return through LTM? |

F5's virtual-server, pool, node, and monitor configuration objects are
documented in the F5 TMSH reference. A monitor result can affect eligibility;
the exact inheritance and availability state depend on attachment scope and
configuration.

## Detailed architecture

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#111111', 'primaryBorderColor': '#222222', 'lineColor': '#222222'}}}%%
flowchart TB
    Client[Client 198.51.100.24] -->|TCP 443| VIP[Virtual server 203.0.113.20:443]
    VIP --> TLS[TLS and HTTP profiles]
    TLS --> Policy[Virtual-server policy]
    Policy --> Pool[web pool]
    Monitor[HTTPS readiness monitor] -. updates health .-> Pool
    Pool --> M1[Member 10.10.1.11:8443]
    Pool --> M2[Member 10.10.1.12:8443]
    SNAT[SNAT address 10.10.1.5] -. source rewrite .-> M1
    SNAT -. source rewrite .-> M2
    M1 --> App1[Application instance A]
    M2 --> App2[Application instance B]
```

This is conceptual: the processing order and available features depend on the
virtual server, profiles, policy, mode, and BIG-IP version.

## Connection lifecycle: UML-style sequence

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#111111', 'primaryBorderColor': '#222222', 'lineColor': '#222222'}}}%%
sequenceDiagram
    participant C as Client
    participant V as LTM virtual server
    participant M as Health monitor
    participant P as Pool
    participant B as Selected member
    M->>B: Periodic health request
    B-->>M: Expected response
    M->>P: Mark eligible
    C->>V: SYN then TLS and HTTP
    V->>P: Select eligible member
    P-->>V: Member B
    V->>B: Backend connection or forwarded flow
    B-->>V: HTTP response
    V-->>C: HTTP response
```

## Health checks are a contract

A TCP monitor can show that a port accepts connections; it does not prove the
application can serve a correct checkout. Prefer a lightweight endpoint that
tests the dependencies needed for the traffic class being admitted. Avoid
making it so expensive that the monitor itself harms the service.

Choose the failure policy deliberately:

| Choice | Benefit | Cost/risk |
| --- | --- | --- |
| Fast monitor interval | Quicker removal | More probe traffic; transient sensitivity |
| Slow monitor interval | Fewer probes, less flapping | Longer exposure to a bad member |
| Shallow TCP probe | Simple signal | May route traffic to a broken application |
| Deep readiness probe | Better admission signal | Can couple health to fragile dependencies |

## Load-balancing methods and persistence

Common policies include round robin, ratio/weighted selection, least
connections, and fastest-response-style policies. A policy only selects among
the **eligible** members it can observe; it does not manufacture capacity.

Persistence (for example a cookie, source address, or application token) can
keep related requests on one member. It can also create hot spots and make
draining slower. Use it only when the application state design requires it;
prefer externally shared state when that is viable.

## TLS termination, re-encryption, and passthrough

| Pattern | LTM can inspect HTTP? | Backend sees TLS? | Key consideration |
| --- | --- | --- | --- |
| Terminate | Yes | Not on that hop | Protect backend hop and client identity headers |
| Terminate then re-encrypt | Yes | Yes, new TLS session | Manage both TLS policies/certificates |
| Passthrough | Usually no L7 inspection | Yes, client session | Less L7 control at LTM |

Never assume `X-Forwarded-For` is trustworthy from the public Internet. Strip
or overwrite it at a trusted boundary and document which proxy hops may add it.

## LTM troubleshooting order

1. Identify the exact VIP, port, client network, timestamp, and error.
2. Check virtual-server availability and whether the flow matched the expected
   listener/policy.
3. Check pool/member availability, monitor output, and administrative state.
4. Compare client-side and server-side TCP/TLS evidence. Look for missing
   return traffic, resets, handshake mismatch, or timeout.
5. Verify SNAT/routing symmetry and backend listener behavior.
6. Correlate with application logs using a request ID; do not diagnose from a
   status code alone.
