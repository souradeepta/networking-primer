# Cloud Deployment Models Track

## A. Purpose and scope

This is the Networking Primer's deployment-model track. It explains private
cloud, public cloud, hybrid cloud, and on-premises infrastructure through the
network path: DNS, interfaces, VLAN/VRF, underlay/overlay routing, BGP, VPN and
Interconnect, firewalls, NAT, ADCs, nodes, observability, and infrastructure as
code. It is designed for SDE2 and Staff interview preparation, not as a
production runbook.

## B. Ordered path

1. [Models and decision framework](01-models-and-architecture.md)
2. [Private cloud and on-premises](02-private-cloud-and-on-premises.md)
3. [Public cloud implementation](03-public-cloud-implementation.md)
4. [Hybrid cloud and connectivity](04-hybrid-cloud-connectivity.md)
5. [Case studies, exercises, and Q&A](05-case-studies-exercises-and-qa.md)

## C. What to produce while studying

For each design, draw the control-plane and data-plane paths from client DNS to
node and back, identify every routing and policy boundary, write the prefix,
MTU, NAT, and security contracts, quantify capacity/cost/RTO/RPO, describe
observability, and state a rollback or forward-repair plan. Compare AWS and GCP
explicitly; similarly named services are not interchangeable.

## D. Related tracks

- [Cloud networking interview track](../cloud-networking-interview/00-README.md)
- [Integrated platform labs](../platform-integration-labs/00-README.md)
- [Terraform and network automation](../terraform-interview/00-README.md)
- [Repository map](../README.md)
