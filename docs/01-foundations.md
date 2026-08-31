# 1. Networking foundations

## The useful layer model

Do not treat OSI as a debugging script. Use layers to limit the search space.

| Layer | Application-engineer question | Examples |
| --- | --- | --- |
| Application | Did the service understand and accept the request? | HTTP, gRPC, DNS |
| Security/session | Did identity and encryption negotiate? | TLS, mTLS, cookies |
| Transport | Can the two processes exchange bytes reliably? | TCP, UDP, ports |
| Network | Can packets reach the right host? | IP, routing, NAT |
| Link | Can the local network carry frames? | Ethernet, ARP/ND, VLAN |

Start with the error and move down only as far as needed. An HTTP `503` proves
that some HTTP-speaking component answered. A TCP timeout does not.

## Addressing, ports, routing, and NAT

- An **IP address** identifies an interface in an IP network; IPv4 uses 32
  bits and IPv6 uses 128 bits.
- A **port** identifies a transport endpoint on a host. A TCP flow is commonly
  distinguished by source IP/port and destination IP/port plus protocol.
- A **route** chooses a next hop by longest-prefix match. A default route is
  the fallback, not a promise that the destination is reachable.
- **NAT** rewrites addresses and sometimes ports. Source NAT (SNAT) commonly
  gives return traffic a route back through a proxy or load balancer.

Private IPv4 addresses are not Internet-routable. If a backend only knows a
private client address but its default route bypasses the LTM, a direct-server
return problem can result; SNAT is one common way to avoid the asymmetric path.

## TCP, UDP, and ports

TCP provides an ordered byte stream with reliability, flow control, and
congestion control. The TCP handshake establishes shared connection state:

```text
client                              server
  SYN  ---------------------------->
       <----------------------- SYN-ACK
  ACK  ---------------------------->
  application bytes <===========> application bytes
```

TCP does not preserve message boundaries. An application protocol must frame
messages itself (for example HTTP headers and a body length). TCP uses a
four-way close in the normal case; `RST` is an abrupt reset.

UDP is datagram-oriented and does not add TCP-style reliability or ordering.
It is useful when the application can tolerate loss or implements its own
recovery (for example DNS and QUIC's transport over UDP). “UDP is faster” is
too vague: compare latency, loss behavior, ordering, connection setup, and
application requirements.

## TLS and HTTP

TLS authenticates the peer (subject to certificate validation) and encrypts
application bytes. The TLS Server Name Indication (SNI) extension lets a client
indicate the intended hostname during setup; it matters where multiple HTTPS
sites share an address. TLS termination means the proxy decrypts traffic and
typically initiates a separate connection to the backend. That creates two
independent failure domains and requires thoughtful header and identity policy.

HTTP is an application protocol. A status code is evidence about the component
that returned it, not necessarily the origin application. For example, an LTM,
reverse proxy, API gateway, or service can all produce a `502`/`503`.

## DNS essentials

DNS maps names to resource records. A stub resolver asks a recursive resolver;
the recursive resolver may consult authoritative servers and cache answers.

| Record | Typical purpose |
| --- | --- |
| A / AAAA | IPv4 / IPv6 address |
| CNAME | Alias to another canonical name |
| NS | Nameserver delegation |
| MX | Mail exchanger |
| TXT | Text data, often verification or policy |

The **TTL** bounds how long a resolver may cache an answer; it does not force
all clients to re-query exactly at expiry and cannot retract answers already
cached. Negative answers can also be cached. Plan traffic migrations around
observed resolver behavior, not a simplistic instant cutover assumption.

## Observability: map evidence to layers

| Symptom | First evidence to collect | Likely layer(s) |
| --- | --- | --- |
| `NXDOMAIN` | `dig name A`, authoritative zone/answer | DNS |
| Connect timeout | destination, route, security policy, SYN/SYN-ACK capture | Network/transport |
| `Connection refused` | listener and target address/port | Transport/application |
| TLS certificate error | hostname, SNI, certificate chain, clock | TLS |
| `502` or `503` | responder identity, proxy/LB logs, pool health | HTTP/application/LB |

Useful tools: `dig`, `curl -v`, `openssl s_client`, `ss -lntp`, `traceroute`
or `tracepath`, packet capture, and application/load-balancer logs. Use the
least privileged approved tool, and never paste credentials into diagnostics.
