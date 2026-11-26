# GMRTI Methodology & Status Markers

This document defines the lifecycle, validation requirements, and epistemic
authority of theoretical claims within the GMRTI framework. It establishes the
non-negotiable behavioral contracts for authoring and refactoring the treatise.

### Ma — Status Markers and Invariant Graduation
**Ma.1** Theoretical claims within GMRTI are tagged with Status Markers. These
    markers dictate the claim's load-bearing authority and serve as invariants
    in the CLDS workflow:

- `[OPEN]`: A known unresolved design challenge. High semantic entropy is
  expected.
- `[PROVISIONAL]`: A claim held with operational confidence but still open to
  fundamental revision. It has not yet survived a full adversarial audit.
- `[STABLE]`: Authorial closure — a formal structural commitment not currently
  undergoing revision in order to prevent infinite regress and self-consuming
  refinement (see §3g.2). Changes here propagate broadly, so any refactor that
  alters a `[STABLE]` claim must deliberately invoke the Refinement Cycle.
  *Epistemic boundary*: `[STABLE]` marks authorial closure and dependency-clean
  integration (Ma.3), not an assertion of metaphysical truth, final proof, or
  permanent immunity from revision.
- `[RECURSIVE]`: A claim that applies to the framework itself and must be
  checked for self-consistency (e.g., the claim that all language is
  high-entropy applies to the language of GMRTI).
- `[ALLEGORY]` (or `[ALLEGORY: <TargetConcept>]`): A concrete domain-specific
  worked instantiation serving as an independent, destination-isomorphic
  polyphonic-encoding path to an abstract target concept.
- `[PLAIN]`: A plain-language seed sentence for a section or concept, written
  at a high-school reading level. Extracted by `pebble.py` to compile
  `PEBBLE.md`. Must appear as the first sub-paragraph of a section, before any
  formal notation or jargon is introduced. Never carries an epistemic claim —
  it is a transmission layer, not an invariant.

**Ma.2 — Compound Status Markers**

Claims may carry compound markers (e.g., `[STABLE][RECURSIVE]`,
`[PROVISIONAL][ALLEGORY]`) when multiple orthogonal status dimensions intersect:

- **Primary Epistemic Dimension**: `[OPEN]`, `[PROVISIONAL]`, or `[STABLE]`,
  defining the claim's verification stage and invariant authority.
- **Secondary Reflexive / Structural Dimension**:
- `[RECURSIVE]`: Indicates that the claim reflexively binds the GMRTI's own
    authoring, representation, and transmission processes.
- `[ALLEGORY]`: Indicates a concrete polyphonic worked instantiation.
- `[PLAIN]`: Indicates a high-school-level entry ramp compiled into
    `PEBBLE.md`.


In compound forms, the primary epistemic status dictates the claim's invariant
rigidity; the secondary tag specifies its reflexive scope or structural role.

**Ma.3 — Invariant Dependency Constraint** `[STABLE]`

No `[STABLE]` claim or architectural invariant may rest upon, cite as
foundational, or require the truth of a `[PROVISIONAL]` or `[OPEN]` claim
without an explicit provisional dependency boundary declaration. When a
`[STABLE]` claim requires support from an evolving concept, the dependent
concept must either be audited and graduated to `[STABLE]` via the Refinement
Cycle, or the upstream claim must be constrained to a bounded heuristic scope.
Graduation is a structural, dependency-ordered operation: invariants may only
depend on validated invariants.

**Ma.4 — Graduation Criteria** `[STABLE]`

A claim graduates from `[PROVISIONAL]` to `[STABLE]` (authorial closure) when it
satisfies **Invariant Dependency (Ma.3)**: all concepts, mechanisms, and
definitions upon which the claim rests must themselves be `[STABLE]`, or carry
an explicit provisional dependency boundary declaration. A claim whose
load-bearing dependencies remain un-graduated without a declared boundary is
structurally blocked from `[STABLE]` status.

> [!NOTE]
> **Agentic Context vs. Provenance Tradeoff:** Extended audit logs and
> changelogs are valuable during philosophical development, and in an ideal
> world every claim would retain an explicit provenance and audit track record
> alongside it. In practice, carrying full audit history inside the treatise
> pollutes agentic context windows and degrades signal-to-noise. Because `git`
> already preserves the complete commit-level history implicitly, this
> repository deliberately trades in-document audit trails for a clean current
> monolith and periodically purges resolved logs via `nuke.ps1`.

```diagram LR
TITLE: Authorial Closure Gate (Ma.3 + Ma.4)
PROV["PROVISIONAL Claim — Held with operational confidence"]
DEP{"Invariant Dependency (Ma.3) — All dependencies STABLE or bounded?"}
STAB("STABLE — Authorial closure (§3g.2)")
PROV --> DEP
DEP -->|Yes| STAB
```
