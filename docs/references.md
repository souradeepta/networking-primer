# References and fact/inference ledger

## Primary references

- [RFC 9293: Transmission Control Protocol](https://datatracker.ietf.org/doc/rfc9293/)
  is the current Internet Standard specification for TCP.
- [RFC 1035: Domain Names - Implementation and Specification](https://datatracker.ietf.org/doc/html/rfc1035)
  specifies core DNS message/record behavior; later RFCs update parts of it.
- [RFC 2131: Dynamic Host Configuration Protocol](https://www.rfc-editor.org/info/rfc2131/)
  specifies DHCPv4 host-configuration and address-allocation behavior.
- [RFC 1918: Address Allocation for Private Internets](https://www.rfc-editor.org/info/rfc1918/)
  defines the familiar IPv4 private address ranges.
- [RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3](https://datatracker.ietf.org/doc/html/rfc8446)
  specifies TLS 1.3, including handshake authentication and protected records.
- [RFC 5280: Internet X.509 Public Key Infrastructure Certificate and CRL Profile](https://datatracker.ietf.org/doc/html/rfc5280)
  defines the X.509 certificate and certification-path validation profile.
- [RFC 4251: The Secure Shell (SSH) Protocol Architecture](https://datatracker.ietf.org/doc/html/rfc4251)
  specifies SSH protocol architecture and server-host authentication concepts.
- [F5 LTM virtual server TMSH reference](https://clouddocs.f5.com/cli/tmsh-reference/v14/modules/ltm/ltm_virtual.html)
  and [pool reference](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html)
  describe LTM configuration objects and options.
- [F5 Wide IP configuration training](https://clouddocs.f5.com/training/community/big-iq-cloud-edition/html/class10/module2/module2.html)
  describes a Wide IP mapping an FQDN to pools of virtual servers and using
  configured load-balancing methods.
- [F5 iControl REST API reference](https://clouddocs.f5.com/api/icontrol-rest/APIRef_tm_gtm.html)
  lists BIG-IP DNS/GTM API resources.
- [F5 Python SDK source and documentation](https://github.com/F5Networks/f5-common-python)
  is the upstream project for the SDK used in the read-only example.
- [F5 BIG-IP AS3 documentation](https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/)
  documents the current declarative application-service model and release
  selector; schema and feature support remain version-dependent.
- [F5 Declarative Onboarding documentation](https://clouddocs.f5.com/products/extensions/f5-declarative-onboarding/latest/)
  covers declarative base-device onboarding and compatibility considerations.
- [F5 Telemetry Streaming documentation](https://clouddocs.f5.com/products/extensions/f5-telemetry-streaming/latest/)
  describes exporting structured BIG-IP telemetry; it is not a configuration
  transaction or health guarantee.
- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
  is the current incident-response recommendations publication and supersedes
  Rev. 2.

## Fact / inference ledger

| Statement | Classification | Basis |
| --- | --- | --- |
| TCP is specified by RFC 9293. | Protocol fact | RFC 9293 |
| DNS has authoritative data and resolver caching. | Protocol fact | RFC 1035 |
| DHCP delivers configuration parameters and allocates addresses. | Protocol fact | RFC 2131 |
| RFC 1918 reserves `10/8`, `172.16/12`, and `192.168/16` for private internets. | Protocol fact | RFC 1918 |
| TLS provides a secure channel with server authentication and optional client authentication. | Protocol fact | RFC 8446 |
| X.509 certification paths and certificate extensions are part of certificate validation. | Protocol fact | RFC 5280 |
| SSH includes server-host authentication, which is the basis for host-key verification. | Protocol fact | RFC 4251 |
| A Wide IP maps an FQDN to pools of virtual servers. | Vendor terminology/fact | F5 Wide IP guide |
| GTM/BIG-IP DNS does not provide instantaneous universal failover. | Engineering inference | DNS caching and existing connection behavior; test in the target environment |
| Deep health checks are always better than TCP checks. | Rejected oversimplification | Probe depth trades detection fidelity against dependencies, load, and flapping |
| The included F5 SDK example is production-ready for every BIG-IP release. | Not claimed | Validate installed BIG-IP/SDK versions and team interface standards |
## Cloud interview track evidence index

## CCNA-to-Staff book expansion

The [CCNA-to-Staff networking expansion](../book/ccna-networking/00-README.md)
uses protocol and vendor evidence for switching, routing, BGP, WAN, security,
wireless, QoS, multicast, EVPN/VXLAN, cloud, and automation. **Fact:** protocol
behavior should be checked against the relevant RFC. **Vendor terminology:**
IOS-XE, NX-OS, A10, F5, NSO, NDFC, AWS, and GCP names and command/API behavior
are release-specific. **Observed lab result:** only applies to the stated
simulator or appliance. **Engineering inference:** design, ownership, capacity,
and rollback guidance must be validated against the target estate.

| Area | Primary evidence | Verification boundary |
| --- | --- | --- |
| Routing and addressing | [RFC 791](https://www.rfc-editor.org/rfc/rfc791), [RFC 8200](https://www.rfc-editor.org/rfc/rfc8200), [RFC 4271](https://www.rfc-editor.org/rfc/rfc4271) | Check the correct VRF, RIB/FIB, route policy, and return path. |
| Switching and fabric | [IEEE 802.1Q](https://standards.ieee.org/ieee/802.1Q/), [RFC 7432](https://www.rfc-editor.org/rfc/rfc7432), [RFC 7348](https://www.rfc-editor.org/rfc/rfc7348) | Check VLAN/VNI, STP/ECMP, VTEP, EVPN routes, MTU, and endpoint state. |
| Services and security | [RFC 2131](https://www.rfc-editor.org/rfc/rfc2131), [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035), [RFC 8907](https://www.rfc-editor.org/rfc/rfc8907) | Check DNS/DHCP/time, ACL direction, AAA, and device/cloud policy logs. |
| Automation | [RFC 7950](https://www.rfc-editor.org/rfc/rfc7950), [RFC 6241](https://www.rfc-editor.org/rfc/rfc6241), [RFC 8040](https://www.rfc-editor.org/rfc/rfc8040) | Check schema/version, ownership, idempotency, state, drift, and read-back. |

The standalone [Cloud Networking Interview Track](../cloud-networking-interview/00-README.md)
contains its own ordered modules and local [fact/terminology/inference ledger](../cloud-networking-interview/17-references.md).
Use the AWS and Google Cloud links there for provider-specific claims; verify
service, region, account/project policy, release, quota, and pricing boundaries
before applying a claim to a real design.

The Terraform track also covers [A10 ADCs, Cisco networking, spine-leaf
fabrics, and Cisco NSO](../terraform-interview/00-README.md). Those modules
label product behavior as vendor-specific and require verification against
the selected A10, IOS-XE/NX-OS, NDFC, or NSO release and licensed capabilities.

The standalone [Terraform Interview Track](../terraform-interview/00-README.md)
contains Terraform-specific modules and a local [evidence ledger](../terraform-interview/13-references.md).
Use it for provider version, state, import, F5 AS3, and plan/apply claims, and
verify the selected Terraform CLI, provider lock entry, account/project, BIG-IP
release, permissions, quotas, and pricing before use.
