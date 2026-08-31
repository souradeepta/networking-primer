# Cloud Networking Track References

## A. Evidence-label policy

- **Fact:** a claim directly supported by the linked canonical documentation.
- **Vendor terminology:** a provider's product or control-plane name; do not assume its semantics match another provider's name.
- **Inference:** a reasoned engineering conclusion derived from the stated assumptions. Mark what would falsify it.

## B. Canonical AWS references

- [Amazon VPC route tables](https://docs.aws.amazon.com/vpc/latest/userguide/subnet-route-tables.html)
- [Security groups and network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/compare-security-groups-and-network-acls.html)
- [AWS PrivateLink concepts](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)
- [Amazon EKS IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html)
- [AWS Service Quotas](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)

## C. Canonical Google Cloud references

- [Google Cloud VPC overview](https://cloud.google.com/vpc/docs/vpc)
- [Google Cloud routes](https://cloud.google.com/vpc/docs/routes)
- [Private Service Connect](https://cloud.google.com/vpc/docs/private-service-connect)
- [Workload Identity Federation for GKE](https://cloud.google.com/kubernetes-engine/docs/concepts/workload-identity)
- [Google Cloud quotas](https://cloud.google.com/docs/quotas)

## D. Repository cross-references

- [Book fact/inference ledger](../book/FACT-INFERENCE-LEDGER.md)
- [Cloud networking primitives](../book/topics/37-cloud-networking-primitives.md)
- [Network observability and SLOs](../book/topics/11-network-observability-slos.md)
- [Interview rubric](../docs/interview-rubric.md)

## E. Verification boundary

These links are study references, not deployment authorization. Before using a claim in a real design, verify the selected service, region, account/project policy, release, quota page, and pricing page. Record the retrieval date and the exact assumption in the design artifact.
