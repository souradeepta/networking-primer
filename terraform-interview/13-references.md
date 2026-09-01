# Terraform Track References and Evidence Ledger

## A. Evidence labels

- **Fact:** directly supported by the cited Terraform, provider, or F5 documentation within its stated version boundary.
- **Vendor terminology:** a provider, product, resource, or API name; similar names do not imply equivalent lifecycle behavior.
- **Inference:** an engineering conclusion from stated assumptions; record the falsifier and owner.

## B. Terraform references

- [Terraform language documentation](https://developer.hashicorp.com/terraform/language)
- [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)
- [Terraform state](https://developer.hashicorp.com/terraform/language/state)
- [Terraform backends](https://developer.hashicorp.com/terraform/language/backend)
- [Terraform import](https://developer.hashicorp.com/terraform/language/import)
- [Terraform moved blocks](https://developer.hashicorp.com/terraform/language/block/moved)
- [Terraform provider requirements](https://developer.hashicorp.com/terraform/language/providers/requirements)

## C. Provider references

- [AWS Terraform provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Google Terraform provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [F5 BIG-IP Terraform provider](https://registry.terraform.io/providers/F5Networks/bigip/latest/docs)
- [F5 `bigip_as3` resource](https://registry.terraform.io/providers/F5Networks/bigip/latest/docs/resources/bigip_as3)
- [Cisco NSO services and service mapping](https://nso-docs.cisco.com/guides/development/core-concepts/services)
- [Cisco NSO implementing services](https://developer.cisco.com/docs/nso-guides-6.3/implementing-services/)
- [Cisco NDFC VXLAN EVPN fabric guidance](https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/managing-and-monitoring-vxlan-evpn-fabrics-using-cisco-ndfc.html)
- [Cisco NDFC BGP fabric guidance](https://www.cisco.com/c/en/us/td/docs/dcn/ndfc/1222/articles/ndfc-bgp-fabric/bgp-fabric.html)
- [AWS VPC CLI examples](https://docs.aws.amazon.com/vpc/latest/userguide/create-a-vpc-with-private-subnets-and-nat-gateways-using-aws-cli.html)
- [Google Cloud CLI configuration](https://cloud.google.com/sdk/gcloud/reference/config)

## D. Evidence boundaries

| Claim area | Source boundary | Verify before use |
|---|---|---|
| Terraform language, state, import, and lifecycle | HashiCorp Terraform documentation | Terraform CLI version and backend implementation |
| AWS networking resources | AWS provider and AWS service documentation | Provider lock entry, account, Region, quotas, and pricing |
| GCP networking resources | Google provider and Google Cloud documentation | Provider lock entry, project, Region, API enablement, quotas, and pricing |
| F5 provider and AS3 behavior | F5 provider, AS3, and BIG-IP/TMOS documentation | Provider release, TMOS/AS3 version, partition, RBAC, and device capability |
| A10 ADC behavior | A10 product/API/provider documentation | ADC release, partition/tenant, API schema, HA mode, and provider support |
| Cisco device and fabric behavior | Cisco IOS-XE/NX-OS/NDFC documentation | Software release, platform, feature license, topology, NDFC/NX-API behavior |
| Cisco NSO service behavior | Cisco NSO/YANG/NED documentation | NSO release, package revision, NED, device model, CDB state, and transaction result |
| Rollback, ownership, and platform policy | Engineering inference in these modules | Service owner, blast radius, tested recovery, and approval authority |

## E. Repository cross-references

- [Cloud networking interview track](../cloud-networking-interview/00-README.md)
- [F5 API and automation toolchain](../book/topics/33-f5-api-and-automation-toolchain.md)
- [Infrastructure automation chapter](../book/13-automation-f5-sdk-rest-ssh.md)
- [Interview rubric](../docs/interview-rubric.md)
- [Repository disclosures](../DISCLOSURES.md)
