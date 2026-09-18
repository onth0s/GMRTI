# GMRTI Decision Log: Refinement Marching Orders

This log defines the ratified resolutions to be implemented in the treatise to
resolve contentions established in `refinery/DISSONANCE.md` (Refinement Cycle
Step 3). Entries act strictly as a bullet-point list of *WHAT* must be
addressed.

---

## Active Marching Orders (v0.9 Candidate Adversarial Audit)

### [DEC-01] Unify Domain Risk Coefficient (DRC) Semantics and Range (D-01, D-07)
- Canonical scale is strictly bounded $[0.0, 1.0]$: $0.0 = \text{maximum
  charity / exploratory dialogue}$, $1.0 = \text{zero charity / audit mode /
  catastrophic liability}$. Drop all references to infinity.
- Fix §3a.4, §2e.5 closing line, GLOSSARY.md (DRC and MIB entries), and §2f.5v
  (schedule PCP during dedicated audit/maintenance postures).

### [DEC-02] Align Core Path Minimization with Polyphonic Encoding (D-02)
- Reframe Core Path Minimization in §0.4, §2f.6, and
  `specs/concept_polyphony.yaml`
  to require *destination-isomorphism* (all paths license identical downstream
  operational inferences) while maintaining *route-independence* (paths traverse
  disjoint intermediate topology).

### [DEC-03] Reframe Relational Operator Terminus and Bootstrap Scope (D-03)
- Reframe §3e.1vi as a *regress* terminus rather than repair terminus: operator
  divergence re-runs CZP (§2e.5iii).
- Clarify §2e.5ii/iii: Primitive Covenant bootstraps 3 fundamental operators via
  CZP; remaining 5 are derived types introduced via JIT-OM.

### [DEC-04] Correct Semantic Entropy Formulation and Contention 1 in §8b.1 (D-04)
- Replace Shannon distribution formula with the Hartley log-count formula
  $H_s(S) = \log_2 |\{G_R : G_R \text{ compatible with } S\}|$.
- Reframe Contention 1 to focus on graph-space partitioning and the
  individuation criterion for compatible edge-configurations.

### [DEC-05] Formalize Dynamic Re-Anchoring as Exponential Smoothing (D-05)
- Replace "Convergence Theorem" in §4b.3 and
  `specs/concept_artifact_anchor.yaml`
  with the standard exponential smoothing update rule ($A_{t+1} = (1 -
  \lambda)A_t
+ \lambda A_{decl,t}$) and the Lag-Bounded Tracking Principle ($\text{lag} \le
  \delta \frac{1-\lambda}{\lambda}$).

### [DEC-06] Refine Polyphonic Node Detection Pre-Screening (D-06)
- Split §2f.5iv pre-screening into two tiers: Tier 1 structural pre-screen
  (in/out degree $\ge 2$ in un-typed graph) followed by Tier 2 typed
  evaluation, avoiding circular dependence on edge types.

### [DEC-07] Integrate Orphan Glossary Terms into Treatise (D-08)
- Integrate all 4 orphan terms into load-bearing subsections:
  `Dependency-Tracing
  Scan` (§2b.2), `Periodic Re-Mirroring Protocol` (§2d.4), `Bad Actors`
  (§3g.4), and `Topological Consistency Audit` (§3g.4).

### [DEC-08] Clarify Refinery Audit Scope in Treatise (D-09)
- Explicitly state in §6b.1 step 5(b) that the Refinery audit inspects the
  `refinery/` workspace and its artifacts.

### [DEC-09] Deploy Syntactic Edge-Forcing Prototype In Situ (D-10)
- Formally annotate foundational definitions in §1a.1, §1a.2, §1a.3, and §2a.2
  in situ with primary relational operators `[->structural]`, `[->identity]`,
  `[->causal]`, and `[->procedural]`.

### [DEC-10] Ground Content-Protocol Stratification in FSM Semantics (D-11)
- Reframe protocol meta-commands in §3e.1vi as performative state transitions in
  a finite state machine rather than declarative truth claims, preventing
  infinite regress without arbitrary fiat.

### [DEC-11] Document Completed Self-Application Cycle (D-12)
- Update §6a.3 to designate the executed adversarial audit
  (`refinery/DISSONANCE.md`) as the completed self-application cycle.

### [DEC-12] Invariant Dependency Constraint and Graduation of §3c.3 (D-13)
- Add Invariant Dependency Constraint to `METHODOLOGY.md`: invariants may only
  depend on validated invariants.
- Graduate §3c.3 (Operational Action Threshold) to `[STABLE]`.

### [DEC-13] Add Operational Action Threshold to Glossary (D-14)
- Add formal definition of `OPERATIONAL ACTION THRESHOLD` to `GLOSSARY.md`.

### [DEC-14] Correct Cross-References (D-15)
- Fix §0.1 repair item 5 citation to `(§3c.2, §3e.1v)`.
- Fix §8b.1 citation to `(§0.4, §1a.6)`.

### [DEC-15] Resolve Governance Heading Collisions and Assign Addresses (D-16)
- Render governance artifacts in compiled monolith as `## APPENDIX A / M / R`.
- Assign `Aa.1–11`, `Ma.1–4`, and `Ra–Rc` address conventions.

### [DEC-16] Place Governance Artifacts in Appendices in Monolith (D-17)
- Reorder `ASSEMBLY_MANIFEST` in `rewrite.py` to position governance artifacts
  as Appendices after Section 8.

### [DEC-17] Synchronize Specs in README (D-18)
- Add `[Concept Specifications (CLDS)](specs/)` to the Companion & Governance
  Artifacts list in `README.md`.

### [DEC-18] Formalize `[EXCISED]` Status Marker (D-19)
- Define `[EXCISED]` marker in `METHODOLOGY.md` and `src/00_preamble.md`.
- Mark §3b.1v with `[EXCISED]`.
