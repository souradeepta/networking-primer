# Networking interview questions: SDE1 and SDE2

Use these to practice explaining trade-offs aloud. Strong answers state the
scope, identify missing facts, and avoid treating one error code as proof of a
single root cause.

## SDE1

1. **What is the difference between an IP address and a port?**
   An address reaches an interface or host in an IP network; a port identifies
   a transport endpoint on that host, and TCP and UDP have separate port
   spaces. For example, `203.0.113.10:443/tcp` identifies a different socket
   from `203.0.113.10:443/udp`. In an interview, mention that a load balancer
   can preserve the client tuple on its front side while creating a new
   server-side tuple, often with SNAT; verify both tuples when debugging.
2. **What does a TCP three-way handshake establish?**
   SYN, SYN-ACK, and ACK negotiate sequence numbers and establish state at
   both endpoints before application bytes are exchanged. It proves that
   packets can traverse the observed path at that moment, not that the
   application is healthy or that the return path will remain symmetric. A
   SYN timeout suggests filtering or loss, while a completed handshake followed
   by an HTTP timeout moves investigation toward TLS, proxy queues, or the
   server process.
3. **Why can DNS be a cause when `curl` reaches the wrong environment?**
   A recursive resolver can return a cached A/AAAA/CNAME answer that differs
   from the authoritative answer, and split-horizon views can intentionally
   differ by client network. Capture the exact name, query type, resolver,
   flags, answer, authority, and TTL with `dig`; then query an authoritative
   server for comparison. A correct answer can still lead to failure if the
   route or VIP behind it is wrong, so DNS evidence is only the first hop.
4. **Timeout vs. connection refused?**
   A TCP reset or connection-refused result means a response was received,
   commonly because no process is listening or a policy actively rejected the
   flow. A timeout means no usable response was observed, so inspect routes,
   ACLs, firewalls, MTU, and packet captures before blaming the application.
   On F5, distinguish a client-side refusal from a server-side connect timeout:
   the former implicates the VIP/listener, while the latter may implicate pool
   members or SNAT.
5. **What does TLS add above TCP?**
   TLS encrypts application records and authenticates a peer when certificate
   validation succeeds; TCP alone supplies only an ordered byte stream. The
   client checks hostname/SAN, validity dates, chain, and policy, while mTLS
   adds a client certificate check. At an F5 termination point, test the
   client-side certificate/SNI profile and the independent server-side trust
   profile because a successful first handshake does not prove re-encryption.
6. **What is a load balancer health check?**
   A repeated probe used to decide whether a backend is eligible for new
   traffic. A TCP-open check proves only that a socket accepted connections;
   an HTTP readiness check can verify status, headers, and a bounded dependency
   contract, but can also create load or flap when dependencies are unhealthy.
   Interview answers should mention interval, timeout, expected response,
   monitor source address, and the difference between monitor health and real
   user traffic.

## SDE2

1. **Contrast LTM and GTM/BIG-IP DNS.**
   LTM is the local data-plane proxy: a virtual server accepts a flow, applies
   profiles/policies, selects an eligible pool member, and may SNAT it. GTM or
   BIG-IP DNS is the DNS control-plane decision point: a Wide IP selects an
   answer from site or virtual-server pools. Because recursive resolvers cache
   answers and clients reuse connections, GTM failover is not instantaneous and
   does not rebalance an existing TCP flow.
2. **Why use SNAT at a load balancer?**
   SNAT rewrites the source address (and usually source port) on the
   load-balancer-to-member leg, making the member’s return route point back to
   the proxy when the client subnet is not routable there. The trade-off is that
   the application may see the SNAT address instead of the client and the
   translation address/tuple space is finite. Explain how you would inspect
   SNAT-creation failures and preserve the original client identity with a
   trusted header only when the proxy sanitizes and re-adds it.
3. **How would you fail over a write-heavy multi-site service?**
   Start with write ownership, replication lag, fencing, and a recovery point
   objective; otherwise DNS can send clients to a site that cannot safely accept
   writes. Define the GTM eligibility signal from those invariants, lower TTL
   ahead of the change, and confirm LTM, TLS, SNAT, and database capacity at the
   destination. During the event, compare authoritative answers with answers
   seen by affected resolvers because cached records and existing connections
   create a long tail. DNS steering cannot repair split-brain data.
4. **Termination, re-encryption, or TLS passthrough?**
   Termination at the proxy enables HTTP routing, WAF inspection, and simpler
   backend operations but makes the proxy a key-trust boundary. Re-encryption
   preserves encryption on the second leg and requires the proxy to validate
   the upstream name, chain, and often mTLS client identity. Passthrough keeps
   end-to-end keys at the application but prevents the L7 proxy from seeing
   HTTP fields; choose from the data classification, observability, and key
   ownership requirements rather than using one mode everywhere.
5. **What makes network automation safe?**
   Safe automation fetches and normalizes observed state, computes a narrow
   diff, checks version/partition/preconditions, and emits a reviewable plan
   before writing. It uses least-privilege SDK/REST credentials, idempotent
   reconciliation, bounded retries, staged canaries, post-change traffic
   checks, audit records, and a tested rollback. For F5, distinguish a REST
   request succeeding from the virtual server, pool, monitor, and dataplane
   actually converging.
6. **How does DDI prevent incidents?**
   DDI links DHCP allocation, DNS publication, and IPAM ownership so an address
   has an accountable source of truth. That reduces duplicate IPs, stale A or
   PTR records, exhausted scopes, and accidental reuse of VIP or SNAT space.
   It does not make drift impossible: compare exports, classify exceptions,
   reconcile in dependency order, and retain timestamps. When an LTM or GTM
   incident occurs, the ownership trail helps determine whether the fault is
   data, routing, policy, or the application.
