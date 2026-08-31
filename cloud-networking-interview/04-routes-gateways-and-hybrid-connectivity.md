# Routes, Gateways, and Hybrid Cloud Connectivity

## A. Learning objectives

- Trace forward and reverse routes using longest-prefix reasoning.
- Explain gateways, peering, transit, VPN, and dedicated connectivity by behavior and ownership.
- Identify route propagation, overlapping CIDRs, asymmetric paths, and control-plane drift.
- Compare AWS and GCP hybrid connectivity without assuming transitivity or identical scopes.
- Construct an evidence-led diagnosis for a hybrid timeout.

## B. Prerequisites

Read [Cloud Networking Foundations](01-cloud-network-foundations.md), [Virtual Network Boundaries](02-virtual-network-boundaries-and-design.md), and [Subnet and IP Planning](03-subnet-and-ip-address-planning.md). Review the route and packet material in [the addressing chapter](../book/02-addressing-subnetting-routing.md) and BGP fundamentals in [the BGP chapter](../book/16-bgp-anycast-and-multi-region.md). You should know that a route is a forwarding decision, not permission to use the destination.

## C. Route and gateway mental model

For a packet, routing answers “which next hop should receive this destination?” A gateway is a role in that path: an internet edge, NAT device, VPN tunnel, peering attachment, transit router, proxy, or inspection appliance. Some gateways are stateful and translate or inspect traffic; others only forward. A route that points to a gateway does not prove that the gateway has a usable attachment, policy, capacity, or return route.

Use the same sequence on both directions:

1. Identify the source and destination address actually used after DNS and translation.
2. Find the most specific matching route at the sender.
3. Follow the next hop and any route advertisement or policy that installed it.
4. Evaluate packet policy, tunnel state, NAT, and inspection behavior.
5. Repeat for the response destination, which may be the translated source.

Hybrid connectivity adds another control plane. A data center router, cloud route controller, VPN endpoint, or dedicated interconnect may exchange prefixes dynamically. BGP session health is not the same as application health: a session can be established while an unwanted route is advertised, a return path is missing, or an intermediate firewall rejects traffic. Staff answers name prefix filters, maximum-prefix protection, change ownership, and rollback.

Peering is often deliberately non-transitive. Transit may provide centralized connectivity, but it introduces shared capacity, route-policy, and failure dependencies. VPN provides encryption over an underlying path, yet tunnel “up” can coexist with MTU, fragmentation, route, or policy failures. Dedicated links can improve predictable capacity but do not make application dependencies highly available automatically.

## D. AWS and GCP comparison

**Vendor terminology:** AWS commonly uses route tables, VPC peering, Transit Gateway, Site-to-Site VPN, and Direct Connect. Google Cloud uses VPC routes, Cloud Router, Cloud VPN, Interconnect, VPC Network Peering, and additional connectivity products. The terms describe provider mechanisms, not a universal topology.

| Mechanism | AWS example | Google Cloud example | Compare explicitly |
| --- | --- | --- | --- |
| Static or local routing | VPC route tables | VPC routes and subnet behavior | Scope, association, priority, and propagation. |
| Central transit | Transit Gateway | Network Connectivity Center or hub patterns | Transitivity, route policy, attachment limits, and cost. |
| Encrypted hybrid path | Site-to-Site VPN | Cloud VPN | Tunnel health, BGP/static mode, MTU, and failover. |
| Dedicated path | Direct Connect | Cloud Interconnect | Redundancy, provider demarcation, routing ownership, and maintenance. |
| Dynamic routing | BGP with gateway or transit features | Cloud Router with BGP | Advertised prefixes, custom policies, and regional/global scope. |

**Fact:** [AWS route tables](https://docs.aws.amazon.com/vpc/latest/userguide/route-table-options.html) and [Google Cloud routes](https://cloud.google.com/vpc/docs/routes) have provider-specific scope and behavior. **Inference:** Ask whether a connection is transitive, which prefixes propagate, and who owns the return path before selecting a product. Never infer that a healthy BGP session means every application flow is healthy.

## E. Worked scenario: asymmetric hybrid flow

Fictional `warehouse-a` at `10.70.4.25` calls cloud `inventory` at `10.80.6.14` over a VPN. The forward path selects a specific `10.80.0.0/16` route into the tunnel. The inventory response is destined for `10.70.4.25`, but the cloud side learned only `10.70.0.0/17`; the actual address is outside that prefix. The SYN leaves, the response has no valid return route, and the client times out.

The calculation is simple but useful: `10.70.4.25` belongs to `10.70.0.0/17` because the third-octet boundary for `/17` covers 0 through 127. If the warehouse address had been `10.70.200.25`, the same advertisement would not cover it. The interview answer should inspect both route tables and advertisements, then verify tunnel counters and policy. Adding a default route may hide the symptom while expanding the blast radius, so it is not a first fix.

## F. Diagram: route selection

```mermaid
%%{init: {'theme':'base','themeVariables': {'primaryTextColor':'#111827','lineColor':'#374151'}}}%%
flowchart LR
    A[Source workload] --> B[Longest prefix lookup]
    B --> C[Gateway or local interface]
    C --> D[Tunnel or transit attachment]
    D --> E[Destination service]
    E --> F[Reverse lookup]
    F --> A
```

## G. Diagram: hybrid control and data planes

```mermaid
%%{init: {'theme':'base','themeVariables': {'primaryTextColor':'#111827','lineColor':'#374151'}}}%%
flowchart TD
    R[Data center router] -->|BGP prefixes| C[Cloud route controller]
    C --> T[Tunnel or dedicated attachment]
    T --> V[Cloud route table]
    W[Workload packet] --> V
    V --> T
    T --> R
```

## H. Failure, evidence, and falsifiers

| Hypothesis | Evidence | Falsifier |
| --- | --- | --- |
| Missing return route | Both route lookups and advertisements | Specific routes exist in both directions |
| Tunnel failure | Tunnel counters, negotiation, and path evidence | Packets traverse and responses return |
| Bad prefix advertisement | BGP received and sent route sets | Exact intended prefixes are accepted |
| MTU or fragmentation issue | Packet size tests and retransmission pattern | Small and large payloads both succeed |
| Policy denies hybrid flow | Firewall or inspection decision | Flow is explicitly accepted at each boundary |
| Transit is saturated | Interface, queue, and latency metrics | Capacity remains below safe headroom |

## I. Exercises

### I.1 Timed whiteboard: hub-and-spoke route policy

Take 20 minutes. Draw two cloud networks, one data center, a shared inspection point, and a partner network. Mark which prefixes are advertised, which paths are transitive, and how the response returns. Add a failure of the primary tunnel and explain convergence. Follow-up: the partner has an overlapping CIDR; propose a proxy or translation boundary and discuss source identity.

### I.2 Evidence-led debugging: VPN is up, API is down

Take 25 minutes. Build a command-agnostic evidence plan: resolved address, route selection, BGP prefixes, tunnel counters, MTU, firewall decisions, NAT state, and service logs. Rank evidence by ability to falsify hypotheses. Follow-up: a route exists but packets are absent from flow logs; explain whether the observation points to the wrong interface, logging scope, or an earlier DNS/client failure.

## J. Interview questions and direct answers

### J.1 SDE2: Why inspect the reverse route?

**Answer:** Responses have their own destination and can select a different path. Missing advertisements, asymmetric policy, NAT, or an inspection device can permit the request while dropping the response. A complete diagnosis traces both directions using the actual post-translation addresses.

### J.2 SDE2: What does longest-prefix match do?

**Answer:** It selects the most specific matching destination prefix among available routes. It does not prove that the next hop is healthy or permitted. If two routes have the same specificity, provider-specific priority and state may decide, so verify the relevant selection rules.

### J.3 SDE2: Is a VPN tunnel being up enough?

**Answer:** No. It proves a control or negotiation state, not end-to-end application success. Verify prefixes, route installation, MTU, policy, tunnel counters, and a real protocol exchange. A tunnel can be healthy while the wrong network is advertised or a return route is absent.

### J.4 SDE2: Peering or transit for two networks?

**Answer:** For two stable networks with a narrow relationship, peering may be simpler. For many networks or centralized route and inspection policy, transit may be more manageable. I would compare transitivity, limits, cost, ownership, route propagation, and failure blast radius.

### J.5 Staff: How do you design hybrid connectivity for failure?

**Answer:** Use independent paths and devices where justified, explicit prefix filters, tested convergence, application timeouts that tolerate failover, and evidence for tunnel, route, and service state. Avoid declaring success based on redundant circuits alone. Exercise failure and include rollback and ownership for both cloud and data-center teams.

### J.6 Staff: How do you protect a shared route controller?

**Answer:** Separate desired intent from learned state, review prefix changes, constrain advertisements, apply maximum-prefix and loop protections, alert on unexpected route deltas, and keep a tested last-known-good configuration. Changes need an owner and a bounded blast radius; a central controller deserves stricter change policy because its reach is broad.

### J.7 Staff: How should a design handle overlapping CIDRs?

**Answer:** Prefer renumbering because it preserves transparent identity and simpler evidence. If impossible, isolate the overlap behind a proxy or carefully bounded translation, document which identity is visible on each side, and test return paths and logs. Do not connect overlapping domains and hope route priority resolves it.

### J.8 SDE2: What evidence distinguishes route failure from firewall failure?

**Answer:** A route lookup and packet/flow observation establish whether forwarding is attempted. A policy decision or counter shows whether a packet was evaluated and rejected. If no packet reaches the policy boundary, investigate an earlier route or interface issue; if it reaches and is denied, the policy hypothesis gains support.

## K. Advanced route review: forwarding, convergence, and hybrid failure

### K.1 Packet and request tuple walk-through

Assume an application in `10.81.12.44:443` calls an on-premises database at `172.22.40.15:5432`. Trace `(10.81.12.44:443 -> 172.22.40.15:5432, TCP)` through the cloud subnet route, transit or VPN attachment, cloud edge, customer router, database firewall, and the reverse path. At each boundary ask: which destination prefix matched, which next hop won, was the route learned or static, and what source address did the next device observe? A VPN control session being established is separate from this data-plane tuple.

Then trace the request contract: DNS name, TLS or database identity, timeout, and correlation ID. If a proxy or translation layer exists, record both tuples. An asymmetric path can allow SYN in and lose SYN-ACK out even though each local route table appears plausible. A Staff answer draws forward and reverse paths separately and identifies the state owner.

### K.2 Assumptions to calculation

Suppose the primary hybrid path carries 700 Mbps peak and the design requires operation after one path fails, with 25% headroom. If there are two equal paths and either may be lost, each surviving path must support `700 x 1.25 = 875 Mbps`; the normal design should not assume both paths are available for safety. If encryption and inspection overhead reduce usable capacity by an assumed 15%, provisioned link capacity should be at least `875 / 0.85 = 1,030 Mbps`, rounded up to the next supported tier. These are engineering assumptions, not provider guarantees.

Falsify the congestion hypothesis with interface and queue evidence below the calculated threshold during the incident. Conversely, high retransmission with low link utilization should redirect investigation toward MTU, route asymmetry, policy, or an application timeout rather than adding bandwidth.

### K.3 Provider non-equivalence and verification boundary

AWS route tables, Transit Gateway, Site-to-Site VPN, Direct Connect, and BGP have different route scope, propagation, attachment, and policy behavior from GCP VPC routes, Cloud Router, Cloud VPN, Interconnect, and Network Connectivity Center. “Transit” is an architectural role, not a guarantee that two provider transit products have equal transitivity, inspection insertion, route priority, or failure convergence. AWS subnet association should not be generalized to GCP’s global VPC route model.

Label provider behavior as **Fact** or **Vendor terminology** and comparison conclusions as **Inference**. Verify advertised and received prefixes, route priority, regional/global scope, BGP timers and policies, MTU, quotas, and maintenance behavior for the exact account/project, region, attachment, and release. A strong answer names the route lookup or provider documentation that will confirm the assumption.

### K.4 Evidence, blast radius, and rollback

Evidence should be ordered from intent to forwarding to application: desired prefixes, learned routes, effective route selection, tunnel counters, packet/flow records, transport retransmission, and service logs. “Tunnel up” falsifies only a negotiation failure. “Route present” falsifies only a missing-route hypothesis for that scope; it does not prove the selected next hop is healthy. An MTU test that works for small packets but fails with the application’s payload is especially valuable because it explains protocol-specific symptoms.

Route changes can affect every prefix behind a shared attachment. Before rollout, define changed advertisements, affected spokes, failover path, convergence budget, and a last-known-good route policy. Canary a narrow prefix, enforce maximum-prefix and loop protections, observe both directions, and keep rollback available. Withdrawals can be slower or riskier than additions, and existing sessions may remain pinned; rollback must include connection draining and application retry behavior.

### K.5 Follow-up interview questions and substantive answers

**Follow-up 1: Both sides show the route, but the request still times out. What do you check?**

**Answer:** I verify the exact longest-prefix winner and next-hop state on both directions, then inspect tunnel counters, MTU, policy, NAT, and packet evidence at each demarcation. I compare a small control payload with the real protocol. A route entry is intent; an observed bidirectional handshake is stronger evidence.

**Follow-up 2: Would you advertise all cloud prefixes to the data center?**

**Answer:** Only if the operational and security model requires it. Summarization can reduce route scale but may create a broader blast radius and send traffic to an attachment that cannot reach every component. I would advertise explicit, owned prefixes with filters, document failure behavior, and test whether summarization changes the return path.

**Follow-up 3: When is automatic failover a liability?**

**Answer:** It is a liability when route convergence is faster than application or data readiness, when both paths share a hidden failure, or when oscillation causes repeated connection loss. I would gate failover on path health and service readiness, add hold-down or dampening where appropriate, and measure recovery against the RTO rather than celebrating route convergence alone.

## L. References and evidence labels

- **Fact:** [AWS route options](https://docs.aws.amazon.com/vpc/latest/userguide/route-table-options.html), [AWS Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html), and [Google Cloud routes](https://cloud.google.com/vpc/docs/routes).
- **Vendor terminology:** [AWS Site-to-Site VPN](https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html), [Google Cloud VPN](https://cloud.google.com/network-connectivity/docs/vpn/concepts/overview), and [Cloud Router](https://cloud.google.com/network-connectivity/docs/router/concepts/overview).
- **Inference:** The route troubleshooting sequence extends [BGP and anycast](../book/16-bgp-anycast-and-multi-region.md) and [network observability](../book/12-observability-and-troubleshooting.md).
- [NAT and conntrack](../book/topics/24-nat-conntrack-and-snat.md) covers translation and state once a route exists.
