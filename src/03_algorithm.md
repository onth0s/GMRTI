## SECTION 3 — The GMRTI Algorithm

**3a — Overview and Termination Conditions** `[STABLE][RESTORED]`

**3a.1** The GMRTI algorithm is a recursive diagnostic-and-reconstruction cycle. It terminates when one of three conditions is met:

- **3a.1i** *Operational Parking*: the transmission has achieved a comosí of sufficient depth for the practical purposes at hand — operationally defined by the Operational Action Threshold (Section 3c) as producing identical downstream actions or operational definitions within the specific bounded domain.
- **3a.1ii** *Epistemic Termination*: the divergence has been localized to the Axiomatic layer and confirmed as irreducible — meaning the parties genuinely differ in foundational commitments rather than in their understanding of each other.
- **3a.1iii** *Cost-Bounded Termination*: further refinement would exceed the DRC-adjusted benefit threshold. In low-risk domains, a weaker comosí may be rationally sufficient even when deeper repair remains theoretically possible. This condition prevents the framework from becoming self-consuming: a method that cannot say "enough for now" is indistinguishable from a method that cannot act. `[STABLE]`

**3a.2** Distinguishing 3a.1i from 3a.1ii is one of the framework's most demanding practical challenges. Distinguishing either from 3a.1iii is equally important: some transmissions are not unresolved because resolution is impossible, but because it is not worth the remaining cost of further repair. Neither error — premature Operational Parking leaving latent divergence, premature Irreducibility Declaration foreclosing available repair, or misidentifying a Cost-Bounded case as one of the other two — is trivially avoidable. `[STABLE]`

**3a.3** The compiler metaphor introduced in earlier versions remains a mnemonic tool for the algorithm's stages, not a description of the algorithm's nature. The GMRTI is not a compiler. A compiler operates on formally specified inputs with deterministic rules; the GMRTI's entire raison d'être is that such formal specification is unavailable. The compiler metaphor is useful precisely where it highlights the iterative, error-surfacing character of the process — and must be abandoned where it implies deterministic precision the framework structurally cannot provide. `[STABLE]`

**3b — Stage 1: Covenant Declaration** `[STABLE]`

**3b.1** The transmitting party makes explicit the semantic starting conditions of their communication. This involves:

- **3b.1i** Identifying the key topological regions in their covenant that the transmission will rely upon.
- **3b.1ii** Making explicit, where possible, the edges connecting those regions — not just labeling them but describing how they connect to each other and to the rest of the covenant.
- **3b.1iii** Flagging any regions the transmitting party suspects may be Anchor-Only Subgraphs in the receiving covenant.
- **3b.1iv** Applying Polyphonic Encoding to any claim suspected of operating at the Structural or Axiomatic layer — providing multiple independent routes to the same semantic destination.
- **3b.1v** *[Excised in v0.8 to align with JIT-OM principle. Edge-typing is strictly deferred to Stage 3 divergence resolution, maintaining Stage 1 as purely topological.]*

**3b.2** Covenant Declaration is not a demand for agreement. It is a demand for *visibility* — bringing the transmitting covenant's architecture to a level of explicitness where divergence can be detected rather than assumed away. `[STABLE]`

**3b.3** A complete Covenant Declaration is an ideal; in practice, only partial declarations are achievable, because any declaration is itself made in language, which inherits the metaagnostic condition. The goal is maximum achievable explicitness within this constraint. `[STABLE][RECURSIVE]`

**3c — Stage 2: Generative Reconstruction and Interpretive Charity Calibration** `[STABLE]`

**3c.1** Stage 2 is temporally divided to resolve the tension between pure reception and active interpretation:
- **3c.1a (Mirror Mode):** The receiving party operates strictly as a Rationally Agnostic Mirror, suspending interpretive charity to passively map the transmitting party's declared edges exactly as stated, identifying structural gaps.
- **3c.1b (Generative Mode):** Interpretive charity is explicitly re-engaged. The receiver uses their own covenant's topology to build active bridges and scaffolds across the gaps identified during Mirror Mode. `[STABLE]`

**3c.2 — The Domain Risk Coefficient (DRC)**

The required precision of reconstruction scales inversely with interpretive charity, governed by the DRC:

- **High-DRC Domains** (aviation, surgery, law, formal logic): interpretive charity approaches zero. Any minor Edge Divergence triggers immediate localization and repair before transmission proceeds. The Mirror posture is sustained throughout.
- **Low-DRC Domains** (casual dialogue, early-stage creative brainstorming, arts): interpretive charity is maximized. Minor divergences are treated as noise, provided the Operational Action Threshold is met. The Mirror posture is adopted only when a divergence becomes operationally significant.

**3c.3 — The Operational Action Threshold**

Comosí is pragmatically sufficient when the semantic clustering of the two covenants produces identical downstream actions or operational definitions within the specific bounded domain of the transmission. Perfect philosophical alignment is unnecessary if the structural subgraphs route to the same behavioral or logical outputs. `[PROVISIONAL]`

**3c.4** Generative Reconstruction produces two outputs:

- **3c.4i** A *candidate reconstruction* — the receiver's best attempt at building the transmitted concept.
- **3c.4ii** A *divergence report* — an explicit account of where the reconstruction required assumptions, where it was blocked, which divergence type (Anchor-Only Subgraph, Edge Divergence, Temporal Drift) appears to be operative, and — where the Edge Taxonomy is applicable — which edge-type misattribution, if any, may be in play. 
  - **Provisional Divergence Report Template:** To make the Mirror-to-Generative transition explicitly operational, the receiver is encouraged to complete this minimal checklist:
    1. **Structural Gaps Detected:** [List gaps]
    2. **Primary Divergence Type:** [Anchor-Only / Edge Divergence / Temporal Drift]
    3. **Edge-Type Guesses (JIT-OM):** [e.g., Sender treats as Causal, Receiver sees as Inferential]

**3d — Stage 3: Divergence Localization** `[STABLE]`

**3d.1** Using the divergence report from Stage 2, both parties collaboratively identify where specifically in the topological depth structure the transmission failed.

**3d.2** Localization proceeds from the surface inward:

- **3d.2i** Surface divergences are identified and resolved first. Their resolution may dissolve apparent Structural or Axiomatic divergences that were in fact downstream effects of surface failures.
- **3d.2ii** Once Surface divergences are resolved, the process repeats at the Structural layer.
- **3d.2iii** Only after exhausting Surface and Structural repairs does the process proceed to the Axiomatic layer — because declaring Irreducibility prematurely is one of the framework's most consequential error modes.

**3d.3** At each layer, the divergence type is identified and named explicitly. Naming the type is not merely taxonomic — it determines the appropriate repair operation in Stage 4. Where the Edge Taxonomy is operative, naming the edge-type misattribution is equally important: it distinguishes cases requiring topological repair from cases requiring edge-type negotiation. `[STABLE]`

**3e — Stage 4: Targeted Repair** `[STABLE]`

**3e.1** Each divergence type calls for a distinct topological operation:

- **3e.1i** *Anchor-Only Subgraph Repair (Generative Scaffolding)*: the transmitting party cannot hand over a missing cluster. They must map new edges outward from the receiver's existing structural subgraphs — building bridges from what the receiver already has toward the topological void — until the void is filled and functional. This is the most demanding repair operation and the one that most requires Polyphonic Encoding: a single scaffold path is likely to fail; multiple independent scaffold paths increase the probability that at least one takes hold in the receiving covenant.
- **3e.1ii** *Edge Divergence Repair (Local Alignment)*: the parties make explicit the different edge-structures each covenant associates with the shared label, identify which differences are operationally significant for the current transmission, and negotiate a local edge-alignment sufficient for the transmission's purposes. This does not require one party to permanently adopt the other's topology — only to model it accurately for the duration of the exchange.
- **3e.1iii** *Edge-Type Misattribution Repair (Type Declaration)*: the parties explicitly name the edge-type each is operating with, identify where the types diverge, and negotiate a working type-assignment sufficient for the transmission's purposes. This is a JIT-OM operation applied at the edge-type level rather than the concept-type level.
- **3e.1iv** *Temporal Drift Repair (Archival Reconstruction)*: the encoding party's earlier state, reconstructed via documentation or the Temporal Stranger protocol (Section 6c), must be consulted to re-establish the original *t₁* edge-structure. The receiver must then distinguish between what has drifted and what was originally transmitted.

**3e.2** Repair operations do not aim at permanent covenant merger. The goal is a locally calibrated comosí — sufficient for the transmission at hand, explicitly acknowledged as bounded, and not assumed to generalize beyond the established domain. `[STABLE]`

**3f — Stage 5: Irreducibility Declaration** `[STABLE]`

**3f.1** If localization reaches the Axiomatic layer and the divergence survives all repair attempts — including mandatory Polyphonic Encoding of the axiomatic claims in question — an Irreducibility Declaration is issued: a formal acknowledgment that the divergence is not a transmission failure but a genuine difference in foundational commitments.

**3f.2** The Irreducibility Declaration has significant practical consequences: `[PROVISIONAL]`

- **3f.2i** It redirects the conversation from repair toward negotiation — the question shifts from "how do we understand each other" to "how do we coexist given that we do not and cannot fully understand each other."
- **3f.2ii** It prevents the corrosive cycle of arguments that persist not because resolution is impossible but because the parties have not distinguished miscommunication from genuine value conflict. This is the GMRTI's primary contribution to the GMCR.
- **3f.2iii** It is the entry point for the GMCR properly speaking.

**3f.3** The Irreducibility Declaration is itself provisional and revisable. New conceptual tools, new bridge-concepts, or new Polyphonic Encoding approaches introduced after the declaration may dissolve what appeared irreducible. The declaration marks a current epistemic limit, not a permanent metaphysical fact. `[STABLE][RECURSIVE]`

**3g — Stopping Principle and Cost Control** `[STABLE]`

**3g.1** Recursive refinement is not meant to continue indefinitely. A GMRTI process should stop when the expected epistemic gain from one more cycle falls below the DRC-adjusted cost of continuing.

**3g.2** This principle is not a retreat from rigor. It is a way of preserving rigor against self-consuming refinement. A framework that can never say "enough for now" becomes indistinguishable from a framework that cannot act. `[STABLE]`

**3g.3** The stopping principle is especially important in low-DRC domains, where over-explication can destroy the very coordination it aims to improve. In those domains, the goal is not maximal reconstruction depth; it is sufficient reconstruction with minimal friction. `[PROVISIONAL]`
