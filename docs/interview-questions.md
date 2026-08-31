# Networking interview questions: SDE1 and SDE2

Use these to practice explaining trade-offs aloud. Strong answers state the
scope, identify missing facts, and avoid treating one error code as proof of a
single root cause.

## SDE1

1. **What is the difference between an IP address and a port?**
   An address reaches an interface/host in an IP network; a port identifies a
   transport endpoint/service on that host. A destination needs protocol too.
2. **What does a TCP three-way handshake establish?**
   It establishes connection state and confirms bidirectional reachability at
   the transport layer before application bytes are exchanged.
3. **Why can DNS be a cause when `curl` reaches the wrong environment?**
   A resolver can return a cached or incorrect A/AAAA/CNAME answer. Inspect
   the exact name, resolver, response, authority, and TTL.
4. **Timeout vs. connection refused?**
   Refused usually means the target responded that no listener accepted it;
   timeout means a response was not observed and needs path/firewall analysis.
5. **What does TLS add above TCP?**
   Encryption and peer authentication subject to certificate validation. TCP
   alone only provides a byte stream, not server identity.
6. **What is a load balancer health check?**
   A repeated test used to decide backend eligibility. Its depth must match the
   safety claim: port-open is weaker than application readiness.

## SDE2

1. **Contrast LTM and GTM/BIG-IP DNS.**
   LTM selects/handles local traffic at a virtual server; GTM/BIG-IP DNS
   returns DNS answers across sites. DNS caching makes their reaction times and
   units of balancing different.
2. **Why use SNAT at a load balancer?**
   It can force a symmetric return path through the load balancer when a
   backend otherwise routes replies elsewhere. It also changes source identity
   visibility and port capacity, so it is not free.
3. **How would you fail over a write-heavy multi-site service?**
   Start with data consistency/write ownership and recovery design, then ensure
   GTM policy, TTL/cache overlap, LTM capacity, and health signals reflect it.
   DNS steering cannot solve unsafe replication.
4. **Termination, re-encryption, or TLS passthrough?**
   Choose based on required L7 control, inspection, trust boundaries, upstream
   identity validation, and key-management policy. Re-encryption has two TLS
   validation points.
5. **What makes network automation safe?**
   Narrow desired state, read-before-write, least privilege, review,
   idempotency, preconditions, staged rollout, traffic verification, audit,
   and rollback.
6. **How does DDI prevent incidents?**
   It makes address allocation, DNS names, and DHCP configuration governed by
   explicit ownership, reducing duplicate addresses, stale records, and drift.
