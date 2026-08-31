# 5. Troubleshooting runbook

Use this as a safe investigation sequence. It intentionally stops before
configuration changes: collect evidence, identify the owning team and change
window, then use the approved operational procedure.

## First five minutes

1. Write down the exact hostname, URL, client network/region, timestamp with
   timezone, request/correlation ID, and user-visible error.
2. Determine blast radius: one client, one resolver, one region, one VIP, or
   all traffic.
3. Preserve evidence: relevant application/proxy/LB logs and safe packet or
   flow metadata. Do not collect secrets or production payloads unnecessarily.
4. Compare with a known-good client/location when policy permits.
5. State a falsifiable hypothesis, such as “the resolver is serving a stale
   DNS answer” rather than “the network is broken.”

## Symptom-to-evidence table

| Symptom | Safe checks | Interpretation and next branch |
| --- | --- | --- |
| Wrong address / `NXDOMAIN` | `dig name A`, `dig name AAAA`, query known resolver | Compare response code, authority, answer, and TTL; then check DNS/WIP ownership |
| TCP timeout | `curl -v --connect-timeout 5`, route/flow evidence | Find where SYN/SYN-ACK disappears; inspect selected VIP and network policy |
| Connection refused | Confirm listener with `ss -lntp` on owned host | Target answered but no compatible listener accepted the port |
| TLS alert/cert error | `openssl s_client -connect host:443 -servername host` | Check SNI, SAN, chain, expiry, clock, TLS version/cipher policy |
| 5xx from VIP | Response headers, request ID, LTM and app logs | Determine whether LTM/proxy/app emitted it; examine pool/monitor state |
| Only one geography fails | DNS answer, GTM target eligibility, regional VIP logs | Compare resolver location/cache and selected data center |
| New VM cannot start | Lease, gateway, DNS resolver, IPAM allocation | Trace DHCP scope/relay/options and duplicate-address evidence |

## LTM: VIP returns failures

```text
Identify the matched virtual server
  -> Is the virtual server available and listening on the intended address:port?
  -> Is the expected pool selected by policy?
  -> Are enough pool members enabled and monitor-healthy?
  -> Does a backend accept the server-side connection and return a response?
  -> Is return routing symmetric or is SNAT required/configured?
  -> Does TLS terminate/re-encrypt/pass through as the application expects?
```

Record both sides of a full proxy boundary. A successful client-side TCP
handshake does not prove a server-side connection exists.

## GTM/BIG-IP DNS: site failover does not appear to work

1. Query the intended FQDN using the affected recursive resolver and save the
   answer and remaining TTL.
2. Check that the query matches the intended Wide IP type/name and policy.
3. Verify target/pool health, enabled state, and the monitor’s actual probe.
4. Confirm the alternate data center has an eligible target and capacity.
5. Account for cache expiry and existing client keep-alive connections before
   declaring failover ineffective.
6. Confirm the application supports traffic in the alternate site, especially
   for write paths and regional data dependencies.

## Escalation packet

Hand off a compact evidence packet: impact/blast radius; UTC time range;
hostname and resolved answer; client source region; selected VIP/site; relevant
request IDs; monitor/pool state; safe logs or flow summary; recent approved
changes; and the hypothesis plus contradictory evidence.
