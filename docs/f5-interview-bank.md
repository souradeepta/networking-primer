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

## Second bank: advanced questions

### LTM internals and capacity

35. **How do TMM flow keys influence capacity?** TMM tracks flow state using tuple and profile context, then distributes eligible work through CMP. Evidence includes per-TMM counters, connection tables, and packet captures. More parallelism can improve capacity but shared state or unsupported features can constrain it. Verify the deployed release before attributing imbalance to hashing.
36. **What is the cost of broad connection limits?** A virtual-server or pool limit protects resources but can reject legitimate bursts. Inspect configured limits, current connections, reset counters, and queue behavior. Raising limits may move failure into TMM, SNAT, or the origin, so capacity changes require load evidence and rollback criteria.
37. **How does slow ramp interact with persistence?** Slow ramp controls newly assigned work, while existing persistence can continue directing clients to an eligible member. Evidence requires persistence keys, assignment timestamps, ramp state, and per-member load. The trade-off is warm-up safety versus delayed recovery; exact precedence is version-dependent and must be tested.
38. **How can a monitor create overload?** A short interval or expensive transactional monitor can consume backend workers and produce a misleading healthy result. Compare monitor source, request cost, interval, timeout, and application logs. A deeper probe improves dependency signal but couples health to more systems; use a lightweight readiness contract where possible.
39. **Why do long-lived connections change capacity planning?** Connection count consumes memory, SNAT ports, and tracking state even when request rate is low. Inspect age distribution, idle timers, stream counts, and allocation errors. Lowering timers may recover resources but interrupt valid sessions, so coordinate drain and client reconnect behavior.
40. **What is a pool member versus a node?** A member combines an address and service port for pool selection; a node is a reusable host object. Evidence should identify both because a node can back several ports and monitors. Conflating them can lead to disabling unrelated services or applying the wrong health policy.
41. **How should capacity tests avoid false confidence?** Use representative connection lifetime, payload size, TLS, persistence, and member behavior, then observe TMM, SNAT, queue, and origin metrics. A synthetic benchmark can omit the limiting resource; its trade-off is repeatability versus realism. State what was measured, not a universal throughput claim.
42. **What does a packet capture miss?** A capture on one VLAN sees only one side of NAT or policy and may miss dropped packets elsewhere. Combine client-side and server-side captures, flow logs, TMM counters, and timestamps. More captures increase privacy and storage risk, so scope interfaces and retention deliberately.

### GTM/DNS operations

43. **How do you validate a Wide IP pool?** Read the Wide IP, pool members, virtual-server references, monitor status, and selection method, then query the authoritative listener. Evidence must include query name, type, LDNS source, answer, and TTL. A valid object graph can still return an unusable address if iQuery or listener state is stale.
44. **Why can iQuery appear healthy while DNS is wrong?** iQuery control communication and client listener service are separate paths. Inspect peer freshness, listener packets, VLAN policy, and authoritative response independently. Adding a peer or changing monitors may hide the issue but increases scope; first identify which plane lacks evidence.
45. **How should topology records be tested?** Query from representative recursive resolver locations and record the matched topology entry and answer. LDNS location is only a proxy for user location. More precise geography can improve locality but adds data and maintenance risk; verify fallback behavior for unmatched clients.
46. **What does DNS listener failure look like?** No packet or no response points toward address, VLAN, route, firewall, or service state. A response with wrong policy points toward Wide IP or topology. Capture UDP and TCP where relevant, and compare the tested address with configured listeners; a different listener can produce a valid but irrelevant answer.
47. **How do DNSSEC keys affect operations?** Signing and validation depend on key publication, chain continuity, and clock validity. Evidence includes flags, signatures, key records, resolver errors, and synchronized timestamps. Emergency disabling reduces immediate validation failures but weakens trust; prefer overlap, staged rollover, and tested recovery.
48. **How should TTL be chosen?** TTL balances cache staleness, query load, and failover expectations. Evidence is authoritative TTL plus recursive cache age, not merely configuration. Short values improve planned agility but increase load and cannot shorten an answer already cached; choose based on measured resolver behavior and recovery objectives.

### TLS, certificates, and mTLS

49. **Why can SNI select the wrong certificate?** The endpoint maps the requested hostname to a TLS profile and certificate before HTTP routing. Evidence includes ClientHello SNI, selected profile, certificate names, and ALPN. A default certificate may be valid for another service; changing the certificate without confirming listener and hostname can cause collateral failures.
50. **How do intermediate certificates fail?** A server may omit or misorder an intermediate, leaving some clients unable to build a trusted chain. Compare client chain-building errors, served chain, trust anchors, and validity intervals. Adding intermediates improves compatibility but increases rotation inventory; verify from representative clients rather than one browser.
51. **What is mTLS authorization versus authentication?** Certificate validation authenticates possession of a key chained to a trusted issuer; authorization decides what that identity may do. Evidence includes verified subject or SAN, issuer, policy mapping, and application decision. Broad trust eases migration but expands blast radius; use scoped issuers and explicit mapping.
52. **How does TLS affect LTM health monitors?** A monitor may connect with a different SNI, client certificate, or trust policy than users. Inspect monitor configuration, source, handshake, URI, and expected response. A green TCP probe proves little about TLS; a deep probe improves signal but can overload dependencies.
53. **What is safe certificate rollback?** Preserve the prior certificate and chain, stage the replacement, canary representative SNI and mTLS clients, and define handshake-error thresholds. Rollback restores known-good material and verifies effective profiles; it is not merely copying a file back. Never store private keys in tickets or logs.
54. **Why does clock skew matter?** Not-before and not-after checks use wall time, so a skewed host can reject an otherwise valid certificate. Record client/server time, synchronization health, chain, and alert. Relaxing validation hides the symptom and weakens security; repair time sources or certificate lifecycle instead.

### HA and upgrades

55. **What is configuration versus runtime state?** Configuration includes objects and profiles; runtime state includes connections, persistence, and learned health. Evidence requires config version, sync status, active owner, and flow behavior. Replicating one does not guarantee the other, so failover plans must test both new and existing requests.
56. **How should traffic be drained before upgrade?** Stop new assignments, allow bounded completion, monitor active sessions, and test reconnects. Evidence is declining connection age and member assignment, not an operator command alone. A long grace period preserves sessions but delays recovery; define a deadline and forced-close policy.
57. **What makes a device image rollback credible?** Keep a tested image, compatible configuration backup, license and dependency checks, and a measured restoration path. Evidence comes from a staging rehearsal and post-rollback probes. A backup that restores syntax but not certificates, routes, or state is incomplete; document exclusions explicitly.
58. **How do you detect split brain?** Compare traffic ownership, peer state, configuration versions, ARP or route advertisements, and independent client probes. A peer status screen is insufficient. Immediate manual changes can worsen divergence; isolate ownership through the approved HA procedure and preserve evidence before remediation.
59. **Why stage upgrades by failure domain?** A staged device or site limits simultaneous loss and reveals version interactions. Evidence includes health, latency, TLS, DNS, and application SLOs before and after. Staging slows rollout and can leave mixed versions, so define compatibility boundaries and an abort threshold.
60. **What is a good upgrade communication?** State scope, owner, timing, expected signals, customer impact, rollback trigger, and evidence locations. This enables coordinated DNS TTL, LTM drain, certificate, and application decisions. Caveat: a communication plan does not replace technical verification or authorize changes outside the approved window.

### SDK, API, and toolchain

61. **How do you handle API version drift?** Pin SDK and extension schemas, inspect target version, and run contract fixtures against representative responses. Evidence includes endpoint version, schema validation, and rendered diff. Pinning slows adoption but prevents silent field or default changes; upgrade deliberately with compatibility tests.
62. **Why distinguish REST stats from config?** Configuration describes intended objects, while statistics describe runtime counters and health. Read both and correlate timestamps. Stats can be sampled or nested differently by release; parsing a convenient field without schema checks can produce false green automation.
63. **How should RBAC be tested?** Use a non-production identity that has only intended partition and operation permissions, then test allowed reads and denied writes. Evidence is audited response and effective scope. Excess privilege simplifies scripts but increases blast radius; separate read, diff, and apply identities where practical.
64. **When is AS3 preferable to imperative REST?** AS3 can express an application declaration and dependencies consistently, reducing order-sensitive scripts. It can also create broad changes and is schema/version dependent. Validate declaration, ownership, rendered objects, task result, and behavior; use imperative calls only for supported exceptions with equivalent review.
65. **How should TS configuration be verified?** Confirm declaration acceptance, effective telemetry endpoints, transport authentication, emitted records, and destination health. A successful POST proves only acceptance. More validation costs test setup but catches schema, RBAC, and network failures before an incident dashboard is trusted.
66. **What should mocks include?** Pagination, token expiry, rate limits, malformed fields, async transitions, permission denial, partial success, and ambiguous timeouts. Evidence is a regression assertion tied to an invariant. An overly friendly mock produces false confidence; fixtures should reflect documented API failure semantics.

### Debugging and design scenarios

67. **Design a multi-site LTM/GTM service.** Use DNS for site choice and LTM for connection and pool selection, with explicit monitors, TTL, drain, and rollback. Evidence includes resolver behavior, site health, VIP tuples, and member state. DNS is not per-request balancing, and a site design must tolerate stale caches and asymmetric failures.
68. **A change passes API validation but users fail. What next?** Preserve request ID and declaration, read effective objects, query DNS, trace client and server tuples, inspect TLS and pool state, and compare a canary. Validation proves schema or acceptance, not behavior. Roll back only after identifying scope and verifying recovery.

## Debugging exercises 9-16

9. **Priority drain hotspot:** One member remains hot after drain. Clues: persistence keys and long sessions. Expected reasoning: inspect persistence and connection age. Solution: bounded drain and planned expiry.
10. **GTM wrong region:** Users resolve a distant site. Clues: LDNS topology match differs from user location. Reasoning: compare resolver sources. Solution: correct topology or fallback and measure.
11. **DNSSEC outage:** Authoritative answers exist but validating resolvers return failure. Clues: signature or time error. Reasoning: inspect chain and clock. Solution: staged key or time correction.
12. **mTLS one-client failure:** One client receives handshake alert. Clues: issuer absent from trust store. Reasoning: compare chain. Solution: overlap trust and canary.
13. **HA stale state:** New active device accepts new flows but old sessions reset. Clues: config synced, runtime state absent. Reasoning: separate state types. Solution: drain and reconnect plan.
14. **API duplicate:** Retry after timeout creates duplicate object. Clues: first task completed. Reasoning: GET before retry. Solution: stable identity and idempotency.
15. **Telemetry silent:** TS declaration accepted but no events arrive. Clues: destination rejection. Reasoning: acceptance is not delivery. Solution: verify endpoint, schema, auth, and transport.
16. **Mixed-version upgrade:** One site shows new profile behavior. Clues: release mismatch and different defaults. Reasoning: compare effective config and schema. Solution: compatibility gate or rollback.
