# Implementation exercises

These exercises turn the book into code. Implement them in a branch, write
tests for edge cases, and explain the layer and failure mode in your README.
Use only reserved addresses, local sockets, or fixture data.

| Exercise | Build | Concepts exercised |
| --- | --- | --- |
| 1. DNS answer classifier | Parse fixture `dig` output into status, TTL, and answers | DNS/GTM, caching, evidence |
| 2. VIP/LTM selector | Select an eligible member with health, weight, and drain state | Pools, monitors, persistence, capacity |
| 3. TLS certificate inventory | Read public PEM metadata and flag expiry/SAN gaps | X.509, SNI, rotation, mTLS trust |
| 4. Request-path tracer | Model DNS -> VIP -> pool and emit structured JSON events | Layered diagnosis and correlation IDs |
| 5. Retry budget simulator | Compare bounded idempotent retries with unsafe duplicate writes | Timeouts, backoff, overload |
| 6. F5 SDK plan generator | Convert desired pool state into a read-before-write diff | REST/SDK, idempotency, audit, rollback |

For every exercise, include malformed input tests, an explicit “no eligible
target” result, and a short fact/inference note. Do not connect to a real F5 or
production DNS system; use mocks and recorded fixtures.
