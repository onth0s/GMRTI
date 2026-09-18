# GMRTI Adversarial Audit Log: Dissonance Report

This document records detected structural gaps, contradictions, un-anchored
assumptions, or high semantic entropy regions identified during adversarial
audits (Refinement Cycle Step 1).

The current active audit is documented in full adversarial detail at
[refinery/DISSONANCE.md](refinery/DISSONANCE.md) (Tenth Iteration / v0.9
Candidate Audit, Mirror Mode per §3c.1i).

---

## Summary of Findings (v0.9 Candidate Audit)

| ID | Finding | Severity | Classification | Status |
|---|---|---|---|---|
| D-01 | DRC scale carries three mutually incompatible semantics | Critical | Invariant Violation | Resolved |
| D-02 | Core Path Minimization contradicts Polyphonic Encoding independence | Critical | Invariant Violation | Resolved |
| D-03 | Relational Operator Vocab Terminus contradicts Covenant Zero Protocol | Critical | Invariant Violation | Resolved |
| D-04 | §8b.1 misquotes the Semantic Entropy formula it audits | Major | Formal Defect | Resolved |
| D-05 | Damping Factor "Convergence Theorem" does not follow from update rule | Major | Formal Defect | Resolved |
| D-06 | PSP pre-screening criterion reintroduces circularity | Major | Formal Defect | Resolved |
| D-07 | Proactive Chaotic Probing scheduled in the wrong DRC mode | Major | Architectural Drift | Resolved |
| D-08 | Four [STABLE] glossary terms are orphans with zero body occurrences | Major | Architectural Drift | Resolved |
| D-09 | Refinery has no presence in the compiled monolith | Major | Scope / Compilation | Resolved |
| D-10 | Syntactic Edge-Forcing prototype is displayed, not deployed | Major | Structural Grounding | Resolved |
| D-11 | Content–Protocol Stratification stops regress by fiat | Major | Regress / Metatheory | Resolved |
| D-12 | Self-application claim of the epigraph has no completed instance | Major | Reflexive Validity | Resolved |
| D-13 | [PROVISIONAL] claims carrying [STABLE] structural load | Moderate | Invariant Dependency | Resolved |
| D-14 | Operational Action Threshold used pervasively, absent from §0.4 | Moderate | Vocabulary Drift | Resolved |
| D-15 | Cross-reference errors (§0.1, §8b.1) | Minor | Hygiene | Resolved |
| D-16 | Heading collision and missing addresses for governance artifacts | Minor | Compilation / Hygiene | Resolved |
| D-17 | Governance material precedes the problem statement in monolith order | Minor | Monolith Ordering | Resolved |
| D-18 | specs/ announced in §0.1, absent from README TOC | Minor | Spec Synchronization | Resolved |
| D-19 | §3b.1v excision marker occupies a live address | Minor | Address Hygiene | Resolved |

---

## Detailed Contentions and Resolution Vectors

Full adversarial critiques, citations, and analysis for each finding D-01
through D-19 are preserved in [refinery/DISSONANCE.md](refinery/DISSONANCE.md).
Operational marching orders derived from these findings are cataloged in
[DECISIONS.md](DECISIONS.md) and executed sequentially per [PLAN.md](PLAN.md).
