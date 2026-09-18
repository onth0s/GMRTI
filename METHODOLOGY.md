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
- `[RECURSIVE]`: A claim that applies to the framework itself and must be
  checked for self-consistency (e.g., the claim that all language is
  high-entropy applies to the language of GMRTI).
- `[RESTORED]`: Content recovered after compression loss in prior iterations.
- `[EXCISED]`: Content formally retired from the operational framework to
  eliminate ambiguity, avoid regress, or adhere to architectural separation
  (such as deferring typing under JIT-OM). Retained in situ with an explicit
  provenance note to preserve address stability and auditability while marking
  the content as operationally inert.

**Ma.2 — Compound Status Markers**

Claims may carry compound markers (e.g., `[STABLE][RECURSIVE]`,
`[STABLE][RESTORED]`) when multiple orthogonal status dimensions intersect:

- **Primary Epistemic Dimension**: `[OPEN]`, `[PROVISIONAL]`, or `[STABLE]`,
  defining the claim's verification stage and invariant authority.
- **Secondary Reflexive / Provenance Dimension**:
- `[RECURSIVE]`: Indicates that the claim reflexively binds the GMRTI's own
    authoring, representation, and transmission processes.
- `[RESTORED]`: Indicates historical provenance — recovered after
    compression loss in prior iterations.
- `[EXCISED]`: Indicates historical retirement — preserved at its original
    address for citation integrity, but excluded from operational inference.

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

A claim graduates from `[PROVISIONAL]` to `[STABLE]` only when it satisfies the
following condition: **Survival of Adversarial Audit**: The claim has been
subjected to a formal `DISSONANCE.md` critique by an external or context-free
agent and has survived without requiring fundamental structural alteration
(i.e., it required at most Surface or minor Structural repair).

When a claim achieves `[STABLE]` status, it becomes an architectural invariant.
