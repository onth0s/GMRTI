## SECTION 1 — The Problem the GMRTI Addresses

### 1a — The Fundamental Transmission Problem
`[PLAIN]` Every idea lives inside the person who had it. Moving it to someone
else is not copying — it is reconstruction. The receiver has to rebuild your
idea from the signals you send, using their own inner dictionary, which is never
quite the same as yours.

**1a.1** Every idea `[->structural]` exists, in its original working form, as a
    configuration of relations `[->structural]` within a semantic covenant.
    `[STABLE]`

**1a.2** Distinct experiential histories `[->causal]` produce non-identical
    semantic covenants; no two semantic covenants are identical, because each is
    the product of a unique sequence of experience, reflection, and linguistic
    inheritance accumulated over time. `[STABLE]`

**1a.3** Transmission of an idea from one covenant to another `[->inferential]`
    requires *reconstruction* (signal decoding `[->procedural]` edge mapping) by
    the receiving covenant: building an approximation of the original
    configuration using only the signals available at the boundary between
    covenants: language, gesture, symbol, artifact. `[STABLE]`


**1a.4** The signals available at that boundary are themselves ambiguous,
    because the symbols used to encode an idea within one covenant carry no
    guarantee of identical decoding within another. This is the metaagnostic
    condition applied to communication. `[STABLE]`

**1a.5** All apparent understanding is therefore a *comosí*: a functional
    overlap sufficient for practical coordination within a bounded domain, but
    not a guarantee of semantic identity. The comosí may hold perfectly within
    its established domain and collapse entirely when conditions change.
    `[STABLE]`

```diagram LR
TITLE: The Fundamental Transmission Boundary
CT["Transmitting Covenant C_T — Semantic configuration"]
SIG["Ambiguous Surface Signal S — Language, gesture, artifact"]
CR["Receiving Covenant C_R — Reconstruction under metaagnosticism"]
COM("Comosí — Functional overlap within bounded domain")
CT -->|encodes| SIG
SIG -->|reconstructed by| CR
CR -->|yields| COM
```

```mirror probe
TITLE: Comosí vs. Semantic Identity
TARGET: [[1a — The Fundamental Transmission Problem]]
PROBE: When two covenants achieve a stable comosí in everyday coordination, what has actually been established?
[ ] Both covenants now hold identical internal edge-topologies for the shared terms. --> That confuses practical overlap with structural identity (§1a.5).
[x] Their distinct topologies overlap functionally enough for the current bounded domain, without guaranteeing identity if conditions shift. --> Exact: comosí is bounded functional sufficiency, not topological identity.
[ ] They have eliminated semantic entropy to zero across all contexts. --> Metaagnosticism rules out zero absolute entropy (§1a.4).

AUTHOR: Comosí is functional sufficiency within a bounded domain, not guaranteed identity of underlying edge-structure.
DIVERGENCE: Treating comosí as identity leaves both parties blind when novel boundary conditions expose hidden divergence.
```

- **1a.5i — The Commercial Purchase Allegory** `[ALLEGORY: COMOSÍ]` A customer
    walks into a corner shop and buys a loaf of bread. She hands over the
    asked-for bills and walks out with the bread. Everything goes smoothly,
    even if the two people have completely different ideas about what "money"
    or "fairness" really means. Because their words and actions fit together
    well enough for buying bread, it works *as if*
    ([[Comosí|comosí]])
    they shared the exact same [[Semantic Covenant|inner dictionary]].
- **1a.5ii — The Living Room vs. Art Gallery Allegory**
    `[ALLEGORY: COMOSÍ-BOUNDARY]` Two friends in a living room easily agree on
    what is a "painting" (hung on the wall) and what is a "sculpture" (placed
    on a shelf). At home, their meanings match well enough for everyday
    conversation ([[Comosí|comosí]]). Later that afternoon, they
    visit a modern art museum where paintings sit on the floor and sculptures
    hang from the ceiling. Suddenly they argue over which is which — showing
    that their definitions only seemed identical inside the living room, until
    conditions changed and exposed the hidden
    [[Divergence|divergence]].

**1a.6 — Semantic Entropy as the Adversarial Target** `[STABLE]`

`[PLAIN]` The more ways a message can be misread, the higher its "confusion
score." The GMRTI's main job is to lower that score — not to zero, which is
impossible, but low enough for the task at hand.

The fundamental transmission problem can be restated precisely using the concept
of Semantic Entropy. A transmission event begins with the transmitter encoding a
semantic configuration — a specific topological region of their covenant — into
a surface signal. That signal reaches the receiver carrying high semantic
entropy: many non-identical edge-configurations in the receiving covenant remain
compatible with what was transmitted. The receiver selects one of these
configurations — typically without awareness that selection is occurring — and
treats it as the transmitted content.

We formalize Semantic Entropy $H_s(S)$ of a consistent surface signal $S$
relative to a receiving covenant as the log of the number of distinct functional
equivalence classes $[G_R]$ compatible with $S$ without contradiction
($|\{[G_R]\}| \ge 1$; an empty set $|\{[G_R]\}| = 0$ denotes **Signal
Contradiction / Unsatisfiability**, not zero entropy; under the §8b.1 quotient,
a class $[G_R]$ is compatible with $S$ iff at least one representative $G \in
[G_R]$ satisfies $S$): $$H_s(S) = \log_2
|\{[G_R] : [G_R] \text{ is compatible with } S\}|$$ Because direct measurement
of $H_s(S)$ is constrained by metaagnosticism, we operationalize it via the
**Behavioral Convergence Proxy (Path-Count Metric)**: the number of independent
Polyphonic Encoding paths that must be successfully reconstructed and verified
by the receiver before they reach the Operational Action Threshold [provisional
dependency boundary: §3c.3, §8b.1]. For a single pair of covenants $(C_T, C_R)$,
this path count measures pairwise reconstruction divergence (analogous to
cross-entropy), not intrinsic signal entropy directly: if each independent
non-void path also exhibits *filtering independence* over rival equivalence
classes (contracting the compatible class space by a factor $k > 1$, which
topological route-independence alone does not guarantee), the required path
count scales as $O(H_s(S) / \log_2 k)$, whereas correlated paths or a path
hitting an Anchor-Only Subgraph yield fewer bits and receiver-specific local
voids or lucky comosí confound the count (making the metric an upper-bound
proxy). The metric converges to an
estimator of $H_s(S)$ only when evaluated under the zero-charity Minimal
Substrate posture (DRC → 1.0) along combined Path-Stripping Probes (§2f.5iv).
Thus, a high path count under those conditions indicates high initial semantic
entropy.

The GMRTI's central purpose is the controlled reduction of semantic entropy:
progressively constraining the space of consistent receiving-covenant
configurations until the residual divergence is either negligible for the
transmission's purposes, or explicitly locatable and typeable when it is not.
This is not entropy elimination — metaagnosticism establishes that as
unachievable — but entropy management: bringing the receiving covenant's
configuration into a neighborhood of the transmitting covenant's configuration
that is close enough for the work at hand.

This framing clarifies why natural language's high-entropy character is not
merely a stylistic inconvenience. Natural language is expressive precisely
because it is high-entropy: a word can mean many things to many covenants. This
is generative for poetry, metaphor, and creative connotation. It is structurally
dangerous for transmission of concepts whose downstream operational consequences
diverge sharply depending on which configuration the receiver selects. The GMRTI
does not propose to replace natural language's expressive entropy with formal
poverty. It proposes to selectively reduce entropy for the nodes and edges that
matter most in a given transmission context, leaving expressive richness intact
elsewhere. `[STABLE]`

```mirror probe
TITLE: Signal Contradiction vs. Zero Entropy
TARGET: [[1a — The Fundamental Transmission Problem]]
PROBE: What does |{[G_R]}| = 0 signify in the Semantic Entropy model?
[ ] Zero semantic entropy (perfect univocal transmission). --> Zero entropy corresponds to |{[G_R]}| = 1, a single compatible class.
[x] Signal Contradiction / Unsatisfiability — no receiving configuration is consistent with the signal. --> Correct: an empty compatible set is contradiction, not clarity.
[ ] An Anchor-Only Subgraph with no internal edges. --> Anchor-Only Subgraphs still admit many compatible completions.

AUTHOR: H_s(S) = 0 requires |{[G_R]}| = 1; an empty set |{[G_R]}| = 0 denotes Signal Contradiction / Unsatisfiability (§1a.6).
DIVERGENCE: Conflating 0 compatible topologies with 0 bits of ambiguity mistakes contradiction for precision.
```


### 1b — Why This Problem Is Not Merely Academic
`[PLAIN]` Misunderstanding is not just uncomfortable — it is dangerous at scale.
When people think they agree but actually don't, no amount of good intentions
will stop the plan from falling apart at the worst possible moment.

**1b.1** If transmission is always approximate and the degree of approximation
    is in principle unknowable without deliberate investigation, then:
    `[STABLE]`

- **1b.1i** Arguments that appear to be about substantive disagreements may in
    fact be about undetected transmission failures — the parties disagree about
    words, not things, without knowing it.
- **1b.1ii** Agreements that appear genuine may rest on comosí overlaps that
    will collapse under novel conditions, producing unexpected conflict
    precisely when coordination is most needed.
- **1b.1iii** Knowledge accumulated within one community may be effectively
    inaccessible to another not because it is hidden, but because the
    transmission medium — shared language, shared conceptual scaffolding — is
    insufficient to carry it.

**1b.2** These failure modes scale. At the individual level they produce
    miscommunication. At the community level they produce ideological
    fragmentation. At the civilizational level they produce the coordination
    failures that constitute the GMRTI's ultimate target domain. `[PROVISIONAL]`

**1b.3** The GMRTI's foundational thesis: a systematic method for locating and
    repairing transmission failures is a prerequisite for any General Method for
    Conflict Resolution, because without it, conflict resolution cannot
    distinguish genuine value disagreements from resolvable miscommunication.
    `[STABLE]`

### 1c — The Three Transmission Modes `[STABLE][RESTORED]`

`[PLAIN]` Misunderstanding happens across three scales: talking to your own
future self through old notes ([[Temporal Stranger]]), talking to another person
right now, and translating ideas between whole communities ([[Federated
Graph]]). The GMRTI starts with notes to yourself first because it is the safest
place to practice before scaling up.

The GMRTI must address transmission across three structurally distinct modes
with a single unified algorithmic skeleton:

**1c.1 — Self-to-Future-Self Transmission** A thinker at time *t₁* attempts to
transmit an idea to their own future state at time *t₂*. The primary failure
mode is Temporal Drift Divergence: the author's covenant has changed between
encoding and decoding such that the originally intended edge-structure is no
longer recoverable from the encoded signal. The Temporal Stranger
operationalization (Section 6c) directly addresses this mode. This mode is
established as the canonical baseline sandbox for the first implementation
(v0.9) under the practice of **Self-Annotation**.

**1c.2 — Self-to-Other Transmission** A thinker attempts to transmit an idea to
a contemporaneous other. This is the classical communication problem, understood
metaagnostically: as reconstruction across covenant difference rather than
transfer of identical content.

**1c.3 — Community-to-Community Transmission** A community's accumulated
knowledge, values, or frameworks is transmitted to another community with a
different collective covenant. This is the problem of ontological translation —
the target community may lack not just the words but the conceptual
infrastructure to receive the transmission. The Federated Graph model (Section
2d) addresses this mode's structural complexity [provisional dependency
boundary: §2d].

**1c.4 — Developmental Ordering** To prevent over-generalization and manage
cognitive overhead, the GMRTI mandates a strict developmental ordering:
Self-Annotation (Self-to-Future-Self) serves as the initial sandbox to generate
and test conceptual primitives; Community-to-Community (Constitutional Drafting)
[provisional dependency boundary: §2d] then formalizes these primitives; which
are subsequently simplified for real-time Self-to-Other dialogue (GMRTI-Mediated
Dialogue). The framework's operational complexity is scoped accordingly: v0.9
targets Self-Annotation only, where the cognitive overhead is borne by a single
practitioner with full access to their own covenant. Scaling to real-time
dialogue requires a simplified subset whose specification is deferred until the
Self-Annotation validation is complete.

```table
TITLE: Three Transmission Modes & Developmental Ordering
| Mode | Primary Failure Risk | Operationalization | v0.9 Scope |
|---|---|---|---|
| Self-to-Future-Self (§1c.1) | Temporal Drift Divergence | [[Temporal Stranger]] / Self-Annotation | Canonical Sandbox |
| Community-to-Community (§1c.3) | Ontological / Anchor Deficit | [[Federated Graph]] & [[Artifact Anchor]] | Formalization Target |
| Self-to-Other (§1c.2) | Reconstruction Divergence | GMRTI-Mediated Dialogue | Deferred Subset |
```
