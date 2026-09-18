# GMRTI Ratified Execution Plan (PLAN.md)

This document formalizes the ratified implementation plan for active decisions
(REP Cycle Phase 3). Work is structured into imperatively sequential phases with
explicit boundary verification.

---

## Active Plan (v0.9 Candidate Adversarial Audit Resolutions)

### Phase 1: Invariant Harmonization & Mathematical Precision (DEC-01 to DEC-05)
- **Targets**: `GLOSSARY.md`, `src/02_architecture.md`, `src/03_algorithm.md`,
  `src/04_temporal_anchoring.md`, `src/08_gaps.md`
- **Scope**: Standardize DRC to $[0.0, 1.0]$; destination-isomorphism for Core
  Path Minimization; CZP bootstrap scope; Hartley log-count formula for
  Semantic Entropy in §8b.1; exponential smoothing and lag-bounded tracking in
  §4b.3.
- **Verification**: `python wrap.py --check`

### Phase 2: Algorithmic & Operational Enhancements (DEC-06 to DEC-10, DEC-12, DEC-13)
- **Targets**: `GLOSSARY.md`, `src/01_problem.md`, `src/02_architecture.md`,
  `src/03_algorithm.md`
- **Scope**: Two-tier PSP pre-screening (§2f.5iv); integrate 4 orphan terms
  (§2b.2, §2d.4, §3g.4); deploy syntactic edge-forcing prototype in situ (§1a,
  §2a); ground Content-Protocol Stratification in FSM semantics (§3e.1vi);
  refine
  §3c.3 as `[PROVISIONAL]` with functional congruence definition; add
  `[provisional dependency boundary: §3c.3]` to §1a.6, §2f.5iv, §3a.1i, §3c.2;
  add `OPERATIONAL ACTION THRESHOLD` to glossary as `[PROVISIONAL]`.
- **Verification**: `python wrap.py --check`

### Phase 3: Empirical Self-Application & Scope Clarification (DEC-08, DEC-11)
- **Targets**: `src/06_refinement_vectors.md`
- **Scope**: Update §6a.3 to `[PROVISIONAL][RECURSIVE]` documenting partial
  execution of Stages 2–3 via adversarial audit and REP repairs, establishing
  algorithmic Stage 4/5 execution as a validation target; clarify §6b.1 step
  5(b)
  inspection of `refinery/`.
- **Verification**: `python wrap.py --check`

### Phase 4: Structural Governance & Address Hierarchy (DEC-12, DEC-14 to DEC-18)
- **Targets**: `METHODOLOGY.md`, `ARCHITECTURE.md`, `REFINEMENT.md`,
  `src/00_preamble.md`, `src/08_gaps.md`, `README.md`, `rewrite.py`
- **Scope**: Invariant Dependency Constraint; `Aa`, `Ma`, `Ra–Rc` addresses;
  `## APPENDIX A / M / R` compilation transforms; reorder `ASSEMBLY_MANIFEST` to
  place governance at end; link `specs/` in `README.md`; define `[EXCISED]`; fix
  citations (§0.1, §8b.1).
- **Verification**: `python wrap.py --check && python -m pytest
  tests/test_links.py tests/test_rewrite.py -v`

### Phase 5: Machine-Readable Concept Specifications (DEC-02, DEC-05)
- **Targets**: `specs/concept_polyphony.yaml`,
  `specs/concept_artifact_anchor.yaml`
- **Scope**: Align invariants with destination-isomorphism + route-independence,
  and exponential smoothing + lag-bounded tracking.
- **Verification**: `python -m pytest tests/test_specs.py -v && python wrap.py
  --check`

### Phase 6: Monolithic Recompilation, Archival & Tooling Verification
- **Targets**: Root `GMRTI_<timestamp>.md`, `archive/`
- **Scope**: Run bare `.\build.ps1` to format, recompile new monolith, archive
  prior revisions, check sync, and run all 29 pytest tests.
- **Verification**: `powershell -ExecutionPolicy Bypass -File .\build.ps1`
