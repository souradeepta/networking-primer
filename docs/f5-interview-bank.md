# F5 role interview bank

This bank is a study aid for SDE1, SDE2, and network-automation interviews.
Names and addresses are fictional. BIG-IP DNS is the current product name;
GTM remains common historical terminology. AS3, DO, TS, FAST, and the BIG-IP
SDK are versioned toolchain components: consult the deployed release and
[F5 documentation](https://clouddocs.f5.com/) before relying on defaults.

## Role map

| Role | Expected depth | Evidence habit |
| --- | --- | --- |
| SDE1 | Trace DNS, TCP, TLS, HTTP, VIP, pool, and monitor symptoms | Capture tuple, time, status |
| SDE2 | Explain failure domains, capacity, HA, policy, and safe change | Compare hypotheses and rollback |
| Automation engineer | Model APIs, RBAC, declarations, retries, and tests | Diff desired/effective state |

## Interview questions and answers

### LTM

1. **How does a request traverse LTM?** A client resolves a VIP, opens a connection, and TMM matches the virtual server. Profiles interpret TCP, TLS, or HTTP; policies and iRules may alter behavior; a monitor-qualified pool member is selected. SNAT and routing determine the server-side tuple and return path. Verify each boundary with timestamps, tuples, profile names, pool state, and member evidence. A successful member probe does not prove the VIP path, and defaults vary by release.
2. **How do persistence and priority interact?** Persistence can pin a client to one eligible member while priority groups determine which members may receive traffic. During drain or failure, behavior depends on persistence scope, timeout, fallback, and configured selection method. Compare client key, member state, active connections, and selection reason. The trade-off is session affinity versus distribution; clearing all records can cause a surge. Test a narrow lab or canary case first.
3. **What causes SNAT exhaustion?** A translated source has finite ephemeral-port combinations for a destination and protocol. High concurrency, long-lived connections, or slow aging can exhaust allocation. Inspect SNAT counters, connection age, pool member tuple, and return route. Adding addresses increases capacity but changes source identity and policy. A timeout alone is not proof; correlate allocation errors with failed new flows and healthy monitor state.
4. **What does OneConnect change?** OneConnect can reuse server-side connections independently from client connections, enabling request-level distribution for suitable HTTP traffic. It changes connection counts and source visibility and may interact with persistence, headers, and application assumptions. Compare client and server captures and document profile ownership. It is a trade-off between connection efficiency and more complex observability, not a universal performance switch.
5. **How do you debug a 503?** Identify which hop emitted it, then record DNS, VIP, profile, policy, pool, monitor, selected member, route, SNAT, and timestamps. A local proxy 503 may mean no eligible member; an origin 503 is application evidence. Check competing hypotheses such as stale DNS, monitor mismatch, member refusal, and policy rejection. Use read-only inspection before changing pool or monitor configuration.
6. **What is TMM and CMP?** TMM is the BIG-IP traffic-processing component; CMP can distribute eligible work across TMM instances. Feature compatibility and shared state affect distribution, so inspect release-specific support and per-TMM counters. The caveat is that an aggregate health or throughput number can hide imbalance. Explain observations as facts and label causal conclusions as hypotheses until packet and state evidence agree.
7. **How should iRules be reviewed?** Identify event scope, conditions, pool or header side effects, logging volume, and interaction with profiles and policies. Read-only source review and bounded logs are safer than disabling a rule globally. The trade-off is flexibility versus complexity and CMP implications. Verify with a canary request and rollback plan, never with real credentials in a transcript.
8. **What makes a monitor useful?** Its source, protocol, URI, TLS name, expected response, interval, and timeout must represent the dependency being tested. A green monitor proves only that configured probe succeeded. Compare monitor evidence with user-path traces and application logs. A deeper monitor can improve signal but consumes capacity and may create dependency coupling.

### GTM / BIG-IP DNS

9. **How does a Wide IP answer work?** BIG-IP DNS receives a query on a listener, evaluates a Wide IP and pool, filters unavailable virtual servers using monitors or iQuery information, applies topology or other policy, and returns an address with TTL. Recursive caches delay change. Query the listener directly and compare recursive answers, source LDNS, TTL, pool state, and timestamps.
10. **What does iQuery provide?** iQuery exchanges BIG-IP system information used by DNS relationships and health decisions. It is distinct from client DNS. Inspect communication, object freshness, monitor state, and listener reachability independently. A current iQuery relationship does not prove an application request succeeds; it only contributes control-plane evidence.
11. **Why can topology misroute?** Topology commonly observes the recursive resolver's location, which may differ from the end user. Missing or overlapping records can choose an unintended site. Record LDNS source, matched topology entry, selected pool member, and TTL. The trade-off is locality versus accurate user attribution; validate with representative resolvers.
12. **How does DNSSEC affect incidents?** Signatures, keys, chains, and validity intervals must verify, and clock skew can make otherwise correct records unacceptable. Test UDP and TCP responses, flags, signatures, and resolver validation. Never disable validation as a first fix. A DNSSEC failure can look like missing service even when the address and LTM pool are healthy.
13. **What does TTL mean operationally?** It bounds intended cache freshness but does not instantly revoke existing answers. Lower TTL increases query load and still cannot shorten a value already cached. Plan failover, observe resolver behavior, and keep an emergency correction path. Evidence includes authoritative answer, recursive answer, age, and timestamps.
14. **How do you debug a listener?** Confirm destination address, UDP/TCP 53, VLAN, route domain, query name and type, and response flags. A valid answer from another listener is irrelevant. Capture safely and compare authoritative behavior with LDNS results. Listener policy, firewall, and DNSSEC are separate hypotheses.

### TLS and mTLS

15. **Where should TLS terminate?** It may terminate at BIG-IP, a CDN, a proxy, or the application, with optional re-encryption upstream. Document certificate ownership, SNI, ALPN, trust store, and client identity at every hop. Termination simplifies backend handling but changes source and confidentiality boundaries. Verify with handshake evidence rather than assuming the VIP certificate describes the origin.
16. **How do you diagnose mTLS?** Record client and server clocks, SNI, certificate chain, key usage, trust store, validity, and negotiated protocol. Distinguish missing certificate, untrusted issuer, expired certificate, and authorization rejection. Rotate trust in overlap, test a canary, and preserve rollback. Never request or print private keys.
17. **What is SNI?** SNI tells a TLS endpoint which hostname the client intends, allowing certificate and policy selection before HTTP. A valid certificate for another name still fails hostname validation. Test each hostname and termination hop, and check profile association. SNI does not authenticate the client; mTLS certificates and authorization do that.
18. **How does certificate rotation stay safe?** Stage new intermediates and trust anchors, verify chain and hostname, overlap validity, canary clients, and monitor handshake errors before removing old material. The trade-off is temporary trust breadth versus avoiding an outage. Record version and expiry metadata, never credentials or private key contents.

### HA and upgrades

19. **What should HA verification include?** Check peer health, traffic-group ownership, state synchronization, configuration version, connection persistence expectations, and failover logs. Test a planned lab failover and verify new and existing flows separately. A green peer status does not guarantee every runtime state is replicated.
20. **How do you plan an upgrade?** Read release notes, compatibility matrices, license and config requirements, backup and restore evidence, traffic drain, health criteria, and rollback duration. Use a staged device or site, observe error budgets, and retain a tested previous image. Do not claim zero risk from a successful lab rehearsal.
21. **What can fail during failover?** Routes, ARP, SNAT state, persistence, certificates, monitor sources, or upstream adjacency can differ. Capture pre/post tuples and effective ownership. A failover may preserve configuration while losing active state; application reconnect and idempotency are part of the plan.
22. **Why are rollback criteria important?** They turn a subjective incident into a bounded decision using error rate, latency, member health, and handshake evidence. Define owner and time window before change. Rollback itself needs verification because reversing a command does not necessarily restore old runtime state.

### SDK, REST, AS3, DO, TS

23. **How should REST tokens be handled?** Use scoped, short-lived tokens from approved secret injection, validate expiry, redact logs, and avoid command-line exposure. Token success proves authorization only, not desired effect. RBAC partitions and object ownership must be checked before writes.
24. **Why does pagination matter?** A list response may contain only one page. Following cursors or offsets and normalizing ordering prevents incomplete diffs that delete valid members or miss drift. Record object count and API version. Test an empty, full, and multi-page fixture.
25. **How do async tasks change automation?** Submission and completion are separate. Poll with backoff and a deadline, parse terminal failure, then GET effective state. A timeout is ambiguous; read before retrying. This costs implementation complexity but prevents duplicate or partially applied changes.
26. **When use transactions?** Transactions can group dependent updates where the platform supports atomic validation and commit. They are not universal rollback guarantees. Verify task and commit semantics, preserve prior desired state, and test partial failure. A small independent change may be safer than a broad transaction.
27. **What are AS3 and DO?** Declarative tools express desired application or device state through versioned schemas. They improve repeatability but can generate many dependent objects. Pin schema and platform versions, validate ownership, inspect rendered effects, and keep rollback declarations. Current capability is release-specific; consult official F5 docs.
28. **What are TS and FAST used for?** Telemetry Streaming (TS) exports structured observability data; FAST helps template application services in supported workflows. Both require schema, destination, RBAC, and version review. A successful declaration is not proof that telemetry arrives or a generated service is correct; verify effective state and emitted records.

### Observability and scenarios

29. **Which metrics matter for LTM?** Track requests, connections, resets, latency, pool member state, monitor results, SNAT allocation, and TLS errors by virtual server and member. Aggregate values hide hotspots. Correlate with DNS answer, route, and application status.
30. **How do you investigate intermittent timeout?** Partition by client, VIP, protocol, member, time, and connection age. Compare SYN, TLS, request, upstream, and response timestamps. Competing causes include SNAT pressure, one bad member, MTU, policy, and queue saturation. Change nothing until evidence narrows scope.
31. **What makes a good packet capture?** It has authorized interface, exact tuple, synchronized timestamp, direction, and enough packets to show handshake and failure. Capture metadata must be redacted and retained appropriately. A capture from the wrong VLAN or post-NAT side can be technically accurate but diagnostically irrelevant.
32. **How do you explain DNS success but HTTP failure?** DNS only maps a name to an address. TCP, TLS, policy, pool selection, routing, SNAT, and application authorization remain separate stages. Query answer and TTL, then trace the selected VIP and server tuple. This layered explanation avoids changing DNS to fix a backend fault.
33. **What is a safe F5 change?** Define intended object, owner, diff, dependency impact, validation, rollback, and observation window. Prefer dry-run or read-only comparison, canary, and bounded concurrency. Trade-off: slower process versus reduced blast radius and auditability.
34. **How should an engineer handle unknown defaults?** Label the behavior as version-dependent, inspect effective configuration, consult primary F5 documentation, and test a fixture. Do not infer a universal rule from another device or release. This is especially important for profiles, CMP, monitors, API schemas, and declarative tools.

## Debugging exercises

1. **VIP timeout:** SYN reaches VIP but no member SYN. Clues: listener up, pool has no eligible members. Reasoning: inspect monitor and selection state. Solution: correct the probe or member eligibility after review.
2. **SNAT failure:** New clients timeout while existing sessions work. Clues: allocation errors and high translated-port use. Reasoning: distinguish capacity from route. Solution: bounded capacity remediation and connection test.
3. **DNS stale answer:** One resolver returns an old site. Clues: authoritative answer changed, recursive TTL remains. Reasoning: cache behavior, not iQuery first. Solution: wait TTL or use approved emergency cache correction.
4. **mTLS alert:** TCP succeeds, handshake fails only for one client. Clues: missing issuer in trust store. Reasoning: inspect chain and profile. Solution: overlap trust update and verify canary.
5. **Uneven pool:** One member is hot. Clues: persistence keys concentrated, monitors green. Reasoning: selection policy before capacity. Solution: review persistence scope and drain safely.
6. **Async API ambiguity:** POST times out but object appears. Clues: subsequent GET shows desired state. Reasoning: do not retry blindly. Solution: record request ID and treat GET as verification.
7. **Upgrade failover:** New active device has healthy config but resets sessions. Clues: state sync incomplete. Reasoning: separate config from runtime state. Solution: planned drain, state verification, and reconnect test.
8. **Telemetry gap:** TS declaration accepted but dashboard is empty. Clues: destination refusal and missing emitted records. Reasoning: acceptance is not delivery. Solution: verify destination, credentials, schema, and transport metrics.

## Follow-up prompts

- What evidence would falsify your first hypothesis? Answer with a packet, state, or log observation rather than another configuration guess.
- What is the smallest reversible test? Answer with scope, owner, expected result, expiry, and rollback.
- Which fact is version-dependent? Answer by naming the effective configuration or official release documentation you would consult.

Use these follow-ups to turn a memorized answer into an interview discussion:

1. **What would you check first?** Name the observation point, timestamp, and
   read-only command or API resource; do not start with a configuration change.
2. **What would falsify your hypothesis?** State a packet, counter, log, or
   state observation that would move the fault to another layer.
3. **What changes on the server-side leg?** Give the translated address, port,
   route domain, TLS state, and profile boundary rather than saying “the F5
   forwards it.”
4. **What is the rollback?** Identify the exact prior object reference or
   declaration, the owner, the observation window, and the post-rollback probe.
5. **How would you prove capacity?** Separate requests, connections, TLS
   handshakes, SNAT ports, queue depth, and member latency; averages alone are
   insufficient.
6. **What if the API timed out?** Classify the write as unknown, query by
   stable partition-qualified identity, and avoid a blind duplicate request.
7. **How does HA change the answer?** Separate configuration sync, traffic-
   group ownership, connection/state mirroring, ARP/ND convergence, and client
   reconnect behavior.
8. **What does DNS actually prove?** Only the answer and TTL from that resolver;
   it does not prove LTM reachability, TLS validity, or application readiness.
9. **What is version-dependent?** Name the profile, API field, declaration
   schema, or TMOS behavior and cite the release documentation you would check.
10. **What is the smallest safe experiment?** Limit source, VIP, member, or
    resolver scope; define an expected result, expiry, owner, and stop signal.

## Official references

- [F5 BIG-IP documentation portal](https://clouddocs.f5.com/)
- [F5 Application Services 3 Extension](https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/)
- [F5 Declarative Onboarding](https://clouddocs.f5.com/products/extensions/f5-declarative-onboarding/latest/)
- [F5 Telemetry Streaming](https://clouddocs.f5.com/products/extensions/f5-telemetry-streaming/latest/)
- [F5 SDK for Python](https://github.com/F5Networks/f5-common-python)
