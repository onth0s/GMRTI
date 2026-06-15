# The Refinement Cycle

This document outlines the formalized workflow for evolving the framework. It is the sanctioned operational pipeline for resolving structural gaps and addressing semantic entropy within the GMRTI.

## 1. The Resolution Pipeline (Dissonance -> Decisions -> REP)

The workflow for evolving the framework is a strict sequence:

1. **Adversarial Audit (`DISSONANCE.md`)**: An auditor (human or agent) reviews the framework and logs structural gaps, contradictions, or high semantic entropy zones into a `DISSONANCE.md` artifact.
2. **Context-Free Review**: Another context-free agent reviews the `DISSONANCE.md` against the current working revision of GMRTI to validate the claims.
3. **Decision Log (`DECISIONS.md`)**: A `DECISIONS.md` file is generated, acting strictly as a bullet-point list of *WHAT* must be addressed (the marching orders). 
4. **Execution (The REP Cycle)**: The actual resolution of those decisions follows the Ratified Execution Protocol (see below).

## 2. The Ratified Execution Protocol (REP) for Theoretical Authoring

The REP cycle guarantees that theoretical and structural integrity is maintained. It must be strictly followed for all changes dictated by `DECISIONS.md`.

- **Phase 1 (Minimal Plan Request)**: The AI proposes a skeletal outline of how to address a bullet point in `DECISIONS.md` (e.g., how to restructure a section). It lists new concepts and their architectural placement. No actual content is written.
- **Phase 2 (Ratification)**: You review the skeleton, apply architectural annotations, and reject or approve the approach.
- **Phase 3 (Full Plan Elaboration)**: The AI drafts `PLAN.md`, dividing the work into logical sequences with distinct boundaries.
- **Phase 4 (Sequential Execution)**: The AI updates the YAML specs and the Markdown source files sequentially. **Crucially**, this is an imperatively procedural execution: if something breaks on Sequence Phase 3, DO NOT PROCEED with Sequence Phase 4.
- **Phase 5 (Alignment Audit)**: A context-free review ensures the new content aligns with both the ratified plan and the established `[STABLE]` invariants.
