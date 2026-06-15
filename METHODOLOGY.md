# GMRTI Methodology & Status Markers

This document defines the lifecycle, validation requirements, and epistemic authority of theoretical claims within the GMRTI framework. It establishes the non-negotiable behavioral contracts for authoring and refactoring the treatise.

## Status Markers and Invariant Graduation

Theoretical claims within GMRTI are tagged with Status Markers. These markers dictate the claim's load-bearing authority and serve as invariants in the CLDS workflow.

- `[OPEN]`: A known unresolved design challenge. High semantic entropy is expected. 
- `[PROVISIONAL]`: A claim held with operational confidence but still open to fundamental revision. It has not yet survived a full adversarial audit.
- `[STABLE]`: A formal invariant. It is considered load-bearing, and changes here propagate broadly. Any refactor that breaks a `[STABLE]` claim without deliberately invoking the Refinement Cycle to downgrade it is an error.
- `[RECURSIVE]`: A claim that applies to the framework itself and must be checked for self-consistency (e.g., the claim that all language is high-entropy applies to the language of GMRTI).
- `[RESTORED]`: Content recovered after compression loss in prior iterations.
- `[NEW]`: Introduced for the first time in the current iteration.

### Graduation Criteria
A claim graduates from `[PROVISIONAL]` to `[STABLE]` only when it satisfies the following condition:
**Survival of Adversarial Audit**: The claim has been subjected to a formal `DISSONANCE.md` critique by an external or context-free agent and has survived without requiring fundamental structural alteration (i.e., it required at most Surface or minor Structural repair). 

When a claim achieves `[STABLE]` status, it becomes an architectural invariant.
