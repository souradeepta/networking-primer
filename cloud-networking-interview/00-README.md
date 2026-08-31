# Cloud Networking Interview Track

## A. Purpose and audience

This standalone track prepares engineers for SDE2 and Staff-level cloud-networking interviews using portable mechanisms first and AWS/GCP terminology second. It is a learning curriculum, not an operational runbook. Provider names are comparison points, not claims of equivalent behavior.

## B. Recommended sequence

1. [Cloud network foundations](01-cloud-network-foundations.md)
2. [Virtual-network boundaries and design](02-virtual-network-boundaries-and-design.md)
3. [Subnet and IP-address planning](03-subnet-and-ip-address-planning.md)
4. [Routes, gateways, and hybrid connectivity](04-routes-gateways-and-hybrid-connectivity.md)
5. [Internet ingress, NAT, and egress](05-internet-ingress-nat-and-egress.md)
6. [Firewalls, security groups, and network ACLs](06-firewalls-security-groups-and-network-acls.md)
7. [Private connectivity and service publishing](07-private-connectivity-and-service-publishing.md)
8. [DNS and service discovery](08-dns-and-service-discovery.md)
9. [Load balancing and traffic entry](09-load-balancing-and-traffic-entry.md)
10. [IAM and workload identity](10-iam-and-workload-identity.md)
11. [Containers, Kubernetes, and NetworkPolicy](11-containers-kubernetes-and-network-policy.md)
12. [Observability, troubleshooting, and SLOs](12-observability-troubleshooting-and-slos.md)
13. [Quotas, capacity, and network cost](13-quotas-capacity-and-network-cost.md)
14. [Multi-region disaster recovery and failover](14-multi-region-disaster-recovery-and-failover.md)
15. [Cloud-network migration and modernization](15-cloud-network-migration-and-modernization.md)
16. [Interview synthesis and mock loops](16-cloud-interview-synthesis-and-mock-loops.md)

## C. How to study

For each module, draw the diagrams from memory, answer the questions aloud, complete the whiteboard exercise, and then use the evidence-led exercise to state what would falsify your leading hypothesis. SDE2 candidates should emphasize mechanism, packet/request paths, and safe diagnosis. Staff candidates should add ownership, failure domains, cost, migration, capacity, and decision records.

## D. Evidence and vendor boundaries

Use [17-references.md](17-references.md) for the local fact, vendor-terminology, and inference ledger. Provider behavior changes by service, region, account/project configuration, and release; verify current claims against the linked official documentation before treating them as design commitments.

## E. Completion gates

- Explain one request path across routing, policy, identity, DNS, and service entry.
- Compare AWS and GCP without mapping similarly named products one-to-one.
- Quantify at least one capacity, address, port, RTO/RPO, or cost assumption.
- Name evidence, a falsifier, rollback point, and owner for a proposed change.
- Complete the three mock loops in the final module and score yourself against the repository's [interview rubric](../docs/interview-rubric.md).
