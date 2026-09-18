# DISSONANCE — Adversarial Audit of GMRTI v0.9 Candidate

**Target revision:** GMRTI — General Method for Refinement and Transmission of
Ideas, Tenth Iteration (v0.9 Candidate), compiled monolith.

**Auditor posture:** Mirror Mode per §3c.1i. Interpretive charity suspended.
Claims are evaluated against the text as written, not against the most
charitable reconstruction available. Where a defect could be an artifact of the
compilation step (`rewrite.py`) rather than the modular sources, this is stated
explicitly.

**Scope limitation:** This audit was performed against the compiled monolith
only. `src/`, `refinery/`, `GLOSSARY.md`, `PEBBLE.md`, `ARCHITECTURE.md`,
`METHODOLOGY.md`, and `REFINEMENT.md` were not inspected as separate artifacts.
Findings marked `[COMPILATION?]` may not reproduce in the modular sources.

**Audit intent per §6b.2:** surface Anchor-Only Subgraph and Edge Divergence
failures that a charitable reader would paper over. Per §6b.3, this audit is
more reliable for failures of *transmission* than failures of *conception*; per
§8b.2, Mirror-Prior Synchronization is an unmitigated risk in this audit, since
the auditing agent shares broad training priors with prior iterations' auditors.
Per §6b.4, no finding in this document recommends compression as such; where
excision is recommended it is on grounds of orphanhood or falsity, not length.

---

## Summary of Findings

| ID | Finding | Severity | Marker conflict |
|---|---|---|---|
| D-01 | DRC scale carries three mutually incompatible semantics | Critical | `[STABLE]` × `[STABLE]` |
| D-02 | Core Path Minimization contradicts Polyphonic Encoding's independence requirement | Critical | `[STABLE]` × `[STABLE]` |
| D-03 | Relational Operator Vocab Terminus contradicts the Covenant Zero Protocol | Critical | `[STABLE]` × `[STABLE]` |
| D-04 | §8b.1 misquotes the Semantic Entropy formula it audits | Major | — |
| D-05 | Damping Factor "Convergence Theorem" does not follow from its update rule | Major | `[STABLE]` |
| D-06 | PSP pre-screening criterion reintroduces the circularity it breaks | Major | `[STABLE]` |
| D-07 | Proactive Chaotic Probing scheduled in the wrong DRC mode | Major | derivative of D-01 |
| D-08 | Four `[STABLE]` glossary terms are orphans with zero body occurrences | Major | — |
| D-09 | Refinery has no presence in the compiled monolith | Major | `[COMPILATION?]` |
| D-10 | Syntactic Edge-Forcing prototype is displayed, not deployed | Major | `[STABLE]` |
| D-11 | Content–Protocol Stratification stops regress by fiat, using the move §5b.1 rejects | Major | `[STABLE]` × `[STABLE]` |
| D-12 | Self-application claim of the epigraph has no completed instance | Major | `[PROVISIONAL]` |
| D-13 | `[PROVISIONAL]` claims carrying `[STABLE]` structural load | Moderate | — |
| D-14 | Operational Action Threshold used pervasively, absent from §0.4 | Moderate | — |
| D-15 | Cross-reference errors (§0.1, §8b.1) | Minor | — |
| D-16 | Heading-level collision and missing addresses for governance artifacts | Minor | `[COMPILATION?]` |
| D-17 | Governance material precedes the problem statement in monolith order | Minor | `[COMPILATION?]` |
| D-18 | `specs/` announced in §0.1, absent from README TOC | Minor | — |
| D-19 | §3b.1v excision marker occupies a live address | Minor | — |

---

## Tier 1 — Invariant Violations

Per `METHODOLOGY.md`, a `[STABLE]` claim is a formal invariant, and any refactor
breaking one without deliberately invoking the Refinement Cycle is an error.
Each finding in this tier is a case of two `[STABLE]` claims breaking each
other, which means the invariant set is currently inconsistent and no further
`[PROVISIONAL]` → `[STABLE]` graduation should proceed until they are resolved.

### D-01 — The DRC scale carries three mutually incompatible semantics `[CRITICAL]`

**Sites:** §0.4 (DOMAIN RISK COEFFICIENT), §2e.5 closing line, §0.4 (MINIMAL
INTELLIGIBILITY BOOTSTRAP), §3a.4, §3c.2, §8a.2. All `[STABLE]` except §8a.2's
containing subsection, which is also `[STABLE]`.

**Reading 1 — §0.4 and §3c.2.** DRC governs required precision of reconstruction
and is *inversely proportional to interpretive charity*. High-DRC domains
(aviation, surgery, law, formal logic) drive charity toward zero and sustain the
Mirror posture. Low-DRC domains (casual dialogue, arts) maximise charity. **DRC
up → charity down.**

**Reading 2 — §3a.4.** Generative Mode: "DRC is calibrated to infinity, enabling
maximum interpretive charity." Audit Mode: "DRC is calibrated to absolute zero.
Interpretive charity is suspended." **DRC up → charity up.** Exact inverse of
Reading 1.

**Reading 3 — §2e.5 and the MIB glossary entry.** "Calibrating the DRC to zero
reduces interpretive charity to the Minimal Substrate baseline." Agrees with
Reading 2 at the zero pole, contradicts Reading 1.

**Compounding range inconsistency.** §3a.4 places Refinement Mode at DRC = 0.5
and §8a.2 uses 0.9 (catastrophic liability) and 0.1 (exploratory dialogue) — a
bounded [0,1] scale. §3a.4's own poles are ∞ and 0 — unbounded. A single
parameter cannot carry both ranges.

**Propagated operational consequence.** §3e.1v mandates, under Meta-DRC
Divergence, "defaulting to the highest demanded DRC of any participating
covenant... to prevent asymmetric risk failure." Under Reading 1 this correctly
selects maximum rigour. Under Readings 2 and 3 it selects **maximum charity** —
the protocol designed to prevent catastrophic asymmetric coordination failure
would systematically choose the least rigorous posture available. §8a.2's entire
Epistemic Asymmetry Boundary argument likewise inverts.

**Recommended resolution.** Ratify Reading 1 as canonical: it is the glossary
definition, it is what §3c.2's worked domains require, and it is what §3e.1v and
§8a.2 depend on for coherence. Then repair:

- §3a.4 — Generative Mode becomes DRC → minimum; Audit Mode becomes DRC →
  maximum. Fix the range to [0,1] throughout and drop "infinity."
- §2e.5 closing line — "Calibrating the DRC to maximum reduces interpretive
  charity to the Minimal Substrate baseline."
- §0.4 MIB entry — same correction.
- §2f.5v PCP scheduling — see D-07.

This is a Structural-layer repair touching five `[STABLE]` sites. It requires a
full REP cycle, not a patch.

---

### D-02 — Core Path Minimization contradicts Polyphonic Encoding `[CRITICAL]`

**Sites:** §0.4 (POLYPHONIC ENCODING), §2f.1, §2f.2, §2f.5iv, §2f.6. All
`[STABLE]`.

**The conflict.** §0.4 and §2f.1 define Polyphonic Encoding as multiple
**structurally independent** edge-paths to the same semantic destination. §2f.2
grounds the mechanism explicitly in independence: since no single path is
guaranteed to survive reconstruction in an unknown receiving covenant, encoding
via multiple independent routes raises the probability that at least one arrives
intact.

§2f.6 then mandates Core Path Minimization: "all redundant encoding paths must
be direct structural translations (**isomorphisms**) of a single declared
canonical path."

Isomorphic translations of one canonical path are by construction not
structurally independent — they share the canonical path's topology, which is
what isomorphism asserts. §2f.6 therefore forbids the property §2f.1 requires
and §2f.2 relies on.

**Propagated diagnostic failure.** §2f.5iv's Path-Stripping Probing operates by
disabling all but one path and checking whether reconstruction still clears the
Operational Action Threshold. If every path is an isomorph of the canonical
path, stripping to any single path yields a structurally identical
reconstruction. PSP then either always passes or always fails and localises no
voids. The framework's primary defence against Redundancy-Masking is nullified
by its own complexity governor.

**Internal counter-evidence.** §2f.3ii's pedagogy example — definition, concrete
example, analogy, Socratic elicitation — describes four routes with genuinely
disjoint machinery. §2f.3iii's legal-drafting example (definition, enumerated
inclusions, enumerated exclusions) likewise. Neither set is isomorphic in
§2f.6's sense. The document's own illustrations violate its own constraint.

**Candidate resolutions, in descending order of recommendation.**

1. **Split the requirement.** Require *destination-isomorphism* — all paths
   terminate at the same semantic destination and license the same downstream
   inferences — while explicitly requiring *route-independence*, that paths
   traverse disjoint intermediate regions. This preserves §2f.6's stated
   motivation (preventing surface-area expansion and semantic drift) without
   destroying independence. Both §2f.3 examples satisfy it.
2. **Narrow §2f.6 to a drift constraint.** Retain only the prohibition on
   introducing new concepts or unrelated semantic domains, and drop the
   isomorphism language, which is stronger than the stated motivation requires.
3. **Downgrade §2f.6 to `[PROVISIONAL]`** pending resolution.

---

### D-03 — Operator Terminus contradicts the Covenant Zero Protocol `[CRITICAL]`

**Sites:** §2e.5ii, §2e.5iii, §2g.4, §3e.1vi. All `[STABLE]` or within
`[STABLE]` subsections.

**The conflict.** §3e.1vi declares the eight primitive relational operators
Axiomatic Primitives, "structurally non-markable at the content level," and
states that "any divergence over the meaning of a relational operator **cannot
be repaired via JIT-OM**, but triggers immediate Cost-Bounded Termination
(3a.1iii) or defaults to classical natural language interpretation."

§2e.5iii defines the Covenant Zero Protocol as a procedure for *establishing*
three of those operators from the Minimal Substrate: `[->causal]` via pairing
physical signals with temporal co-occurrence, `[->inferential]` via pattern
co-occurrence and logical consistency checks, `[->identity]` via signal
substitution.

If CZP can bootstrap an operator from nothing, divergence over that operator is
repairable by re-running CZP against it. §3e.1vi's "cannot be repaired" is false
for at least three of the eight.

**Secondary gap — incomplete bootstrap.** CZP establishes 3 of 8 operators.
`[->procedural]`, `[->normative]`, `[->referential]`, `[->affective]`, and
`[->structural]` have no bootstrap path, yet §2e.5ii declares all eight
constitutive of the Primitive Covenant. Either CZP is incomplete and should
carry `[OPEN]`, or the Primitive Covenant should be narrowed to the three
bootstrappable operators, with the remaining five introduced as derived types
via JIT-OM.

**Structural observation.** §3e.1vi's termination response is also operationally
brittle in the case the framework most needs to survive: cross-covenant
transmission where operator meanings have not yet converged is the *normal*
starting condition for Community-to-Community transmission (§1c.3), and
immediate termination there forecloses precisely the work §7b claims as the
framework's civilizational contribution.

**Recommended resolution.** Reframe §3e.1vi as a *regress* terminus rather than
a *repair* terminus: operators are non-markable at the content level (no
meta-tagging of tags), but operator divergence is repaired by re-running CZP,
not by termination. Termination is then reserved for the case where CZP itself
fails — which is a genuine Minimal Substrate failure and correctly terminal.

---

## Tier 2 — Formal Defects in `[STABLE]` Claims

### D-04 — §8b.1 misquotes the Semantic Entropy formula `[MAJOR]`

**Sites:** §0.4 (SEMANTIC ENTROPY), §1a.6, §8b.1.

§0.4 and §1a.6 both define semantic entropy as a Hartley-style log-count over
compatible configurations:

`H_s(S) = log_2 |{G_R : G_R compatible with S}|`

No probability distribution is involved, deliberately — §1a.6 states that direct
measurement is constrained by metaagnosticism and therefore operationalises via
the Behavioral Convergence Proxy (Path-Count Metric).

§8b.1 states: "The mathematical formulation of Semantic Entropy in Section 1a
(`H_s = -Σ p_i log_2 p_i`) defines entropy over the distribution of
reconstructed meanings."

That is Shannon entropy over a distribution and is **not what §1a says**. The
contention then worries whether `p_i` can be metricized without arbitrary
subjective partitioning — a problem the document's actual formulation was
designed to avoid by counting configurations rather than weighting them.

**Consequence.** Contention 1 is either auditing a formula absent from the
    document, or silently proposing a Shannon upgrade without declaring it as a
    proposal. Neither is acceptable in an `[OPEN]`-tracking section.

**Recommended replacement contention.** The live problem in the stated
formulation is different and sharper: the log-count presupposes an individuation
criterion for "non-isomorphic edge-configurations," and that criterion is itself
covenant-relative. Counting compatible configurations requires a partition of
configuration-space, and who partitions is exactly the metaagnostic question.
This is recursive in the sense §0.3 `[RECURSIVE]` intends and is a better
Contention 1 than the current text.

**Also:** §8b.1 cites §2f.4 for the path-count proxy. The proxy is defined at
§0.4 and §1a.6; §2f.4 concerns depth-layer asymmetry. See D-15.

---

### D-05 — The Damping Factor "Convergence Theorem" does not follow `[MAJOR]`

**Site:** §4b.3, `[STABLE]`.

Stated update rule: `A_{t+1} = A_t + λ(A_decl − A_t)`, with λ < 1.0, typically
0.15.

Stated theorem: "Under any bounded correction stream, the anchor trajectory
converges to a stable equilibrium state if the sum of update magnitudes is
finite: `Σ|v_t| < ∞`."

**Four defects.**

1. **`v_t` does not appear in the update rule.** The prose introduces
   "correction vector updates `v_t`" as the quantity scaled by λ; the displayed
   equation scales `(A_decl − A_t)`. These are distinct objects unless
   `v_t ≡ A_decl − A_t`, which is nowhere stated.
2. **The stated condition makes λ idle.** If `Σ|v_t| < ∞`, the trajectory is
   absolutely convergent by summability alone — the partial sums are Cauchy
   irrespective of damping. The theorem gives λ no work, which vacates the
   axiom's own stated motivation ("to prevent anchor oscillation and guarantee
   mathematical convergence").
3. **Boundedness and summability are conflated.** The sentence asserts
   convergence "under any bounded correction stream" and then conditions on a
   finite sum. A bounded stream need not be summable (`v_t = c` for all `t` is
   bounded, not summable), and under a constant non-zero stream the recursion
   does not converge to a fixed point — it tracks with lag.
4. **The target is not fixed.** The recursion is standard exponential
   smoothing, `A_{t+1} = (1−λ)A_t + λA_decl`, which converges geometrically to
   `A_decl` **when `A_decl` is constant**. The premise of Dynamic Re-Anchoring
   is that declarations keep arriving, so `A_decl` is a sequence. The relevant
   result is a tracking-error result, not a convergence result.

**Recommended resolution.** Restate as a `[PROVISIONAL]` smoothing heuristic
with an explicit responsiveness/stability tradeoff. Under drift rate δ per step,
steady-state lag under exponential smoothing is on the order of `δ(1−λ)/λ`,
which correctly frames λ as a *choice* rather than a guarantee. Remove the word
"Theorem" until one is proved. The value λ = 0.15 is currently presented as
"typically" with no empirical or analytic basis; either source it or mark it as
an arbitrary starting value subject to calibration, as the Dependency-Tracing
Scan's 30% threshold is marked in §0.4.

---

### D-06 — PSP pre-screening reintroduces the circularity it breaks `[MAJOR]`

**Site:** §2f.5iv (Polyphonic Node Detection), `[STABLE]`.

§2f.5iv correctly states the circularity: PSP needs to know which nodes are
legitimately polyphonic, but detecting polyphony requires the analysis PSP
provides. The proposed break: flag as a candidate polyphonic node "any node with
two or more incoming edges of distinct types *and* two or more outgoing edges of
distinct types."

**The criterion depends on edge-type information that is unavailable when it is
needed.** §2a.5's Taxonomy Switching Rule puts the framework in Tier 1
(Inferential / Causal / Other) by default during Covenant Declaration. §3b.1v
explicitly excises edge-typing from Stage 1, deferring it entirely to Stage 3.
Tier 2's eight types activate locally via JIT-OM, triggered *only* on detected
Edge-Type Misattribution.

So: candidate-node pre-screening requires typed edges → typed edges require
JIT-OM activation → JIT-OM activation requires detected divergence → and PSP
exists to detect divergence that standard detection misses. The criterion is
inoperable precisely when needed. Additionally, under Tier 1 most edges will be
typed "Other," collapsing the "two or more of distinct types" test to a near-
constant negative.

**Recommended resolution.** Define a Tier-1-runnable structural pre-screen —
in-degree ≥ 2 and out-degree ≥ 2, ignoring types — as the default, and reserve
the type-sensitive criterion for regions where Tier 2 is already active. The
structural variant is weaker (more false candidates) but actually executable,
and over-flagging is the safe direction given that flagged nodes merely receive
a strengthened threshold rather than an exemption.

---

### D-07 — Proactive Chaotic Probing is scheduled in the wrong mode `[MAJOR]`

**Site:** §2f.5v, `[STABLE]`. Derivative of D-01.

PCP is prescribed to run "during generative states (low DRC)." Under the
canonical §0.4/§3c.2 semantics, low DRC means maximum interpretive charity with
minor divergences treated as noise. This schedules the framework's most
sensitive void-detection instrument for the mode in which sensitivity is
deliberately suppressed.

Under §3a.4's inverted semantics the prescription reads correctly — which is
useful evidence that D-01's inconsistency has already propagated into
operational prescriptions and is not merely a definitional untidiness.

**Recommended resolution.** Resolve D-01 first, then restate PCP's scheduling in
terms of the *mode name* (Generative Mode / Refinement Mode / Audit Mode) rather
than a bare DRC value, so the prescription is robust to future scale revisions.
Note that the substantive question — whether chaotic probing belongs in drafting
(cheap, low stakes, catches drift early) or in audit (expensive, high
sensitivity) — is a real design decision that the DRC confusion has been
obscuring. It should be decided on its merits, not inherited.

---

## Tier 3 — Completeness and Self-Application

### D-08 — Four `[STABLE]` glossary terms are orphans `[MAJOR]`

The following §0.4 entries have **zero occurrences anywhere in Sections 1–8**.
Verified by full-text search of the compiled monolith; these are not passing
mentions but total absences.

| Term | Marker | Body occurrences |
|---|---|---|
| Topological Consistency Audit | `[STABLE]` | 0 |
| Dependency-Tracing Scan (incl. 30% threshold, "Axiomatically Active") | `[STABLE]` | 0 |
| Periodic Re-Mirroring Protocol | `[STABLE]` | 0 |
| Bad Actors (threat model) | — | 0 (appears only inside the TCA glossary line) |

This is more serious than ordinary orphan-definition untidiness, for three
reasons.

**An entire adversarial threat model exists only in the glossary.** Bad Actors —
participants who declare inconsistent subgraphs or reject isomorphic repairs —
appear nowhere in the algorithm. §§3b–3f assume good-faith participants
throughout: Covenant Declaration assumes willingness to make architecture
visible, Generative Reconstruction assumes honest divergence reporting, Targeted
Repair assumes good-faith negotiation, and Irreducibility Declaration assumes
neither party is manufacturing irreducibility to foreclose repair. A framework
whose ultimate target domain is civilizational conflict (§7b) with no body-level
treatment of adversarial participants has a substantial hole, and the glossary
entry makes it appear filled. This is itself an Anchor-Only Subgraph in the
reader's covenant: a shared surface label with zero relational depth behind it.

**Dependency-Tracing Scan is the only operational criterion offered anywhere for
identifying Axiomatic Edge-Clusters.** §2b states that axiomatic clusters have
topological dependency approaching infinity and are "rarely explicit — usually
invisible to their holder until extreme divergence pressure surfaces them."
§3d.2iii makes reaching the Axiomatic layer the gate for Irreducibility
Declaration; §3f.2iii makes that declaration the entry point to the GMCR. The
framework's most consequential decision procedure therefore rests on a detection
method that exists only as a glossary line with an admittedly uncalibrated
default threshold.

**Periodic Re-Mirroring is the stated defence against Artifact Anchor decay**,
which §2d.3 identifies as the mechanism by which institutions fail silently
while all members believe they understand each other. §2d.2 introduces the
Maintenance Covenant but never names the protocol.

**Recommended resolution.** For each of the four, choose explicitly: promote to
a body subsection with worked operational content, or remove from §0.4 and
record the deferral in §8. Leaving `[STABLE]` definitions with no home violates
§0.4's own framing (terms that "carry precise technical meaning throughout this
document") and, per §8c.1, lets unresolved work masquerade as stable invariant.
Bad Actors / TCA is the highest-value promotion; it is also the largest, and
deferring it to v1.1 with an explicit §8 entry would be defensible.

---

### D-09 — The Refinery has no presence in the compiled monolith `[MAJOR]` `[COMPILATION?]`

§6b.1 step 5 mandates, as part of every Irreducibility Check, "a
length-and-redundancy audit of all Refinery entries, since Refinery compression
is a confirmed failure mode." §6b.4 cites the empirical v0.6 loss of Refinery
entries R2–R4 as the confirming instance and instructs that "any reduction in
Refinery entry length" be flagged as requiring explicit justification. The
README links `refinery/`.

The compiled monolith contains no Refinery section. A reader or auditor working
from the monolith — which is the artifact this audit was handed, and which
`rewrite.py --check` treats as the canonical compiled form — cannot perform the
audit the monolith itself mandates.

**Recommended resolution.** Either include `refinery/` in the `rewrite.py`
compilation, or amend §6b.1 step 5 to state that the Refinery audit operates on
modular sources outside the compiled artifact. The first is preferable: §6b.4
establishes Refinery compression as a *confirmed* failure mode, and an audit
step that the primary artifact cannot support is an audit step that will be
skipped.

---

### D-10 — The Syntactic Edge-Forcing prototype is displayed, not deployed `[MAJOR]`

**Sites:** §0.1 item 3, §2g.7, and the in-situ text of §1a.1, §1a.2, §1a.3,
§2a.2.

§2g.7 claims: "As a working prototype, key stable claims in this treatise **are
formally edge-forced** as follows," then lists edge-forced restatements of four
claims.

The four claims **as they appear in Sections 1 and 2 carry no operators**. The
edge-forced versions exist only inside §2g.7's list. The treatise therefore
contains four edge-forced sentences *about* four claims, not four edge-forced
claims.

**Why this is not a nitpick.** §2g.2 defines the mechanism as one where edge
traversal "is not optional — it is load-bearing in the very act of
comprehension." A reader encountering §1a.1 in situ decodes it as ordinary
prose; the forcing is absent at the site where it would do its work. §0.1 item
3's claim to have "prototyped Syntactic Edge-Forcing (§2g)" overstates what was
implemented, and §2g.7's "are formally edge-forced" is false as written.

**Recommended resolution, two options.**

1. Annotate the four claims in situ and reduce §2g.7 to a pointer. This makes
   the claim true and produces a genuine, if small, deployment.
2. Amend §2g.7 to: "are restated in edge-forced form below as a notational
   demonstration; in-situ deployment is deferred." Cheaper, honest, and
   consistent with §8c.1's principle that open work be marked rather than
   asserted.

Option 1 is preferable if v0.9 is to claim the prototype at all.

---

### D-11 — Content–Protocol Stratification stops the regress by fiat `[MAJOR]`

**Sites:** §5b.1 `[STABLE]`, §3e.1 Content–Protocol Stratification `[STABLE]`.

§5b.1 argues that upfront metalanguage creates infinite regress "because the
metalanguage used to classify concepts is itself subject to the same
transmission failures it was designed to prevent." This argument is the
justification for JIT-OM, one of the framework's three core mechanisms.

§3e.1's Content–Protocol Stratification declares a closed six-term
meta-vocabulary — propose, accept, reject, pause, resume, default — "operating
at a single declared meta-level above the content layer," concluding: "no
further meta-level is **required or permitted**."

"Permitted" is a stipulation, not an argument. The six meta-operations are
natural-language terms and therefore carry semantic entropy by §1a.6
(`[STABLE]`). Two parties can diverge on "accept" (provisional acceptance?
acceptance with reservation? acceptance of the repair versus acceptance of the
re-typing?) or on "default" (immediately, or after a negotiation window?).
Repairing that divergence requires discussing the meta-vocabulary, which is
level 3 — prohibited by declaration.

This is structurally the same situation §5b.1 says fails. Either §5b.1's
anti-regress argument is too strong, in which case upfront metalanguage is
sometimes acceptable and JIT-OM's justification weakens; or §3e.1's terminus is
unjustified. Both currently hold `[STABLE]`.

**Most promising resolution.** Argue that the meta-vocabulary is *performative*
rather than descriptive: "I accept" does not describe a state whose
edge-structure could diverge, it enacts a move in a protocol, and its meaning is
exhausted by its role in a declared state machine. This is a real argument and
would genuinely halt the regress, but it must be *made* rather than asserted,
and it carries a prerequisite: the protocol state machine must be specified. The
document currently does not specify it — the six operations are listed but their
transitions, preconditions, and effects are not.

Note the structural parallel to D-03: both are regress-termination claims, and
both would be better served by a mechanism than by a prohibition.

---

### D-12 — The epigraph's self-application claim has no completed instance `[MAJOR]`

The frontispiece declares: "This document is itself a primary test case of the
GMRTI."

§6a.3 concedes (`[PROVISIONAL]`): "The current iteration asserts and partially
prototypes self-application (see 2g.7) but does not execute a complete
self-audit cycle."

Per D-10, the partial prototype §6a.3 points to is itself weaker than claimed.
The epigraph's assertion therefore has no completed instance behind it.

**Recommended resolution.** Execute one complete five-stage cycle — Covenant
Declaration, Generative Reconstruction, Divergence Localization, Targeted
Repair, Irreducibility check — on a single section, and publish the resulting
artifact alongside the treatise. §5 (Metalanguage and JIT-OM) is the highest-
value target, since D-11's contradiction lives there and a genuine self-audit
would have to confront it. This is the single most defensible thing to complete
before 1.0: it converts the document's central credibility claim from assertion
to demonstration.

---

### D-13 — `[PROVISIONAL]` claims carrying `[STABLE]` structural load `[MODERATE]`

Per `METHODOLOGY.md`, `[PROVISIONAL]` means the claim "has not yet survived a
full adversarial audit." The following `[PROVISIONAL]` claims are load-bearing
for `[STABLE]` structures:

- **§3c.3 Operational Action Threshold** `[PROVISIONAL]` — depended on by
  §3a.1i `[STABLE]` (Operational Parking termination), §2f.5iv `[STABLE]`
  (PSP's failure criterion), §1a.6 `[STABLE]` (the Path-Count Metric's
  terminus), and §3c.2 `[STABLE]`. This is the most significant instance: the
  framework's principal termination condition and its principal entropy proxy
  both bottom out in an unaudited definition.
- **§2c.2** `[PROVISIONAL]` — states the divergence taxonomy is "diagnostic,
  not exhaustive." §3e.1's repair operations `[STABLE]` are indexed
  exhaustively by that taxonomy, so a non-exhaustive taxonomy implies an
  undeclared gap in the repair catalogue.
- **§2d Federated Graphs** `[PROVISIONAL]` — §1c.3 routes Community-to-
  Community transmission here, and §1c.4 makes Constitutional Drafting the
  second mandated developmental stage. A `[PROVISIONAL]` section carries a
  mandated stage of the roadmap.
- **§3f.2 Irreducibility consequences** `[PROVISIONAL]` — §7a.1iii–iv
  `[STABLE]` makes the Irreducibility Declaration the GMRTI's primary
  contribution to the GMCR.

**Recommended resolution.** Add a dependency invariant to `METHODOLOGY.md`: no
`[STABLE]` claim may rest on a `[PROVISIONAL]` one without an explicit
dependency flag. This makes graduation a structural operation rather than a
per-claim judgement, and it would have surfaced D-13 automatically. Then either
graduate §3c.3 or flag its four dependents.

---

### D-14 — Operational Action Threshold absent from §0.4 `[MODERATE]`

The term is used six times across §§1a.6, 2f.5iv, 3a.1i, 3c.2, and 3c.3, and it
is the operative criterion for the Path-Count Metric, PSP's void declaration,
and Operational Parking. §0.4 states that terms carrying precise technical
meaning "throughout this document" are listed there and must not be substituted
with natural-language synonyms. This term qualifies and is missing.

Compounding: its definition at §3c.3 carries `[PROVISIONAL]` — see D-13.

---

## Tier 4 — Hygiene

### D-15 — Cross-reference errors `[MINOR]`

- **§0.1 item 5** cites "Meta-DRC Alignment (§3b.4, §3c.2)." **There is no
  §3b.4** — §3b terminates at 3b.3. Meta-DRC content lives at §3c.2 and §3e.1v.
- **§8b.1** cites §2f.4 for the Polyphonic Encoding path-count proxy. The proxy
  is defined at §0.4 and §1a.6; §2f.4 concerns depth-layer asymmetry.

### D-16 — Heading collision and unaddressable governance content `[MINOR]` `[COMPILATION?]`

The three governance artifacts are inlined between the glossary and §1 as `#` H1
headings ("GMRTI Architectural Model", "GMRTI Methodology & Status Markers",
"The Refinement Cycle"), the same level as the document title, while §§0–8 are
`##`. The compiled document therefore has four H1s, three of which are
subordinate content.

More consequentially, **those artifacts carry no alphanumeric addresses**, so
§0.2's instruction to "cite the shortest address that uniquely identifies it"
cannot reach any claim inside ARCHITECTURE, METHODOLOGY, or REFINEMENT. These
include the status-marker invariant definitions and the REP phase specifications
— among the most citation-worthy claims in the corpus. This audit had to cite
them by name rather than address, which is itself evidence of the defect.

**Recommended resolution.** Address them as Sections A / M / R with the same
`Na.1i` convention, or fold them into numbered sections.

### D-17 — Monolith ordering `[MINOR]` `[COMPILATION?]`

A first-time reader of the compiled document encounters the full glossary, then
the architectural rejection filter, then the methodology, then the REP — roughly
160 lines of governance — before reaching §1's statement of the problem the
framework exists to address. The README's modular order is more readable. Moving
the three artifacts to an appendix after §8 would improve the monolith without
touching modular sources, if `rewrite.py` controls the sequence.

### D-18 — `specs/` drift `[MINOR]`

§0.1 item 6 announces "strict YAML concept specifications (`specs/`)" as part of
the CLDS integration. The README TOC lists `src/`, `refinery/`, and the four
companion artifacts, but not `specs/`. Either the README is stale or the CLDS
integration is partially unlanded. Requires a check against the working tree.

### D-19 — §3b.1v excision marker occupies a live address `[MINOR]`

§3b.1v reads: "*[Excised in v0.8 to align with JIT-OM principle. Edge-typing is
strictly deferred to Stage 3 divergence resolution, maintaining Stage 1 as
purely topological.]*"

Retaining excision provenance is good practice and consistent with the
`[RESTORED]` discipline. But the marker occupies an address in the §0.2 scheme,
so any citation of 3b.1v cites a hole. **Recommended resolution:** formalise an
`[EXCISED]` status marker in `METHODOLOGY.md` so the convention is declared
rather than ad hoc, or move excision records to a changelog and renumber.

---

## Findings Checked and Passed

Recorded so a future audit can see what was examined and cleared, and so this
report is not mistaken for a claim that the framework is unsound.

- **§2a.4 (Edge-Grounding Resolution)** — The regress objection (edges must
  connect *something*) is answered cleanly by the field-analogy without
  positing a substrate, and §2a.4iii's observation that node-labels are post-hoc
  conveniences whose reification *is* the transmission failure connects the
  ontology directly to the operational apparatus. Structurally sound.
- **§7c (The GMRTI's Ambition, Precisely Stated)** — Explicitly rejecting
  universal understanding as a target, and grounding the rejection in §7c.2's
  argument that perfectly aligned covenants admit no new ideas, converts an
  otherwise grandiose programme into a falsifiable one. "Accurate disagreement"
  as the stated ambition is defensible and pre-empts the most obvious hostile
  reading.
- **§6b.4 (Compression as Covenant Intrusion)** — Identifies a real failure
  mode, names its mechanism (Redundancy-Masking at the meta-level), cites a
  specific confirmed instance with artifact-level detail (v0.6, Refinery R2–R4,
  the metaagnosticism second clause), and prescribes a concrete countermeasure.
  This is the shape a `[STABLE]` claim should have.
- **§3a.1iii and §3g (Cost-Bounded Termination and the Stopping Principle)** —
  The self-consumption guard is well-placed, and §3g.3's point that
  over-explication destroys low-DRC coordination is a genuine and
  under-appreciated cost.
- **§2e.4 (Isolation Axiom demotion)** — An earlier architectural principle
  downgraded to "useful approximation" with a stated reason. Invariant
  graduation running correctly in reverse.
- **§8a.3 (JIT-OM Ceiling)** — Declaring that no finite diagnostic sequence can
  guarantee the absence of un-encountered boundary conditions, and that the
  defences reduce risk asymptotically rather than eliminating it, is precisely
  the limit-marking the epigraph promises.

---

## Sequencing Recommendation for the REP

**Phase gate:** D-01, D-02, and D-03 are invariant violations. Per
`METHODOLOGY.md`, the `[STABLE]` set is currently inconsistent, so **no further
`[PROVISIONAL]` → `[STABLE]` graduation should proceed until they are
resolved.** D-01 in particular should enter as a Phase 1 Minimal Plan Request
for ratification, since it touches five `[STABLE]` sites and its resolution
determines the correct reading of D-07.

**Ratified order:**

1. D-01 (DRC semantics) — resolves D-07 as a consequence
2. D-02 (Polyphonic independence vs. Core Path Minimization)
3. D-03 (Operator terminus vs. CZP)
4. D-05 (Damping Factor) and D-04 (§8b.1 formula)
5. D-06 (PSP pre-screen)
6. D-08 (glossary orphans) — decide promote-or-remove per term
7. D-10 (edge-forcing in situ or honest downgrade)
8. D-11 (meta-vocabulary terminus) — requires the state machine as prerequisite
9. D-12 (execute one complete self-audit cycle on §5)
10. D-13 (dependency invariant in METHODOLOGY), D-14
11. D-09, D-15 through D-19 (hygiene; D-09, D-16, D-17 pending source check)

**Auditor's note per §8b.2.** This audit was produced by an LLM Mirror and is
therefore subject to Mirror-Prior Synchronization. Findings D-01, D-02, D-03,
D-04, D-05, D-08, and D-15 are *structural* — verifiable by inspection or
search, independent of the auditor's priors, and should reproduce under any
competent audit. Findings D-10, D-11, D-12, and D-13 are *interpretive* and
warrant a cross-model adversarial check with an opposed prompt-covenant before
ratification. No finding in this report was generated by appeal to brevity.
