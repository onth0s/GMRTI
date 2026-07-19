# GMRTI Refinement Plan: Execution Sequence

This plan details the exact files and modifications required to execute the decisions in `DECISIONS.md` in a sequential, stable manner.

---

## Sequence Phase 1: YAML Specifications (`specs/`)
We will create and update the concept specifications in the `specs/` directory to codify our new architectural invariants.

### 1.1 Update `specs/concept_covenant.yaml`
- Modify status and invariants to reflect self-annotation baseline.

### 1.2 [NEW] `specs/concept_forcing.yaml`
- Define the `GMRTI-FORCING` concept (Syntactic Edge-Forcing operator set and rules).

### 1.3 [NEW] `specs/concept_entropy.yaml`
- Define the `GMRTI-ENTROPY` concept (Semantic Entropy Metric \(H_s\) and path-count proxy).

### 1.4 [NEW] `specs/concept_meta_drc.yaml`
- Define the `GMRTI-META-DRC` concept (Meta-DRC Divergence and default behavior).

---

## Sequence Phase 2: Core Treatise Updates (`src/`)

### 2.1 Update `src/01_problem.md`
- **1a.6:** Incorporate the formal definition of Semantic Entropy \(H_s\) and the Behavioral Convergence Proxy.
- **1c.1 / 1c.4:** Formally declare Self-Annotation as the bootstrapping sandbox use case and establish the developmental ordering.

### 2.2 Update `src/02_architecture.md`
- **2a.5:** Formally structure the Tier 1 coarse cut vs. Tier 2 JIT-OM taxonomy, specifying when each is active.
- **2g.4 / 2g.7:** Proscribe the exact set of primitive relational operators (`->inferential`, `->causal`, `->procedural`, `->normative`, `->identity`, `->referential`, `->affective`, `->structural`) and show how they are syntactically embedded.
- Apply these operators to the key `[STABLE]` claims within `src/01_problem.md` and `src/02_architecture.md` (e.g. `1a.1`, `1a.2`, `1a.3`, `2a.2`) as a working prototype.

### 2.3 Update `src/03_algorithm.md`
- **3c.2:** Integrate the detection of Meta-DRC Divergences.
- **3e.1iii:** Add explicit repair steps for Edge-Type Misattribution and Meta-DRC Divergences (pausing communication and defaulting to the highest demanded DRC).

### 2.4 Update `src/08_open_challenges.md`
- Move `8b.1` (DRC Classification) to `8a` (Resolved as Meta-DRC Alignment).
- Move `8b.2` (Bad Actor) to `8a` (Resolved via Topological Consistency Audit).
- Move `8b.3` (Artifact Anchor Decay) to `8a` (Resolved via Periodic Re-Mirroring Protocol).
- Move `8c.2` (Redundancy-Masking Detection) to `8a` (Resolved via Path-Stripping Probing).
- Move `8c.4` (Structural Integrity Metric) to `8a` (Resolved via Semantic Entropy Metric).
- Move `8c.5` (Axiomatic Visibility) to `8a` (Resolved via Dependency-Tracing Scan).
- Document these resolved protocols under their new headings in **8a**.
- Ensure remaining challenges in **8b** and **8c** are correctly updated.

---

## Sequence Phase 3: Glossary & Refinery Updates

### 3.1 Update `glossary.md`
- Update definitions: Semantic Entropy, Edge Taxonomy, Syntactic Edge-Forcing.
- Add definitions: Meta-DRC Divergence, Topological Consistency Audit, Periodic Re-Mirroring Protocol, Path-Stripping Probing, Dependency-Tracing Scan.

### 3.2 Update `refinery/R*.md` Files
- **R1, R2, R3, R4, R5, R7:**
  - Change status tag in headers from `[OPEN]` or `[NEW][OPEN]` to `[RESOLVED]`.
  - Append a resolution summary to the end of each file detailing *how* it was resolved and linking to the exact sections in the `src/` files, without compressing or removing the original open questions (preserving full depth).

---

## Sequence Phase 4: Verification & Compilation
- Run `python rewrite.py` to compile the monolithic treatise.
- Conduct a validation check on the generated file to verify alignment, spelling, and structural integrity.
