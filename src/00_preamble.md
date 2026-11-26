## SECTION 0 — Preamble and Document Conventions

### 0.0 — Why This Exists
`[PLAIN]` Man is a creature of Science. Homo Sapiens, right? Epistemology didn't
begin with Newton describing the motion of rolling balls down slopes nor the
orbital trajectories of celestial objects that have been shaping human myth for
as long as we were capable of looking at the sky. No. Science began with burning
meat and learning it tasted better that way. Crushing rock and dirt and learning
that it could be heated and combined into better things. Planting seeds on the
ground and learning that that place now belonged to you and your peers.

And passing it along. And teaching it to your kids.

Man is a creature of Science. And there must be a Science of Understanding. It
has been long enough. It's time to pass it on to future generations.

### 0.1 Purpose of This Document
`[PLAIN]` When you try to explain an idea to someone, you can never be
completely sure they understood exactly what you meant — and they can't be sure
either. The GMRTI is a step-by-step method for finding where that gap is, naming
it, and closing it as tightly as the situation requires.

This document articulates the General Method for Refinement and Transmission of
Ideas (GMRTI) as a unified, operational framework for diagnosing and repairing
semantic divergence without sacrificing diagnostic precision.

Its core structural commitments are:

1. **Tiered Edge Taxonomy Economy:** Using a lightweight tiered approach
   (coarse cut for Covenant Declaration vs. finer cut via JIT-OM for
   misattribution repair) to prevent classification overhead from blocking
   transmission.
2. **Mirror-to-Generative Transition:** Formalizing the Divergence Report with
   an explicit artifact template to make the transition operational.
3. **Syntactic Edge-Forcing (§2g):** Requiring explicit primary relational
   operators in formalized declarations.
4. **Empirical Validation of Semantic Entropy (§1a, §2f):** Establishing an
   empirical protocol for the Semantic Entropy Metric by counting Polyphonic
   Encoding paths to reach Operational Parking.
5. **Meta-DRC Alignment (§3c.2, §3e.1v):** Codifying the protocol to handle
   divergence over Domain Risk Coefficient classification itself.
6. **Cognitive Load Distribution System (CLDS):** Governing GMRTI's authoring
   through strict YAML concept specifications (`specs/`), formal Status Markers
   (`METHODOLOGY.md`), and the Ratified Execution Protocol (`REFINEMENT.md`) to
   manage and prevent structural debt.

A standalone Lean 4 formal verification package for the mathematical claims
latent in this framework is maintained in `math/` and is explicitly outside the
scope of this treatise.

### 0.2 Alphanumerical Convention
`[PLAIN]` The sections in this document are numbered so that any specific claim
can be pointed to precisely — like a street address for ideas. If you want to
challenge, quote, or repair something, you cite its address.

Sections follow the pattern `N`, `Na`, `Na.1`, `Na.1i` for four levels of depth:

- `N` — Major division (e.g. `3`, or Appendices `A`, `M`, `R`)
- `Na` — Named subsection (e.g. `3a`, `Ma`)
- `Na.1` — Numbered clause within subsection (e.g. `3a.1`, `Ma.1`)
- `Na.1i` — Roman-numeral sub-clause (e.g. `3a.1i`, `2e.5i`)

When pointing to a specific dissonance or claim for critique, cite the shortest
address that uniquely identifies it. Addresses identify clauses within the
current compiled revision only and are not stable across revisions.

### 0.3 Status Markers
`[PLAIN]` Every claim in this document carries a small tag showing how settled
it is — whether it is load-bearing, still being tested, an open puzzle, or a
plain-language example. That way you always know which parts are bedrock and
which parts are still under construction.

- `[STABLE]` — Considered load-bearing; changes here propagate broadly. Marks
  authorial closure (claims not currently being revised to avoid infinite
  regress per §3g.2), not an assertion of metaphysical truth or final proof
- `[PROVISIONAL]` — Held with confidence but open to revision
- `[OPEN]` — Known gap; active work needed
- `[RECURSIVE]` — Applies to the framework itself; check for reflexivity
- `[ALLEGORY]` — Concrete domain-specific instantiation serving as an
  independent polyphonic-encoding path to an abstract target
- `[PLAIN]` — Plain-language entry ramp compiled into `PEBBLE.md`; written
  at a high-school reading level; not an epistemic invariant

```table
TITLE: Treatise Status Marker Reference
| Marker | Dimension | Meaning |
|---|---|---|
| `[STABLE]` | Epistemic | Authorial closure — load-bearing invariant not currently under revision (§3g.2) |
| `[PROVISIONAL]` | Epistemic | Held with operational confidence; open to revision pending audit |
| `[OPEN]` | Epistemic | Known unresolved gap; active work needed |
| `[RECURSIVE]` | Reflexive | Applies to the GMRTI framework itself; check for self-consistency |
| `[ALLEGORY]` | Structural | Concrete domain-bounded polyphonic path to an abstract target |
| `[PLAIN]` | Structural | High-school-accessible entry ramp compiled into `PEBBLE.md` |
```
