# GMRTI Ratified Execution Plan (PLAN.md)

This document formalizes the ratified implementation plan for active decisions
(REP Cycle Phase 3). Work is structured into imperatively sequential phases with
explicit boundary verification.

---

## Active Plan

### Sequence 1: Theoretical & Guide Alignment (DEC-003, DEC-004, DEC-005, DEC-006)
- **Target Files**:
- `METHODOLOGY.md`
- `src/02_architecture.md`
- `src/00_preamble.md`
- `PEBBLE.md`
- `REFINEMENT.md`
- **Execution Boundary**: All target text files wrapped and formatted; `python
  wrap.py --check` passes; all existing unit tests pass.
- **Verification Command**: `python wrap.py --check && python -m pytest tests/
  -v`

### Sequence 2: Machine-Readable Concept Specifications (DEC-001)
- **Target Files**:
- `specs/concept_drc.yaml`
- `specs/concept_artifact_anchor.yaml`
- `specs/concept_temporal_drift.yaml`
- **Execution Boundary**: All new YAML specifications conform to schema and
  resolve all dependencies without cycles or missing references.
- **Verification Command**: `python -m pytest tests/test_specs.py -v && python
  wrap.py --check`

### Sequence 3: Section 8 Formalization & Compilation Pipeline (DEC-002)
- **Target Files**:
- `src/08_gaps.md`
- `rewrite.py`
- `tests/test_rewrite.py`
- **Execution Boundary**: `src/08_gaps.md` is authored with complete horizon
  analysis; added to `ASSEMBLY_MANIFEST` in `rewrite.py`; tests updated to
  assert Section 8 presence.
- **Verification Command**: `python wrap.py --check && python -m pytest tests/
  -v`

### Sequence 4: Monolithic Recompilation & Final Alignment Audit
- **Target Files**:
- Workspace root `GMRTI_<timestamp>.md`
- `archive/` directory
- **Execution Boundary**: New monolithic document compiled; prior monolithic
  archived per `AGENTS.md`; `rewrite.py --check` validates byte-level
  synchronization; 0 link or schema errors.
- **Verification Command**: `python rewrite.py && python rewrite.py --check &&
  python wrap.py --check && python -m pytest tests/ -v`
