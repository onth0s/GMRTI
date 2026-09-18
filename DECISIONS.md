# GMRTI Decision Log: Refinement Marching Orders

This log defines the ratified resolutions to be implemented in the treatise to
resolve contentions established in `DISSONANCE.md` (Refinement Cycle Step 3).
Entries act strictly as a bullet-point list of *WHAT* must be addressed.

---

## Active Marching Orders

### [DEC-001] Creation of Machine-Readable Concept Specifications for Foundational Entities (D-001)
- **Decision**: Formulate and install `concept_drc.yaml`,
  `concept_artifact_anchor.yaml`, and `concept_temporal_drift.yaml` as
  `PROVISIONAL` specs with full invariants.
- **Action Items**:
- Author `specs/concept_drc.yaml` (GMRTI-DRC).
- Author `specs/concept_artifact_anchor.yaml` (GMRTI-ARTIFACT-ANCHOR).
- Author `specs/concept_temporal_drift.yaml` (GMRTI-TEMPORAL-DRIFT).
- Verify dependency resolution in `test_specs.py`.

### [DEC-002] Formalization and Compilation of Section 8 (D-002)
- **Decision**: Fully author `src/08_gaps.md` to catalog known theoretical gaps,
  structural boundaries, and open challenges; integrate into `rewrite.py`
  `ASSEMBLY_MANIFEST`.
- **Action Items**:
- Author `src/08_gaps.md` covering the Horizon Problem, active theoretical
    contentions, and open refinement vectors.
- Add `src/08_gaps.md` to `ASSEMBLY_MANIFEST` in `rewrite.py`.
- Update `test_rewrite.py` to assert Section 8 presence.

### [DEC-003] Formalization of Compound Status Markers in Methodology (D-003)
- **Decision**: Ratify compound status markers as valid dual-predicate semantic
  annotations in `METHODOLOGY.md`.
- **Action Items**:
- Update `METHODOLOGY.md` to define compound markers (`[STATUS_1][STATUS_2]`),
    their composition rules, and semantic intent.

### [DEC-004] Rectification of Typographical and Historical Ref Drifts (D-004)
- **Decision**: Correct grammatical and referential inaccuracies in
  `src/02_architecture.md` and `src/00_preamble.md`.
- **Action Items**:
- Correct "a Anchor-Only" to "an Anchor-Only" in `src/02_architecture.md`.
- Replace dangling reference "R7" in `src/00_preamble.md` with explicit
    reference to Section 3b.4 / 3c.2 (Meta-DRC Alignment).

### [DEC-005] Synchronization of Plain-English Guide (PEBBLE.md) (D-005)
- **Decision**: Align PEBBLE Section 5 connection ordering with canonical Tier 2
  sequence and link Section 7 protocol commands to rule 3e.1vi.
- **Action Items**:
- Reorder connections in `PEBBLE.md` Section 5 to: Inferential, Causal,
    Procedural, Affective, Normative, Identity, Referential, Structural.
- Reference clause 3e.1vi in `PEBBLE.md` Section 7.

### [DEC-006] Codification of Tooling Verification Gates in REP Protocol (D-006)
- **Decision**: Mandate local execution boundaries (`wrap.py --check`,
  `rewrite.py --check`, `pytest`) in `REFINEMENT.md`.
- **Action Items**:
- Add Section 3 to `REFINEMENT.md` formalizing local verification gates.
