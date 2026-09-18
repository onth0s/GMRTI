# GMRTI — General Method for Refinement and Transmission of Ideas
### A Living Framework Document · Tenth Iteration (v0.9 Candidate)

---

> *This document is itself a primary test case of the GMRTI. Every claim herein
> is subject to the same refinement discipline it prescribes. Where the
> framework is uncertain, it says so. Where it is provisional, it stays
> provisional. Where it is structural, it is named as such. The document is not
> trying to win by compression; it is trying to remain true under
> reconstruction.*

---

## Table of Contents

- [Glossary](GLOSSARY.md)
- [0. Preamble and Document Conventions](src/00_preamble.md)
- [1. The Problem the GMRTI Addresses](src/01_problem.md)
- [2. Foundational Architecture: The Topological Network
  Model](src/02_architecture.md)
- [3. The GMRTI Algorithm](src/03_algorithm.md)
- [4. Temporal Anchoring](src/04_temporal_anchoring.md)
- [5. The Metalanguage Problem and Just-In-Time Ontological
  Marking](src/05_metalanguage.md)
- [6. The GMRTI in Operation: Refinement Vectors](src/06_refinement_vectors.md)
- [7. Relation to Downstream Applications](src/07_downstream.md)
- [8. Known Gaps and Open Challenges](src/08_gaps.md) `[OPEN]`
- [Refinery](refinery/)

## Companion & Governance Artifacts

- [PEBBLE: The Plain-English Alignment Guide](PEBBLE.md)
- [Architectural Authority & Entities](ARCHITECTURE.md)
- [Methodology & Invariant Graduation](METHODOLOGY.md)
- [The Refinement Cycle & Execution Protocol](REFINEMENT.md)
- [Concept Specifications (CLDS)](specs/)
- [Formal Model (Lean 4)](math/)

## Development

**Install dependencies:**

```
pip install -r requirements.txt
```

**Run tests:**

```
python -m pytest tests/ -v
```

**Check formatting:**

```
python wrap.py --check
```

**Check monolithic document sync:**

```
python rewrite.py --check
```

**Recompile monolithic document:**

```
python rewrite.py
```

**Full local build & verification (PowerShell):**

```powershell
.\build.ps1               # Builds everything: format, compile, sync check, and run tests
.\build.ps1 -CheckOnly    # Optional bypass: run checks and tests only (no write)
.\build.ps1 -SkipTests    # Optional bypass: format, compile, and sync check without pytest
```

## Formal Verification (Lean 4)

A standalone satellite verification package in `math/` provides machine-checked
proofs of the quantitative properties latent in GMRTI (hypothesis-space
contraction, steady-state tracking bounds, multipath monotonicity).

```bash
cd math
lake build
```
