# Unix debugging sessions

These sessions are designed for a Linux host or container lab. They emphasize
read-only inspection and bounded output. Replace `<PID>`, `<PORT>`, and example
addresses with local or approved values.

## A. Session 1 — process and service lifecycle

**Prompt:** A service is reported down. Prove whether the process exists, what
started it, and whether the failure is process, bind, dependency, or listener
state.

```bash
ps -eo pid,ppid,user,stat,lstart,cmd --sort=pid
systemctl status example.service --no-pager
journalctl -u example.service --since '15 minutes ago' --no-pager
```

Collect process state, restart count, exit status, dependency errors, and the
last start time. A process can be running while its listener failed to bind;
service-manager health is not data-plane health.

## B. Session 2 — sockets, queues, and ownership

```bash
ss -lntup
ss -tan state syn-recv
ss -tan state established '( sport = :443 or dport = :443 )'
lsof -nP -iTCP:<PORT> -sTCP:LISTEN
cat /proc/<PID>/limits
```

| Observation | Candidate explanation | Next evidence |
| --- | --- | --- |
| No listener | Wrong bind address, failed startup, wrong port | Service logs and startup configuration |
| Listener only on loopback | Namespace or bind-address mismatch | `ip -br addr`, namespace-local test |
| Many `SYN-RECV` | Arrival exceeds accept capacity or replies are blocked | Backlog counters, CPU, capture, return path |
| Many `CLOSE-WAIT` | Application is not closing peer sockets | Process behavior and connection age |
| Many `TIME-WAIT` | High connection churn or short-lived clients | Connection reuse, ephemeral ports, workload shape |

Do not infer “kernel problem” from a socket count alone; compare limits,
traffic rate, connection lifetime, and application behavior.

## C. Session 3 — addresses, routes, and neighbors

```bash
ip -br addr
ip route show table main
ip rule show
ip route get 198.51.100.20
ip neigh show
ip -s link
ip -6 route get 2001:db8::20
```

Record selected source, interface, next hop, policy table, route metric, and
neighbor state. Distinguish the **RIB/control-plane view** from the **FIB/data-
plane view** where the platform exposes both. A route lookup does not prove
neighbor resolution, ACL permission, return routing, MTU compatibility, or a
listening process.

## D. Session 4 — resolver context and DNS

```bash
cat /etc/resolv.conf
getent ahosts api.lab.example
resolvectl status
resolvectl query api.lab.example
dig +noall +answer +authority +comments api.lab.example A
dig +noall +answer +authority +comments api.lab.example AAAA
```

Compare resolver address, search path, record type, TTL, answer set, split-
horizon view, and query timestamp. A local cache, container namespace, sidecar,
or stub resolver may see a different answer. Do not flush caches or edit DNS as
the first diagnostic action.

## E. Session 5 — TCP and TLS boundary

```bash
nc -vz -w 3 198.51.100.20 443
curl --connect-timeout 3 --max-time 10 -sv https://api.lab.example/health -o /dev/null
openssl s_client -connect 127.0.0.1:8443 \
  -servername api.lab.example -showcerts </dev/null
```

Separate TCP connection, TLS negotiation, certificate validation, HTTP request,
and application authorization. Record SNI, SAN, issuer, validity, ALPN, local
clock, and whether a proxy creates a second TLS session. Use `-k` only for a
deliberate negative lab test.

## F. Session 6 — packet evidence

Use a short, authorized capture with an explicit filter and packet limit:

```bash
sudo tcpdump -ni any 'host 198.51.100.20 and tcp port 443' -c 40
```

Classify SYN silence, SYN-ACK without final ACK, RST, retransmission, completed
TCP followed by TLS failure, and HTTP response. Identify the sender of a reset;
do not label every reset a firewall action. Avoid payload capture where headers,
flow logs, or metadata answer the question.

## G. Session 7 — resource pressure and tail latency

```bash
uptime
free -h
vmstat 1 5
pidstat -p <PID> 1 5
df -h
df -i
```

Correlate CPU run queue, memory reclaim, file descriptors, inode/block space,
socket counts, request queue, and p99 latency. A healthy network path can still
serve failures because the process cannot schedule, allocate, accept, or flush
responses.

## H. Session deliverable

Submit a Markdown note:

```markdown
## Scope and authorization
## Commands and timestamps
## Observed facts
## Competing hypotheses
## Falsifier and next safe test
## Owner, containment, and rollback boundary
## Verification
```
