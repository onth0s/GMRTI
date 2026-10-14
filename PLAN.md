# GMRTI Ratified Execution Plan (PLAN.md)

This document formalizes the ratified implementation plan for active decisions
(REP Cycle Phase 3). Work is structured into imperatively sequential phases with
explicit boundary verification.

---

## Completed Execution (v0.9 Candidate Adversarial Audit Resolutions) `[COMPLETED]`

The REP cycle resolving all active decisions from `DECISIONS.md` (DEC-01 through
DEC-18) and `refinery/DISSONANCE.md` (D-01 through D-19) has been fully executed
and verified.

### Phase 1: Invariant Harmonization & Mathematical Precision (DEC-01 to DEC-05) `[COMPLETED]`
- **Targets**: `GLOSSARY.md`, `src/02_architecture.md`, `src/03_algorithm.md`,
  `src/04_temporal_anchoring.md`, `src/08_gaps.md`
- **Scope**: Standardized DRC to $[0.0, 1.0]$; destination-isomorphism for Core
  Path Minimization; CZP bootstrap scope; Hartley log-count formula for
  Semantic Entropy in §8b.1; exponential smoothing and lag-bounded tracking in
  §4b.3.
- **Verification**: `python wrap.py --check` passed.

### Phase 2: Algorithmic & Operational Enhancements (DEC-06 to DEC-10, DEC-12, DEC-13) `[COMPLETED]`
- **Targets**: `GLOSSARY.md`, `src/01_problem.md`, `src/02_architecture.md`,
  `src/03_algorithm.md`
- **Scope**: Two-tier PSP pre-screening (§2f.5iv); integrated 4 orphan terms
  (§2b.2, §2d.4, §3g.4); deployed syntactic edge-forcing prototype in situ (§1a,
  §2a); grounded Content-Protocol Stratification in FSM semantics (§3e.1vi);
  refined §3c.3 as `[PROVISIONAL]` with functional congruence definition; added
  `[provisional dependency boundary: §3c.3]` to §1a.6, §2f.5iv, §3a.1i, §3c.2;
  added `OPERATIONAL ACTION THRESHOLD` to glossary as `[PROVISIONAL]`.
- **Verification**: `python wrap.py --check` passed.

### Phase 3: Empirical Self-Application & Scope Clarification (DEC-08, DEC-11) `[COMPLETED]`
- **Targets**: `src/06_refinement_vectors.md`
- **Scope**: Updated §6a.3 to `[PROVISIONAL][RECURSIVE]` documenting partial
  execution of Stages 2–3 via adversarial audit and REP repairs, establishing
  algorithmic Stage 4/5 execution as a validation target; clarified §6b.1 step
  5(b) inspection of `refinery/`.
- **Verification**: `python wrap.py --check` passed.

### Phase 4: Structural Governance & Address Hierarchy (DEC-12, DEC-14 to DEC-18) `[COMPLETED]`
- **Targets**: `METHODOLOGY.md`, `ARCHITECTURE.md`, `REFINEMENT.md`,
  `src/00_preamble.md`, `src/08_gaps.md`, `README.md`, `rewrite.py`
- **Scope**: Invariant Dependency Constraint; `Aa`, `Ma`, `Ra–Rc` addresses;
  `## APPENDIX A / M / R` compilation transforms; reordered `ASSEMBLY_MANIFEST`
  to
  place governance at end; linked `specs/` in `README.md`; defined `[EXCISED]`;
  fixed
  citations (§0.1, §8b.1).
- **Verification**: `python wrap.py --check && python -m pytest
  tests/test_links.py tests/test_rewrite.py -v` passed.

### Phase 5: Machine-Readable Concept Specifications (DEC-02, DEC-05) `[COMPLETED]`
- **Targets**: `specs/concept_polyphony.yaml`,
  `specs/concept_artifact_anchor.yaml`
- **Scope**: Aligned invariants with destination-isomorphism +
  route-independence,
  and exponential smoothing + lag-bounded tracking.
- **Verification**: `python -m pytest tests/test_specs.py -v && python wrap.py
  --check` passed.

### Phase 6: Monolithic Recompilation, Archival & Tooling Verification `[COMPLETED]`
- **Targets**: Root `GMRTI_<timestamp>.md`, `archive/`
- **Scope**: Ran bare `.\build.ps1` to format, recompile monolith, archive
  prior revisions, check sync, and run pytest test suite.
- **Verification**: Local build pipeline passed cleanly.

---

## Next Cycle (Future Refinement Target)

The next cycle will initiate under Refinement Cycle Stage 1 (Adversarial Audit),
generating a subsequent `DISSONANCE.md` report targeting:
1. Empirical validation of the Behavioral Convergence Proxy (Path-Count Metric).
2. Cross-model adversarial probing under opposed prompt-covenants (§8b.2).
3. Formal specification of the Self-Annotation validation dataset.

---

## Ratified Execution (v0.9 High-DRC Mirror Audit Repairs) `[RATIFIED 2026-10-14]`

Adversarial audit of the v0.9 Candidate (5 architectural/mathematical defects,
Ma.3/Ma.2 status collisions, mechanical/parser defects) executed per
`misc/v0.9_audit_repair_plan.md` with five cross-phase trap resolutions, and
ratified under REP Rb.5 (no `[PROVISIONAL]` → `[STABLE]` graduations; only
downgrades, holds, and assignments to previously unmarked claims).

- **Treatise**: §2f.5iv disjunctive-hub relabel + single-path PSP rule (§2f.5v
  aligned); §4b.3 post-update lag bound + embedding note (matches
  `math/GMRTI/Temporal.lean`, no Lean change); §3b.1v `[RESTORED]` Tier 1
  Stage 1 cut; §1a.6 pairwise-divergence clarification; §1a.1–1a.3/§2a.2/§2g.7
  edge-forcing operand fixes; §5b.3 `[OPEN]` → `(see §8a.3)`.
- **Markers**: §2c.3/§3c.2 → `[STABLE]`; §2d.2/§2d.4 → `[PROVISIONAL]`;
  GLOSSARY GRAPH-SPACE/DYNAMIC RE-ANCHORING/PERIODIC
  RE-MIRRORING/FEDERATED/ANCHOR → `[PROVISIONAL]` with `[provisional dependency
  boundary: §3c.3]` (plus `§8b.1` on SEMANTIC ENTROPY); full unmarked-entry
  assignment table applied; `a Anchor-Only` → `an Anchor-Only`;
  REDUNDANCY-MASKING bullet rejoined; `[PLAIN]` moved to body paragraphs
  (§0.0/§0.1/§0.2/§9a); LaTeX delimiters standardized (`$...$`/`$$...$$`,
  Aa.12).
- **Tooling**: `pebble.py` heading scan-back fix (zero-content-loss §0.0
  3-paragraph capture).
- **Specs**: `concept_polyphony.yaml` (+disjunctive-hub PSP invariant),
  `concept_artifact_anchor.yaml` (+post-update lag precision),
  `concept_entropy.yaml` (+pairwise-divergence invariant); dates `2026-10-14`.
- **Verification**: `wrap.py --check` clean, `rewrite.py --check` in sync,
  `pytest` 87 passed, `pebble.py --check` in sync, `lake build` success.
