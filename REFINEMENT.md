# The Refinement Cycle

This document outlines the formalized workflow for evolving the framework. It is
the sanctioned operational pipeline for resolving structural gaps and addressing
semantic entropy within the GMRTI.

**Ra — The Resolution Pipeline (Dissonance -> Decisions -> REP)**

The workflow for evolving the framework is a strict sequence:

- **Ra.1 Adversarial Audit (`DISSONANCE.md`)**: An auditor (human or agent)
  reviews the framework and logs structural gaps, contradictions, or high
  semantic entropy zones into a `DISSONANCE.md` artifact.
- **Ra.2 Context-Free Review**: Another context-free agent reviews the
  `DISSONANCE.md` against the current working revision of GMRTI to validate the
  claims.
- **Ra.3 Decision Log (`DECISIONS.md`)**: A `DECISIONS.md` file is generated,
  acting strictly as a bullet-point list of *WHAT* must be addressed (the
  marching orders).
- **Ra.4 Execution (The REP Cycle)**: The actual resolution of those decisions
  follows the Ratified Execution Protocol (see below).

**Rb — The Ratified Execution Protocol (REP) for Theoretical Authoring**

The REP cycle guarantees that theoretical and structural integrity is
maintained. It must be strictly followed for all changes dictated by
`DECISIONS.md`:

- **Rb.1 Phase 1 (Minimal Plan Request)**: The AI proposes a skeletal outline of
  how to address a bullet point in `DECISIONS.md` (e.g., how to restructure a
  section). It lists new concepts and their architectural placement. No actual
  content is written.
- **Rb.2 Phase 2 (Ratification)**: You review the skeleton, apply architectural
  annotations, and reject or approve the approach.
- **Rb.3 Phase 3 (Full Plan Elaboration)**: The AI drafts `PLAN.md`, dividing
  the
  work into logical sequences with distinct boundaries.
- **Rb.4 Phase 4 (Sequential Execution)**: The AI updates the YAML specs and the
  Markdown source files sequentially. **Crucially**, this is an imperatively
  procedural execution: if something breaks on Sequence Phase 3, DO NOT PROCEED
  with Sequence Phase 4.
- **Rb.5 Phase 5 (Alignment Audit)**: A context-free review ensures the new
  content aligns with the ratified plan, verifies that no invariant was broken,
  and strictly validates the Invariant Dependency Constraint (Ma.3) and
  Graduation Criteria (Ma.4) before any `[PROVISIONAL]` → `[STABLE]` graduation
  is ratified.

**Rc — Tooling Verification & Execution Boundaries**

All REP execution boundaries must be verified locally before transition to the
next phase:

- **Rc.1 Formatting Check**: `python wrap.py --check` ensures all markdown and
  YAML sources adhere to the canonical line width without untracked drift.
- **Rc.2 Monolithic Synchronization**: `python rewrite.py --check` guarantees
  the
  root monolithic document is in strict byte-level sync with modular sources.
- **Rc.3 Specification & Unit Tests**: `python -m pytest tests/ -v` validates
  spec schemas, link integrity, and parser contracts.

Per `AGENTS.md`, verification is performed exclusively locally via these Python
scripts and `pytest`.
