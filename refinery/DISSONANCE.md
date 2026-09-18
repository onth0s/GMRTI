# DISSONANCE.md

## Entry D-01 — Compression Asymmetry Justification & STABLE Clarification

**Status**: `[RESOLVED]` (Ratified via `DEC-19`, `DEC-20`, `DEC-21`)
**Addresses**: `6b.4` (Compression as Covenant Intrusion); `0.3` / `Ma.1`
(Status Markers); `3a.4` / `GLOSSARY.md` (Domain Risk Coefficient) **Auditor**:
External adversarial dialogue (human-directed), logged per Ra.1 **Date**:
2026-09-18

---

### D-01.1 — The Contention

`[PLAIN]` Section 6b.4 says compressing Polyphonic Encoding paths is
presumptively a bad thing to do. But it never says *why* the burden of proof
should fall on the person doing the cutting rather than on the person doing the
keeping. That gap makes the rule read as an assertion, not a derivation — which
is exactly the kind of unstated axiomatic commitment the framework elsewhere
insists on surfacing.

**D-01.1i — Formal statement**: `6b.4` asserts an asymmetric epistemic burden
(compression is presumptively covenant intrusion; preservation is not
presumptively over-encoding) without grounding that asymmetry in a prior
principle. This is a dissonance of *justification*, not of *conclusion* — the
audit does not dispute that the asymmetry is correct, only that it is currently
undefended. A framework that otherwise requires explicit dependency boundaries
(Ma.3) should not rest a `[STABLE]` behavioral prescription on an ungrounded
assertion.

**D-01.1ii — Symmetry gap**: Section 2f names Redundancy-Masking (paths that
look sufficient but conceal a topological void) as a real risk. No symmetric
failure mode is named for *actual* over-encoding — redundant paths that are
truly duplicate under Core Path Minimization (§2f.6) and whose removal costs
nothing. Without that symmetric case on record, 6b.4 cannot currently
distinguish "compression that destroyed real content" from "compression that
correctly identified true redundancy." The document's own revision history (loss
of allegories requiring retroactive introduction of the `[ALLEGORY]` tag)
supplies evidence for the former; no instance of the latter is logged anywhere
in the repository.

---

### D-01.2 — Resolution Surfaced in Dialogue

`[PLAIN]` Think of art tutorials. Nobody says "there are enough YouTube drawing
tutorials, stop making them" — because you can't know in advance which
explanation will be the one that clicks for a given learner's existing mental
structure. That's exactly why Polyphonic Encoding exists: not redundancy for its
own sake, but multiple independent routes to the same destination because the
receiver's prior topology is unknown ex ante.

**D-01.2i — Formal grounding**: The asymmetry in 6b.4 is justified by Polyphonic
Encoding's own stated purpose (§2a): a transmitting covenant cannot know in
advance which encoding path achieves comosí with an unknown receiver's existing
edge-structure. Since the cost of an unnecessary path is low (marginal length)
but the cost of a wrongly cut path is high (total transmission failure for
whichever receivers that path alone would have reached), the default under
uncertainty must favor preservation. This is not an appeal to authorial
sentiment — it is a direct consequence of Polyphonic Encoding's justification
applied to the act of editing, not just the act of authoring.

**D-01.2ii — Recommended allegory** (for REP consideration, not ratified here):
`[ALLEGORY: POLYPHONIC-ENCODING]`, sited near §2a and/or 6b.4 — the
art-tutorial/artbook case above, illustrating why redundant independent
explanations are not presumptively wasteful when the receiver's prior structure
is unknown.

**D-01.2iii — Recommended corollary direction** (for `DECISIONS.md`, not
specified here — REP-scoped): 6b.4 should be amended from a bare prohibition
into a burden-of-proof rule: a cut is legitimate only when it can be shown,
under Core Path Minimization (§2f.6), to be destination-isomorphic *and*
non-route-independent with a path that survives the edit — i.e., demonstrably
true redundancy, not merely reduced length. An edit that cannot make this
showing is presumptively intrusion. This closes the symmetry gap in D-01.1ii by
giving "legitimate compression" a defined, falsifiable shape instead of leaving
it unaddressed.

---

### D-01.3 — STABLE Clarification Gap

`[PLAIN]` Separately: the `[STABLE]` tag doesn't mean "this is objectively
true." It means "I'm done revising this for now, and here's why that's not the
same as claiming truth." The document explains the *mechanism* (3g.2 — closure
against infinite regress) but doesn't state the *epistemic status* clearly
enough near the tag's own definition, which risks a reader mistaking authorial
closure for a truth-claim.

**D-01.3i — Formal statement**: `0.3` and `Ma.1` define `[STABLE]` procedurally
(load-bearing, changes propagate, requires Refinement Cycle to downgrade) but do
not explicitly disclaim the truth-status of the marker at its site of
definition. 3g.2 supplies the underlying justification (closure against
self-consuming refinement) but is not cross-referenced from 0.3/Ma.1, leaving
the connection implicit.

**D-01.3ii — Related point on DRC ambiguity**: The Domain Risk Coefficient (§ —
DRC definition) is left deliberately unresolved as a fixed scale of what counts
as "high-risk." This is not an oversight — resolving it would require importing
a moral/normative framework for what counts as important or dangerous, which
GMRTI, as a detection mechanism for semantic divergence rather than an arbiter
of value, does not claim authority to supply. This deliberate ambiguity is
consistent with STABLE's non-truth-claiming status: both are places where the
framework declines to assert an external authority (truth, or risk-ranking) it
does not hold, leaving disambiguation to the covenants applying it rather than
embedding it as a first-class value judgment in the framework itself.

**D-01.3iii — Recommended repair direction** (REP-scoped, not ratified here):
add an explicit disclaimer at `0.3`/`Ma.1`, adjacent to the `[STABLE]`
definition, cross-referencing `3g.2`: *"STABLE marks authorial closure — a claim
not currently being revised — not a truth-claim or proof of correctness. See
3g.2 for why closure is necessary despite this."* Consider a parallel one-line
note at the DRC definition making the deliberateness of its ambiguity explicit
at the site of definition rather than only recoverable by inference.

---

### D-01.4 — Disposition

Both sub-contentions (D-01.1/2 and D-01.3) are resolved and ratified into
`DECISIONS.md` under `[DEC-19]`, `[DEC-20]`, and `[DEC-21]`. Implemented across
`src/06_refinement_vectors.md` (§6b.4), `src/00_preamble.md` (§0.3),
`METHODOLOGY.md` (§Ma.1), `src/03_algorithm.md` (§3a.4), `GLOSSARY.md`, and
`specs/concept_polyphony.yaml`.
