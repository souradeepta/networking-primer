# Networking Primer learning path

This repository is a vendor-aware learning curriculum, not an operational
runbook. Move from request-path fundamentals to platform-specific evidence,
then use the role artifacts to practice explaining decisions.

## Four-session foundation

1. **Foundations:** [networking foundations](docs/01-foundations.md) and
   [request path](docs/02-request-path.md). Produce a packet/request trace
   that identifies the first failing layer.
2. **Local delivery:** [F5 LTM](docs/03-f5-ltm.md), [troubleshooting](docs/05-troubleshooting.md),
   and [LTM topics](book/topics/01-vips-and-virtual-servers.md). Produce a VIP,
   profile, pool, monitor, SNAT, and return-path evidence table.
3. **Global and platform delivery:** [GTM/BIG-IP DNS](docs/04-f5-gtm.md),
   [DDI](docs/06-ddi.md), cloud/Kubernetes, BGP/anycast, and security topics.
   Produce a resolver-aware migration or failover decision record.
4. **Automation and design:** [automation](docs/07-automation.md), capacity,
   observability, Staff simulations, and focused-topic deep dives. Produce a
   reviewed change plan with owners, cost/risk, rollout, rollback, and a
   falsifier for the leading hypothesis.

## Focused-topic progression

Use [the focused-topic index](book/topics/README.md) for the maintained
39-topic sequence. Topics 01–16 establish F5, DNS, DDI, operations, cloud, and
security foundations; 17–27 cover transport and systems mechanics; 28–37
cover F5 implementation and distributed/cloud design; 38–39 cover modern
DNS/IPv6 and edge abuse defense. The HTTP overview is topic 17, with protocol
deep dives in topics 22–23.

Every topic includes SDE2/Staff calibration, an expected artifact, evidence
scope, and a Staff follow-up. Facts and vendor terminology must be separated
from engineering inference and verified against the target release.

## Role exit artifacts

- **SDE1:** explain the request path and select a safe read-only check.
- **SDE2:** provide mechanism, evidence, trade-offs, implementation detail,
  and a falsifier for a diagnosis or design.
- **Staff:** add ownership boundaries, migration/adoption sequencing,
  quantified capacity/cost/risk, stakeholder communication, and an explicit
  stop condition for irreversible failure.

Use the [Staff design review pack](docs/staff-design-review-pack.md),
[simulation pack](docs/interview-simulation-pack.md), and [Staff rubric](docs/staff-interview-rubric.md)
to score the artifacts.

## Verification before handoff

```bash
./scripts/validate.sh
python3 examples/request_path.py
git diff --check
```
