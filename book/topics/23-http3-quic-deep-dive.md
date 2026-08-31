# HTTP/3 and QUIC deep dive

## Learning objectives

Describe QUIC packets, connection IDs, TLS integration, independent streams,
loss recovery, migration, and HTTP/3 mapping. Diagnose UDP policy, MTU, ALPN,
and fallback issues across a CDN, F5 boundary, or origin.

## Prerequisites

Know UDP, TCP, TLS 1.3 concepts, HTTP/2 streams, DNS, and firewall flow logs.

## Mental model

QUIC is a reliable, congestion-controlled encrypted transport carried in UDP.
HTTP/3 maps HTTP requests onto QUIC streams. A connection ID lets endpoints
identify a connection across some address changes. TLS supplies handshake and
key agreement; QUIC supplies packet protection, acknowledgements, retransmission,
flow control, and congestion control. Fact: UDP alone supplies none of those
reliability properties. Inference: a UDP allow rule is necessary but does not
prove QUIC health.

## Diagram

```mermaid
%%{init: {"theme":"base", "themeVariables":{"primaryColor":"#ffffff","primaryTextColor":"#111111","lineColor":"#222222"}}}%%
flowchart LR
 C[Client] --> U[UDP path]
 U --> Q[QUIC endpoint]
 Q --> H[HTTP/3 streams]
 H --> E[Edge or F5 boundary]
 E --> O[Origin service]
```

## Worked example

An edge advertises HTTP/3 through Alt-Svc while retaining HTTPS over TCP for
fallback. A client first resolves the name, validates the certificate, and
attempts QUIC on UDP 443. If a corporate firewall drops UDP, the client uses
HTTP/2. Compare protocol outcome, handshake duration, packet loss, and status
at the same edge. A backend can remain HTTP/1.1; protocol termination is a
boundary that must be documented. Changing F5 or CDN profiles requires review
of TLS ownership, idle timeouts, and observability fields.

| Signal | Interpretation | Next check |
| --- | --- | --- |
| ALPN h3 | HTTP/3 negotiated | Request and origin status |
| UDP deny | Path policy issue | Authorized firewall review |
| Retry or loss | Transport/path issue | MTU and congestion evidence |
| h2 fallback | Compatibility path | Fallback rate and user impact |

## When this breaks

Blocked UDP, NAT rebinding, certificate mismatch, unsupported QUIC versions,
path MTU problems, and exhausted stream or connection windows can fail. Some
middleboxes inspect TCP only. A successful fallback can hide degraded mobile
or regional paths. Do not infer that HTTP/3 is faster from a single synthetic
request; compare representative workloads and protocol costs.

## Operational checklist

- Track h3 negotiation, fallback, handshake, and transport errors separately.
- Verify UDP policy and effective MTU on each important path.
- Keep TLS certificate and ALPN configuration versioned.
- Bound stream, connection, and application deadlines.
- Ensure edge logs correlate connection IDs without exposing payloads.
- Test disabling h3 as a reversible rollback.

## Implementation exercise

In a permitted lab, run `curl --http3 -I` and `curl --http2 -I` against a local
endpoint. Record ALPN, status, response bytes, and timing. Use a packet capture
only on your own interface to identify outer UDP and inner protocol evidence.
Write a failure hypothesis for each missing signal and state what observation
would falsify it.

## Questions and answers

1. **Why is QUIC over UDP?** UDP gives QUIC a deployable datagram substrate without imposing TCP's kernel transport behavior. QUIC then implements reliability, congestion control, encryption, and streams itself. This flexibility helps evolution but requires firewalls and observability to understand UDP traffic.
2. **What is connection migration?** Connection IDs can allow a QUIC session to survive some endpoint address changes, such as network transitions. NAT and policy can still prevent it, so applications must handle reconnects and operators must test the actual path.
3. **Does HTTP/3 remove congestion?** No. QUIC has congestion control and shares bottlenecks with other traffic. It mainly changes stream loss behavior and handshake evolution. A congested access link can make HTTP/3 slow even when the origin is healthy.
4. **Why does ALPN matter?** ALPN binds the TLS handshake to an application protocol such as h3. A certificate can be valid while protocol negotiation fails. Record ALPN on every termination hop to separate capability from authorization and service health.
5. **What is 0-RTT risk?** Early data can reduce setup latency but may be replayed by an attacker under protocol conditions. Servers should accept it only for operations safe to replay, and authentication and idempotency rules still apply.
6. **How should fallback be measured?** Count attempted, negotiated, failed, and fallback requests by client and path. A fallback success preserves availability but may indicate blocked UDP or an edge regression, so it deserves an explicit service objective.

## Design notes and evidence

HTTP/3 operations cross several ownership boundaries. DNS chooses an endpoint
for a resolver, an edge chooses a connection policy, and an origin may never
see QUIC if TLS terminates upstream. Record each boundary and its protocol.
Packet captures should distinguish outer UDP headers from encrypted QUIC payload
and should be taken only on authorized lab or production interfaces. For an
F5 or CDN change, validate certificate names, ALPN, UDP policy, effective MTU,
idle timers, and fallback before and after the change. DDI and GTM TTLs affect
which edge new clients reach but do not migrate established connections. These
facts support an inference that protocol rollout must be measured by path and
client population rather than by one synthetic location.
