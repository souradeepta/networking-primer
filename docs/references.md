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

## Fact / inference ledger

| Statement | Classification | Basis |
| --- | --- | --- |
| TCP is specified by RFC 9293. | Protocol fact | RFC 9293 |
| DNS has authoritative data and resolver caching. | Protocol fact | RFC 1035 |
| DHCP delivers configuration parameters and allocates addresses. | Protocol fact | RFC 2131 |
| RFC 1918 reserves `10/8`, `172.16/12`, and `192.168/16` for private internets. | Protocol fact | RFC 1918 |
| A Wide IP maps an FQDN to pools of virtual servers. | Vendor terminology/fact | F5 Wide IP guide |
| GTM/BIG-IP DNS does not provide instantaneous universal failover. | Engineering inference | DNS caching and existing connection behavior; test in the target environment |
| Deep health checks are always better than TCP checks. | Rejected oversimplification | Probe depth trades detection fidelity against dependencies, load, and flapping |
| The included F5 SDK example is production-ready for every BIG-IP release. | Not claimed | Validate installed BIG-IP/SDK versions and team interface standards |
