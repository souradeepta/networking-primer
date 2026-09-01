# 2. Labs, Exercises, and Answer Key

## A. Exercise 1: green monitor, broken user path

**Starting state:** A10/F5 reports both nodes healthy, but clients see
intermittent 502s. The VIP terminates TLS and SNAT is enabled.

**Answer:** verify client SNI/certificate, ADC selected-member and reset
counters, monitor source/Host/URI/status, SNAT allocation and port use, backend
listener/logs, and the return route. Green proves only that the configured probe
passed. If failures cluster on one member, drain it after preserving evidence.
If new-flow load triggers errors, test SNAT and connection capacity. A bounded
probe using the same SNI, headers, source behavior, and member is a falsifier.

**SDE2 follow-up:** explain why disabling SNAT can create asymmetric routing.
**Staff follow-up:** define monitor contracts, headroom, SLO gates, and the
owner of client-IP preservation.

## B. Exercise 2: BGP established, no application traffic

**Starting state:** IOS-XE and a cloud router show BGP Established. An AWS or
GCP node cannot reach an on-premises VIP.

**Answer:** inspect accepted/advertised prefixes, route policy, VRF RIB/FIB,
cloud route table, security group/firewall, ADC return route, and node listener.
Compare AWS or GCP flow logs with router and ADC counters. BGP state proves
adjacency, not correct prefix acceptance or installation. The smallest repair
may be missing export policy or propagation; a full-service rollback can hide
the defect.

## C. Exercise 3: EVPN duplicate MAC

**Starting state:** a node flaps between two leaves and connections drop.

**Answer:** correlate MAC moves, EVPN sequence changes, access-port flaps,
vPC/MLAG consistency, host teaming, and endpoint identity. Do not clear all
forwarding state first. Contain one looping port under approved authority,
preserve counters, restore intended attachment, and verify ARP/ND plus an
application probe. Host mobility, a loop, and address reuse are distinct causes.

## D. Exercise 4: NSO timeout after commit

**Starting state:** Terraform times out after creating an NSO service while the
device was briefly unreachable.

**Answer:** query NSO by stable service key and correlation ID. Classify
absent/pending/committed/failed, read CDB and transaction state, inspect device
diff and operational state, and only then refresh or retry. Idempotency prevents
duplicates. Roll back only when causality and safe deletion are established;
otherwise repair the session and reconcile.

## E. Exercise 5: fabric MTU failure

**Starting state:** small pings work, but large responses fail across VXLAN to
AWS or GCP. Calculate payload plus outer Ethernet/IP/UDP/VXLAN overhead and
check node, leaf, spine, border, VPN/Interconnect, and cloud MTUs. Inspect
PMTUD, fragmentation, and drops. A TCP handshake does not disprove MTU trouble.
Change the narrowest boundary and test both directions.

## F. Exercise 6: tool and ownership decision

Choose direct Terraform, F5 AS3, an A10 API/provider, Ansible, NDFC, or NSO for
one switch VLAN, a four-leaf fabric, a reusable L3VPN service, and an ADC
declaration.

**Answer:** select the system whose identity, read-back, dependencies, and
ownership match the change. Direct Terraform can fit stable cloud primitives
or narrow device resources; NDFC/NSO fits controller-owned intent; AS3 fits an
F5 declaration boundary; A10 requires ACOS/provider verification. Ansible may
fit sequencing or recovery but does not automatically supply Terraform-style
lifecycle state. Always explain exceptions and migration.
