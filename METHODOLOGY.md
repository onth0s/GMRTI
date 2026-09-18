# GMRTI Methodology & Status Markers

This document defines the lifecycle, validation requirements, and epistemic
authority of theoretical claims within the GMRTI framework. It establishes the
non-negotiable behavioral contracts for authoring and refactoring the treatise.

**Ma — Status Markers and Invariant Graduation**

**Ma.1** Theoretical claims within GMRTI are tagged with Status Markers. These
    markers dictate the claim's load-bearing authority and serve as invariants
    in the CLDS workflow:

- `[OPEN]`: A known unresolved design challenge. High semantic entropy is
  expected.
- `[PROVISIONAL]`: A claim held with operational confidence but still open to
  fundamental revision. It has not yet survived a full adversarial audit.
- `[STABLE]`: A formal invariant. It is considered load-bearing, and changes
  here propagate broadly. Any refactor that breaks a `[STABLE]` claim without
  deliberately invoking the Refinement Cycle to downgrade it is an error.
  *Epistemic boundary*: `[STABLE]` marks authorial closure — a claim not
  currently undergoing revision in order to prevent infinite regress and
  self-consuming refinement (see §3g.2) — not an assertion of metaphysical
  truth or objective proof.
- `[RECURSIVE]`: A claim that applies to the framework itself and must be
  checked for self-consistency (e.g., the claim that all language is
  high-entropy applies to the language of GMRTI).
- `[RESTORED]`: Content recovered after compression loss in prior iterations.
- `[EXCISED]`: Content formally retired from the operational framework to
  eliminate ambiguity, avoid regress, or adhere to architectural separation
  (such as deferring typing under JIT-OM). Retained in situ with an explicit
  provenance note to preserve address stability and auditability while marking
  the content as operationally inert.
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
- **Secondary Reflexive / Provenance / Structural Dimension**:
- `[RECURSIVE]`: Indicates that the claim reflexively binds the GMRTI's own
    authoring, representation, and transmission processes.
- `[RESTORED]`: Indicates historical provenance — recovered after
    compression loss in prior iterations.
- `[EXCISED]`: Indicates historical retirement — preserved at its original
    address for citation integrity, but excluded from operational inference.
- `[ALLEGORY]`: Indicates a concrete polyphonic worked instantiation.
- `[PLAIN]`: Indicates a high-school-level entry ramp compiled into
    `PEBBLE.md`.


In compound forms, the primary epistemic status dictates the claim's invariant
rigidity; the secondary tag specifies its reflexive scope or historical
preservation requirement.

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

A claim graduates from `[PROVISIONAL]` to `[STABLE]` only when it satisfies both
of the following non-negotiable conditions:

1. **Survival of Adversarial Audit**: The claim's content has been subjected to
   a
   formal `DISSONANCE.md` critique by an external or context-free agent and has
   survived without requiring fundamental structural alteration (i.e., it
   required at most Surface or minor Structural repair).
2. **Satisfaction of Invariant Dependency (Ma.3)**: All concepts, mechanisms,
   and
   definitions upon which the claim rests must themselves be established
   `[STABLE]` invariants, or carry an explicit provisional dependency boundary
   declaration. A claim whose load-bearing dependencies remain un-graduated is
   structurally blocked from `[STABLE]` graduation.

When a claim satisfies both conditions, it graduates to `[STABLE]` and becomes
an architectural invariant.
