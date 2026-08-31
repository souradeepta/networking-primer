# Networking tools and commands

## A. Tool-selection matrix

| Question | First tool | What it cannot prove |
| --- | --- | --- |
| What address will the host use? | `ip route get` | That policy or listener accepts the packet |
| Is a process listening? | `ss -lntup` | Remote reachability or application health |
| Which resolver answered? | `resolvectl`, `dig` | What another namespace or client cached |
| Did TCP complete? | `nc`, `curl -v` | TLS trust, HTTP semantics, authorization |
| Which certificate was served? | `openssl s_client` | Backend certificate unless tested separately |
| Did packets arrive or return? | `tcpdump` | Packets outside the capture point |
| Which hop emitted 503/504? | `curl -v`, proxy logs, trace ID | Root cause without backend evidence |
| Is the host saturated? | `vmstat`, `pidstat`, `ss` | A complete distributed capacity model |
| What does Kubernetes believe? | `kubectl get/describe/events` | That the data plane enforced the intended state |

## B. Safe command patterns

```bash
date -u
ip route get 198.51.100.20
ss -tan state established '( dport = :443 or sport = :443 )'
dig +time=2 +tries=1 +noall +answer api.lab.example A
curl --connect-timeout 3 --max-time 10 -sS -D - https://api.lab.example/health -o /dev/null
```

Prefer numeric output where appropriate, bound time and output, and preserve
the exact command, environment, namespace, and timestamp. Use a small output
limit when logs or socket inventories may contain sensitive metadata.

## C. Host and process commands

| Command | Useful fields | Caution |
| --- | --- | --- |
| `ps` | PID, parent, state, start time, command | Arguments may contain secrets |
| `systemctl status` | Unit state, recent failure | Manager state is not request health |
| `journalctl` | Bounded service timeline | Apply time bounds; redact output |
| `ss` | Socket state, local/peer tuple | `-p` exposes process details |
| `lsof` | Process/file/socket ownership | Can be expensive on large hosts |
| `vmstat` | Run queue, memory, I/O | Samples need workload context |
| `pidstat` | Per-process CPU, faults, I/O | Avoid unbounded intervals |

## D. Network commands

```bash
ip -br addr
ip route show table all
ip rule show
ip neigh show nud failed
ip -s link show dev eth0
tracepath 198.51.100.20
```

`tracepath` and `traceroute` show intermediate responses only when policy
allows them; `*` is not proof of a broken hop. Compare route lookup with a
packet trace and, when possible, the return direction.

## E. DNS and TLS commands

```bash
dig +noall +answer +authority +comments api.lab.example A
dig +noall +answer +authority +comments api.lab.example AAAA
dig +trace api.lab.example
openssl s_client -connect 127.0.0.1:8443 -servername api.lab.example \
  -alpn h2,http/1.1 -showcerts </dev/null
```

`dig +trace` walks delegation and does not reproduce a recursive resolver’s
cache. `openssl s_client` is a diagnostic client, not a complete browser or
application simulation. Test every termination hop and exact SNI.

## F. Packet and flow commands

```bash
sudo tcpdump -ni any 'host 198.51.100.20 and (tcp port 443 or udp port 443)' -c 60
sudo tcpdump -ni eth0 -nn -tttt 'tcp[tcpflags] & (tcp-syn|tcp-rst) != 0' -c 40
```

Use `-nn` to preserve numeric identity and `-tttt` for readable timestamps.
Capture only the smallest slice needed. Do not share payloads, cookies, client
certificates, or private addresses without authorization and redaction.

## G. Kubernetes and container context

```bash
kubectl get svc,endpointslice,pods -n <namespace> -o wide
kubectl describe ingress <name> -n <namespace>
kubectl get networkpolicy -n <namespace>
kubectl get events -n <namespace> --sort-by=.lastTimestamp
kubectl exec -n <namespace> <pod> -- getent hosts api.lab.example
```

State the cluster context and namespace before reading or sharing output. API
objects describe intended or observed control-plane state; verify the CNI,
routes, sidecars, load balancer, and packet path before claiming enforcement.

## H. Separate change-plan commands

Do not treat these as routine diagnostics: `ip route add/del`, `tc`, `iptables`,
`nft`, service restarts, `systemctl stop`, DNS/cache flushes, config writes,
packet injection, broad scans, and `kubectl delete` or `rollout restart`.
Document target, authorization, rate, abort condition, owner, rollback, and
verification before using them in an approved lab or change window.
