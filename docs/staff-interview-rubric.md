# Staff interview rubric

Use this rubric for architecture, incident-leadership, and platform-strategy
answers. It complements the [general interview rubric](interview-rubric.md).

## Scorecard

| Dimension | 0 | 2 | 4 |
| --- | --- | --- | --- |
| Framing | Jumps to a solution | States some assumptions | Clarifies ambiguity, users, SLOs, constraints, and success metrics |
| Technical depth | Names components | Traces a plausible path | Explains state, control/data planes, capacity, and failure domains |
| Trade-offs | Claims one “best” design | Compares two options | Quantifies cost, risk, operability, migration cost, and reversibility |
| Ownership | Assumes one team owns all work | Names dependencies | Defines durable ownership, interfaces, escalation, and adoption plan |
| Influence | Gives an individual fix | Communicates a decision | Handles dissent, aligns stakeholders, and changes systems or behavior |
| Verification | Says “monitor it” | Names a metric | Defines canary, falsifier, rollback, and measurable post-change proof |

## Staff answer shape

1. **Frame:** restate the problem, impact, SLO, scale, and constraints.
2. **Model:** draw request path, control path, state owners, and trust boundaries.
3. **Quantify:** estimate demand, concurrency, failure load, headroom, and cost.
4. **Choose:** compare alternatives and explain the rejected option.
5. **Evolve:** describe migration stages, ownership, adoption, and rollback.
6. **Verify:** name signals, a falsifier, decision gates, and the next learning.

> *Staff-level does not mean adding more components.* It means making the
> smallest durable decision that reduces risk across teams and over time.

## Readiness gate

Target an average of **3.5/4**, with no ownership, safety, or verification
score below **3**. Pass two designs, one ambiguous incident, one coding or
reconciliation exercise, and one behavioral scenario. Answers must label
protocol facts, vendor terminology, and engineering inferences.
