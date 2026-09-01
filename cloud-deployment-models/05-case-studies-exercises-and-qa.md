# 5. Case Studies, Exercises, and Q&A

## A. Case study: overlapping CIDRs block migration

An on-premises private cloud uses `10.20.0.0/16`; a new AWS VPC uses the same
range. The VPN is up, BGP is Established, but routes are rejected or traffic
lands in the wrong domain.

**Diagnosis:** inventory all prefixes, inspect accepted routes and longest
match behavior, and confirm which system owns translation. Do not “fix” this by
randomly adding static routes. Use renumbering, a translation boundary with
documented limitations, or a staged migration. Test DNS, source identity,
logging, and return traffic. **Staff lesson:** CIDR allocation is a platform
governance problem; reserve address space before teams create networks.

## B. Case study: private ADC to public-cloud node

An F5 or A10 VIP in the private facility sends traffic to GCP nodes. Health
checks pass, but responses time out. The cloud route to the node exists.

**Diagnosis:** compare monitor source and user source, SNAT behavior, GCP
firewall logging, Cloud Router return advertisement, node default route, MTU,
and backend listener. The likely fault is not proven until a bounded probe and
flow logs distinguish ACL, asymmetric routing, and application behavior.

## C. Case study: public-cloud outage with private failover

AWS target health degrades during a regional event. DNS points users to a
private/on-premises VIP, but latency rises and some sessions fail.

**Diagnosis:** verify DNS TTL/cache, private ADC pool capacity, border and
hybrid-link headroom, node saturation, and state/persistence assumptions. Do
not fail back merely because AWS health recovered; require stable error rate,
latency, route convergence, and capacity evidence.

## D. Exercise: write a hybrid change plan

Change a cloud BGP advertisement, add a Cisco border policy, update an NSO
service, and change an ADC pool. Your plan must include dependency order,
canary, evidence, approval owner, stop conditions, rollback, and forward repair.

**Answer:** make the least risky reversible change first, save the prior
configuration/plan, check policy in the correct VRF, verify route acceptance,
then test a single node or pool member before broadening. For a non-reversible
CIDR migration, use a dual-address transition and forward-repair plan.

## E. Networking whiteboard drill: find the first broken hop

Draw `client -> DNS -> ADC -> leaf -> spine -> border -> VPN/Interconnect ->
cloud route -> firewall -> node -> return path`. Mark the evidence available at
each hop and explain what a missing route, denied policy, wrong VRF, MTU black
hole, SNAT exhaustion, and node listener failure would look like. The answer is
incomplete until it includes the reverse path and a falsifier for the leading
hypothesis.

## F. Interview Q&A

### E.1 “When would you choose hybrid cloud?”

Choose it when the workload has a meaningful private dependency—regulated data,
latency-sensitive systems, existing hardware, or migration constraints—while
public cloud provides elasticity, managed services, or geographic reach. Name
the connectivity, identity, data movement, operating cost, and exit plan.

### E.2 “What is the hardest hybrid-cloud problem?”

The hardest problem is usually the boundary contract: overlapping addressing,
split identity, route ownership, asymmetric paths, inconsistent security
semantics, and unclear incident ownership. A Staff answer makes those explicit,
tests them, and assigns measurable SLOs and escalation paths.

### E.3 “How do you debug public versus private failures?”

Use the same layered path—name, connect, route, policy, TLS, listener, service,
return path—but collect different evidence. Private evidence may be switch
counters and device captures; cloud evidence may be route tables, flow logs,
managed-LB health, IAM, and service quotas. Never treat a provider API response
as packet-level proof.

### E.4 “How should Terraform participate?”

Terraform should own stable resource lifecycles and explicit interfaces. It may
own AWS/GCP networks and an NSO service instance, while NSO owns rendered
router/switch configuration and A10/F5 automation owns ADC objects. Avoid
co-ownership, use idempotent reads after timeouts, protect state, and verify
behavior after apply.

### E.5 “Active/active or active/standby?”

Choose based on state, failure detection, capacity, cost, and operational
complexity. Active/active uses capacity efficiently but requires careful DNS,
routing, persistence, and split-brain handling. Active/standby is simpler but
leaves capacity idle and can fail during an untested promotion. Explain the
failure test and measurable recovery objective.

## G. Scoring rubric

Score 0–2 each for mechanism, packet path, ownership, evidence/falsifier,
security, capacity/cost, recovery, and communication. SDE2 readiness requires a
correct layered diagnosis. Staff readiness additionally requires a durable
platform contract, migration strategy, explicit trade-offs, and an operating
model for teams that own different clouds and devices.
