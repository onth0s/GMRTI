# GMRTI Adversarial Audit: Dissonance Log

This document logs structural gaps, contradictions, and high-entropy zones
identified during the adversarial audit of the GMRTI framework (v0.9Candidate).

---

## 1. Ontological Classification & Markers (Refinery R1)
- **Dissonance:** Section 5a.1 taxonomy is purely descriptive. There is no
prescription for which ontological types require distinct markers in a JIT-OM
implementation.
- **Ambiguity:** The "carved vs. constructed" binary hypothesis (R1.5) lacks
formal integration. It is unclear how to handle boundary-straddling concepts
(e.g., mathematical concepts which are constructed but operationally carved).

## 2. Syntactic Edge-Forcing & Operator Overhead (Refinery R2)
- **Dissonance:** Syntactic Edge-Forcing (2g) claims to reduce entropy via
grammatical compulsion but is practically unusable if cognitive overhead is too
high.
- **Contradiction:** Mandatory primary relational operators (R2.9) like `A
[->causal] B` introduce a new syntactic layer. However, we haven't defined the
exact set of primitive operators or how they prevent the "edge-typing" metadata
from becoming its own source of semantic entropy.

## 3. Target Use Case Selection (Refinery R3)
- **Dissonance:** The formal layer requirements for Constitutional Drafting
(high overhead, community-to-community), GMRTI-Mediated Dialogue (low overhead,
real-time), and Self-Annotation (medium overhead, self-to-future-self) are
mutually incompatible for a first implementation.
- **Ambiguity:** We have not formally declared which of these three modes is the
definitive starting point of the v0.9 Candidate framework, nor how the other
modes will boot off it.

## 4. Operationalizing Semantic Entropy (Refinery R4 / Section 8c.4)
- **Dissonance:** Semantic Entropy (1a.6) is the framework's central target but
lacks a formal measurement procedure. Without a metric, the framework cannot
quantitatively verify whether entropy is actually reduced.
- **Contradiction:** The "path-count of Polyphonic Encoding" proxy (R4.11)
conflates the transmitter's redundancy with the receiver's internal entropy. We
need a clear, mathematically sound definition of the Operational Action
Threshold as a proxy.

## 5. Edge Taxonomy Economy (Refinery R5 / Section 8c.6)
- **Dissonance:** The eight-type edge taxonomy (2a.5) introduces severe
classification overhead, increasing the risk of Edge-Type Misattribution (2c.3)
due to classifier confusion.
- **Gap:** The two-tiered taxonomy (Tier 1 coarse cut vs. Tier 2 JIT-OM) is
proposed but the exact partition and switching rules are not formalized in
Section 2a.5 or Section 3e.

## 6. Meta-DRC Alignment (Refinery R7 / Section 8b.1)
- **Dissonance:** Communicating parties can disagree on the Domain Risk
Coefficient (DRC), leading to one party demanding strict Mirror Mode while the
other treats the exchange as Low-DRC.
- **Gap:** The candidate repair strategy (Stage 3 Localization and explicit
negotiation) is not integrated into the core GMRTI Algorithm (Section 3).

## 7. Operational and Structural Gaps (Section 8b & 8c)
- **8b.2 The Bad Actor Problem:** Lack of a topological mechanism to detect
intentional fabrication of Edge Divergences.
- **8b.3 Artifact Anchor Decay:** Lack of a methodological protocol for tracking
and repairing desynchronization between a Federated Graph and its Artifact
Anchors.
- **8c.2 Redundancy-Masking Detection:** No formal trigger conditions or path
selection protocols for single-path probing (2f.5iv) to detect hidden voids.
- **8c.5 Axiomatic Visibility Problem:** No reliable method for identifying
which claims operate at the Axiomatic layer before they surface via divergence.
