# Book and focused-topic review remediation plan

## Review scope

Terra performed a read-only review of all **17 long-form book chapters** and
all **37 focused topic references**, with the repository validator, internal-link
checker, references, and fact/inference ledgers used as supporting evidence.
The review examined:

- Protocol and networking correctness.
- F5, cloud, Kubernetes, and other vendor terminology.
- Contradictions between diagrams, prose, and worked examples.
- Evidence labeling and reference coverage.
- Interview-answer quality, duplication, and SDE2/Staff calibration.
- Topic overlap, missing senior-level concepts, and practice quality.
- Validator blind spots and maintenance risks.

The baseline currently passes `./scripts/validate.sh` and
`python3 examples/request_path.py`. Passing structural checks is not evidence
that every answer is unique, every diagram is semantically correct, or every
vendor claim is sufficiently sourced.

## Prioritized findings

Severity means **High** can teach a materially wrong mental model or weaken
trust in the curriculum; **Medium** reduces coverage or maintainability but is
less likely to cause an immediate conceptual error.

### High: WAF/TLS ordering contradicts the security model

**Location:** [book/17-network-security-waf-zero-trust.md](../book/17-network-security-waf-zero-trust.md),
the first architecture diagram near the WAF example; the later prose and
sequence diagram describe a different order.

**Observed issue:** The diagram places an L7 WAF policy before client TLS
termination, while the prose correctly explains that HTTP inspection requires
the request to be decrypted or otherwise available at the enforcement point.

**Why it matters:** A learner may conclude that an L7 WAF can inspect canonical
HTTP fields inside encrypted traffic without a termination boundary. This is a
direct contradiction inside one chapter, not merely a vendor implementation
difference.

**Fix:** Redraw the diagram so the TLS termination and HTTP/WAF inspection
relationship is explicit. Show either `TLS termination -> HTTP/WAF policy` or
an L4 pass-through boundary followed by a separate terminating WAF. Add a
caption explaining that exact co-residency and inspection features are
product-specific.

### High: route-selection explanation conflates control plane and forwarding

**Location:** [book/02-addressing-subnetting-routing.md](../book/02-addressing-subnetting-routing.md),
the route-selection explanation near the mental model.

**Observed issue:** The text says administrative preference and metrics choose
among equally specific candidates. Longest-prefix match is a forwarding/FIB
decision; administrative distance/preference and protocol metrics commonly
affect which route is installed before forwarding, including routes for the
same prefix learned from different sources.

**Fix:** Separate the sequence into: route advertisements and protocol
selection, RIB installation, FIB programming, and data-plane longest-prefix
match. Add a small example with two sources for one prefix and a more-specific
prefix, plus a caveat that exact preference names and ordering vary by routing
implementation.

### High: focused topics are outside the evidence ledger

**Location:** [book/FACT-INFERENCE-LEDGER.md](../book/FACT-INFERENCE-LEDGER.md)
and `book/topics/`.

**Observed issue:** The ledger covers core chapters and case studies but does
not provide equivalent rows for the 37 focused topics. The gap is most visible
in vendor-heavy topics 28–33 and the new distributed-systems/cloud topics
34–37.

**Fix:** Add a focused-topic ledger section with topic, claim, classification,
source, source version/date where relevant, and target-environment verification
boundary. Start with F5 TMM, SDK/API, LTM selection, BIG-IP DNS, and cloud
networking; then complete the remaining topics. Link the ledger from the
focused-topic README and each topic’s references section where useful.

### High: answer-depth validation is inflated by reusable boilerplate

**Location:** Q&A sections throughout `book/` and `book/topics/`; current
answer parsing in [scripts/validate.sh](../scripts/validate.sh).

**Observed issue:** The validator counts all text after a question until the
next heading. Long “Interview reasoning” blocks therefore satisfy the word
minimum even when the direct answer is only a sentence. Terra also identified
repeated reasoning blocks, including DDI material reused across chapters 1, 3,
15, and 16.

**Why it matters:** The repository can report compliant answers that are not
actually question-specific, explanatory, or interview-ready. Repetition also
increases reading time without increasing transferable understanding.

**Fix:** Make the answer boundary explicit with a consistent `**Answer:**`
marker or dedicated answer paragraph. Validate the direct answer only. Add a
normalized-paragraph duplicate detector with an allowlist for intentional
shared definitions. Replace repeated blocks with short links to a canonical
explanation plus a topic-specific mechanism, evidence, trade-off, and
falsifier.

### Medium: Staff coverage is concentrated in topics 34–37

**Observed issue:** New topics 34–37 contain explicit Staff-tagged prompts,
but most chapters and topics 1–33 do not. The repository now positions itself
for Staff preparation, so the role depth is uneven.

**Fix:** Add at least one Staff-tagged exercise or follow-up to multi-region,
security, automation, LTM/DNS, capacity, cloud/Kubernetes, and observability
material. Require ownership boundaries, migration sequencing, cost/risk,
policy rollout, stakeholder communication, and irreversible-failure handling.

### Medium: Kubernetes NetworkPolicy language overgeneralizes behavior

**Location:** [book/15-cloud-networking-and-kubernetes-ingress.md](../book/15-cloud-networking-and-kubernetes-ingress.md),
the NetworkPolicy discussion.

**Observed issue:** The chapter advises verifying that policies cover both
directions without clearly distinguishing Kubernetes policy objects from the
installed CNI’s enforcement behavior and feature support.

**Fix:** Explain ingress and egress policy as separate constructs, state that
effective enforcement is CNI-dependent, and explicitly test default-deny,
DNS-egress exceptions, namespace/label selectors, and return traffic in the
chosen implementation. Avoid presenting a provider or CNI behavior as a
Kubernetes guarantee.

### Medium: advanced chapters need stronger evidence labels

**Location:** Chapters 15–17, especially
[book/15-cloud-networking-and-kubernetes-ingress.md](../book/15-cloud-networking-and-kubernetes-ingress.md),
[book/16-bgp-anycast-and-multi-region.md](../book/16-bgp-anycast-and-multi-region.md),
and [book/17-network-security-waf-zero-trust.md](../book/17-network-security-waf-zero-trust.md).

**Observed issue:** These chapters make useful protocol, vendor, and platform
claims but do not consistently label facts and inferences at the point of use
or link primary sources as consistently as chapters 1–14.

**Fix:** Add local `**Fact:**`, `**Vendor terminology:**`, and
`**Engineering inference:**` labels where claims affect a design decision.
Link primary IETF, Kubernetes, NIST, F5, and cloud-provider sources. State
release/version boundaries and what must be verified in the target environment.

### Medium: validator coverage is structural rather than semantic

**Location:** [scripts/validate.sh](../scripts/validate.sh) and
[scripts/check_internal_links.py](../scripts/check_internal_links.py).

**Observed issue:** The validator checks counts, headings, approximate word
budgets, tables, Mermaid presence, and file existence. It does not currently
enforce fact labels, source coverage, duplicate-answer detection, Staff/SDE2
distribution, diagram theme configuration, focused-topic index parity, or
valid Markdown anchors. The focused-topic threshold also remains lower than
the current inventory: it requires 33 while 37 exist.

**Fix:** Add semantic checks incrementally rather than one brittle gate:

1. Require the exact current topic count and index/file parity.
2. Check new/advanced topics for evidence labels and a references section.
3. Parse direct-answer boundaries and flag repeated normalized paragraphs.
4. Require role tags across the interview practice artifacts.
5. Verify configured Mermaid light theme variables and ASCII content.
6. Extend the link checker to validate local anchors against generated heading
   IDs, while preserving support for normal Markdown heading rules.

## Remediation plan

### Phase 0 — correctness and trust

- Fix the chapter 17 WAF/TLS diagram.
- Correct chapter 2’s control-plane/FIB/longest-prefix explanation.
- Qualify chapter 15 NetworkPolicy language.
- Audit the three advanced chapters for claims that need explicit fact,
  vendor-term, or inference labels.

**Exit gate:** A reviewer can trace each corrected diagram and paragraph from
claim to source or clearly labeled engineering inference; all existing checks
still pass.

### Phase 1 — evidence governance

- Extend `book/FACT-INFERENCE-LEDGER.md` to all focused topics.
- Add primary references for F5 topics 28–33 and new topics 34–37.
- Record version-sensitive cloud, Kubernetes CNI, managed-LB, and F5 behavior.
- Add a short “verify in target release” convention to the focused-topic README.

**Exit gate:** Every focused topic has a references/evidence section, and every
vendor or platform claim used in a recommendation has a source and scope.

### Phase 2 — answer quality and de-duplication

- Introduce explicit direct-answer boundaries.
- Rewrite duplicated “Interview reasoning” blocks into topic-specific answers.
- Add a duplicate detector with intentional-reuse exceptions.
- Require each senior answer to contain mechanism, evidence, trade-off, and a
  falsifier or caveat.

**Exit gate:** Direct answers meet the depth contract without relying on text
from later generic sections; repeated content is either removed or explicitly
canonicalized.

### Phase 3 — role coverage and pedagogy

- Add Staff-tagged follow-ups across chapters and topics 1–33.
- Add SDE2/Staff role labels, prerequisites, and expected interview artifacts
  to the topic index.
- Ensure multi-region, security, automation, capacity, cloud, and observability
  each include ownership, migration, cost/risk, and adoption reasoning.
- Add one worked Staff answer key to each major domain before adding more files.

**Exit gate:** Staff practice is distributed across the curriculum and not
isolated in topics 34–37; an unfamiliar prompt can be scored using the existing
rubric.

### Phase 4 — validator hardening

- Raise the topic count requirement from 33 to the actual maintained inventory,
  or derive it from the index with an explicit minimum.
- Validate index/file parity and local anchors.
- Validate semantic evidence markers, role tags, and Mermaid theme settings.
- Keep structural checks, but report semantic warnings separately until the
  content has been normalized.

**Exit gate:** The validator catches the known WAF/TLS contradiction class,
missing topic evidence, duplicate direct answers, and stale index entries
without requiring artificial prose padding.

## New material and consolidation decisions

The review does **not** recommend adding many more files immediately. First
repair correctness, evidence, and duplication. After those phases:

- Keep topics 34–37 as the distributed-systems and cloud foundation.
- Add modern DNS/IPv6, edge abuse defense, and routing-underlay topics only if
  they have distinct state models and interview evidence.
- Consolidate or cross-link overlapping HTTP/2 material (topics 17 and 22) and
  HTTP/3/QUIC material (topics 17 and 23) after comparing learning objectives,
  examples, and Q&A; do not duplicate definitions solely to increase counts.
- Prefer canonical explanations with short, topic-specific applications over
  repeated boilerplate.

## Acceptance criteria

- No known high-severity contradiction remains in diagrams or prose.
- The route-selection explanation distinguishes route installation from FIB
  forwarding and longest-prefix match.
- All 37 focused topics are represented in the evidence ledger or explicitly
  marked as having no external claims.
- Direct-answer validation measures the answer itself and duplicate content is
  reported with file and heading locations.
- Staff-tagged material appears across existing major domains, not only topics
  34–37.
- NetworkPolicy and other implementation-specific claims identify the relevant
  CNI/provider/version boundary.
- Focused-topic index parity, local anchors, evidence labels, and Mermaid theme
  constraints are validated.
- `./scripts/validate.sh`, `python3 examples/request_path.py`, and
  `git diff --check` pass after every remediation phase.

## Review discipline

Use this plan as a backlog ordered by severity. When editing material, retain
the repository’s vendor-aware boundary: **protocol facts** come from primary
standards, **vendor terminology/behavior** is version-qualified, and
**engineering inferences** are presented as recommendations with assumptions,
trade-offs, and verification steps.
