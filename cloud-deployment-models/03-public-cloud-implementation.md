# 3. Public Cloud Setups: AWS and GCP

## A. AWS implementation pattern

Create a VPC with private subnets across availability zones, route tables,
security groups, flow logs, and a controlled ingress/egress path. Use an ALB or
NLB when managed load balancing fits the service. Use a Transit Gateway or
Site-to-Site VPN for private connectivity. Terraform owns the cloud resource
graph, IAM boundary, and outputs consumed by an ADC, NSO service, or on-prem
router.

```hcl
variable "aws_region" { type = string }
variable "workload_cidr" { type = string }

provider "aws" { region = var.aws_region }

resource "aws_vpc" "training" {
  cidr_block           = var.workload_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "training-public-cloud" }
}

# Illustrative shape: add subnets, route tables, SGs, logs, and a
# load-balancer/backend contract using the selected provider version.
output "vpc_id" { value = aws_vpc.training.id }
```

Verify VPC route tables, security groups, load-balancer target health, Cloud
Watch metrics, and VPC Flow Logs. A healthy target does not prove that DNS,
TLS, return routing, or an upstream ADC is correct.

## B. GCP implementation pattern

Create a VPC network, regional subnets, firewall rules, Cloud Router/HA VPN or
Interconnect, and a managed load balancer appropriate to the traffic. GCP
firewall rules are network-level constructs; IAM and service accounts are a
separate control plane. Terraform owns the project-scoped graph and exposes
stable attachment outputs to NSO or a border-router workflow.

```hcl
variable "gcp_project" { type = string }
variable "gcp_region" { type = string }

provider "google" { project = var.gcp_project region = var.gcp_region }

resource "google_compute_network" "training" {
  name                    = "training-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "workload" {
  name          = "training-workload"
  network       = google_compute_network.training.id
  region        = var.gcp_region
  ip_cidr_range = "10.60.0.0/24"
}
```

Verify subnet routes, firewall logging, backend health, Cloud Router BGP
advertisements, Cloud Logging, and VPC Flow Logs. Do not map AWS security
groups, route propagation, or load-balancer health semantics one-to-one onto
GCP.

## C. Public-cloud challenges

Quotas and regional availability constrain design; managed services hide some
failure modes; API throttling affects Terraform; egress and inter-region costs
can dominate; IAM mistakes can be more damaging than a route mistake; and
provider abstractions may not expose every packet-path detail. Design for
provider API failure, partial apply, eventual consistency, and support limits.

## D. Networking evidence by cloud

| Layer | AWS evidence | GCP evidence |
| --- | --- | --- |
| Addressing | VPC/subnet and ENI addresses | VPC/subnet and NIC addresses |
| Routing | Route tables, TGW/VPN propagation | Dynamic routes, Cloud Router advertisements |
| Policy | Security groups, NACLs, LB policy | VPC firewall rules, LB policy |
| Hybrid | VPN/BGP or Direct Connect | HA VPN/BGP or Interconnect |
| Traffic | VPC Flow Logs and LB metrics | VPC Flow Logs and Cloud Logging |
| Limits | quotas, targets, TGW, NAT ports | quotas, routes, VPN, Cloud NAT |

For an interview, name the exact hop and expected observation. “The cloud
network is configured” is not evidence that a packet entered the intended VRF,
was accepted by policy, reached the node, and returned through an authorized
path.

## E. Exercise: AWS/GCP equivalence review

Implement the same private application boundary in AWS and GCP. Produce a
mapping table for network, subnet, route, firewall, identity, load balancer,
logging, VPN, and DNS. Mark every row as equivalent, analogous, or not
equivalent, and explain the operational consequence.

**Answer standard:** do not merely rename resources. Explain route propagation,
firewall direction and priority, health-check source, BGP ownership, logging,
and failure behavior. The goal is transferable reasoning, not memorizing APIs.
