# Architecture diagrams and reasoning patterns

These diagrams are deliberately detailed enough to guide a design review while
remaining implementation-neutral. Boxes show responsibilities; they are not an
automatic deployment prescription.

## Multi-site service architecture

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#111111', 'primaryBorderColor': '#222222', 'lineColor': '#222222'}}}%%
flowchart TB
    subgraph ControlPlane[Control plane]
        IPAM[IPAM address allocations]
        AUTH[Authoritative DNS]
        GTM[Big-IP DNS Wide IP and pools]
        MON[Health and capacity signals]
        IPAM --> AUTH
        AUTH --> GTM
        MON --> GTM
    end
    Client[Client application] --> Resolver[Recursive resolver]
    Resolver --> GTM
    subgraph East[East data center]
        EVIP[LTM virtual server east]
        EPOOL[Application pool east]
        EDB[(Data store east)]
        EVIP --> EPOOL --> EDB
    end
    subgraph West[West data center]
        WVIP[LTM virtual server west]
        WPOOL[Application pool west]
        WDB[(Data store west)]
        WVIP --> WPOOL --> WDB
    end
    GTM --> EVIP
    GTM --> WVIP
    MON -. health .-> EVIP
    MON -. health .-> WVIP
```

### Review this architecture with these questions

| Concern | Concrete question |
| --- | --- |
| Failure domain | Can the DNS control plane, an LTM pair, a site, or a dependency fail independently? |
| Consistency | Is it safe for a write to land in either site during DNS cache overlap? |
| Capacity | Does every eligible site have enough capacity for the traffic it can receive? |
| Health | Is a DNS/GTM target marked healthy only when the LTM and application can safely serve? |
| Security | Which hop terminates TLS, validates client identity, and validates upstream identity? |
| Observability | Can one request ID link client, LTM/proxy, application, and dependency evidence? |

## State ownership model

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#111111', 'primaryBorderColor': '#222222', 'lineColor': '#222222'}}}%%
classDiagram
    class IPAM {
      prefix
      address
      owner
      allocationStatus
    }
    class DNSRecord {
      fqdn
      type
      value
      ttl
    }
    class WideIP {
      fqdn
      poolPolicy
      persistence
    }
    class LTMVirtualServer {
      destination
      profiles
      defaultPool
    }
    class PoolMember {
      addressPort
      monitorState
      adminState
    }
    IPAM --> DNSRecord : allocates address for
    DNSRecord --> WideIP : delegates or names
    WideIP --> LTMVirtualServer : returns VIP
    LTMVirtualServer --> PoolMember : selects
```

The meaningful design choice is **ownership**: give each important field a
system of record and a change path. A data model alone does not synchronize
systems.

## Failure propagation sequence

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'primaryColor': '#ffffff', 'primaryTextColor': '#111111', 'primaryBorderColor': '#222222', 'lineColor': '#222222'}}}%%
sequenceDiagram
    participant App as Application instance
    participant LTM as Site LTM
    participant DNS as Big-IP DNS
    participant R as Recursive resolver
    participant C as Client
    App-->>LTM: Readiness endpoint fails
    LTM-->>DNS: Site virtual server health changes
    DNS-->>DNS: Recompute eligible Wide IP pool
    C->>R: New DNS lookup
    R->>DNS: Cache miss lookup
    DNS-->>R: Alternate site answer and TTL
    R-->>C: Alternate site address
    Note over C,R: Cached prior answers may continue until expiry
```

Do not model a DNS change as a synchronous redirect. Existing clients can have
cached answers and open connections, so application resilience remains needed.
