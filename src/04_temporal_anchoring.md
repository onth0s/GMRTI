## SECTION 4 — Temporal Anchoring

**4a — The Drift Problem** `[STABLE][RESTORED]`

`[PLAIN]` The "you" who writes a note today and the "you" who reads it in five
years are not the same person. As you learn and change, your inner dictionary
drifts, which means you can easily misread your own past notes.

**4a.1** Every semantic covenant is in constant motion. Experience, reflection,
    encounter with new ideas, and the passage of time all alter the
    edge-structure of a covenant continuously.

**4a.2** This creates a problem for all three transmission modes, but most
    acutely for Self-to-Future-Self transmission: the entity that encoded a
    message at *t₁* is not semantically identical to the entity that will decode
    it at *t₂*.

**4a.3** Without temporal anchoring, documentation — the primary technology for
    self-to-future-self transmission — is vulnerable to silent distortion: the
    author re-reads their own work through a covenant that has drifted, reading
    meaning into or out of the text that the original encoding did not contain.
    This distortion is typically invisible to the author, which makes it more
    dangerous than external transmission failure.

**4b — Temporal Anchoring Operations** `[PROVISIONAL]`

`[PLAIN]` To stop your guides and notes from drifting away, update them with
small, careful nudges over time rather than throwing everything out and starting
over every time something changes.

**4b.1** The GMRTI prescribes the following temporal anchoring practices:

- **4b.1i** *Date-stamping of covenant states*: major documents and framework
    articulations should be explicitly dated and treated as expressions of the
    author's covenant at that moment, not as timeless declarations. This
    document's version history is an instance of this practice.
- **4b.1ii** *Drift logging*: where a thinker is aware that their understanding
    of a key concept has changed, that change should be explicitly documented,
    linking the old edge-structure to the new one and identifying the experience
    or argument that drove the transition.
- **4b.1iii** *Reconstruction protocols*: when re-engaging with past work, the
    reader — even if identical to the author — should perform a Generative
    Reconstruction, attempting to recover the *t₁* edge-structure rather than
    reading the document through the current *t₂* covenant.

**4b.2** Temporal anchoring cannot be applied exhaustively without prohibitive
    cost. It is therefore a prioritization problem: anchor the edge-clusters
    most likely to drift significantly and most critical to the transmission's
    long-term integrity. Axiomatic-layer clusters warrant anchoring before
    Surface clusters, precisely because their drift is least visible and most
    consequential. `[PROVISIONAL]`

**4b.3 — Dynamic Re-Anchoring and Exponential Smoothing Heuristic**
`[PROVISIONAL]`

To stabilize Artifact Anchors against continuous Temporal Drift, GMRTI defines
**Dynamic Re-Anchoring**: treating the anchor not as an immutable coordinate,
but as a damped moving average updated via successive declaration states
$A_{decl,t}$.
- **The Damping Factor Axiom**: To prevent anchor oscillation and maintain
  stability under noisy or local fluctuations, updates are scaled by a damping
  factor $\lambda \in (0, 1)$ (with $\lambda = 0.15$ as an operational
  default, subject to empirical calibration):
  $$A_{t+1} = (1 - \lambda)A_t + \lambda A_{decl,t} = A_t + \lambda (A_{decl,t} - A_t)$$
- **Lag-Bounded Tracking Principle**: Under an incoming sequence of declarations
  with bounded drift rate $\delta = \sup_t \|A_{decl,t+1} - A_{decl,t}\|$, the
  steady-state tracking lag of the smoothed anchor is bounded by:
  $$\limsup_{t \to \infty} \|A_t - A_{decl,t}\| \le \delta \frac{1 - \lambda}{\lambda}$$
This frames the choice of $\lambda$ as a formal tradeoff: smaller $\lambda$
suppresses local variance and prevents oscillation, while larger $\lambda$
minimizes steady-state tracking lag behind authentic covenant evolution.

- **4b.3i — The Floating Sea-Anchor Allegory**
    `[ALLEGORY: DYNAMIC-REANCHORING]`
    In deep, stormy waters, a ship cannot drop a heavy iron anchor down to the
    ocean floor: the seabed is too deep and rigid, and the chain will snap. But
    if the captain drops no anchor at all, every passing wave spins the ship out
    of control ($\lambda = 1.0$). Instead, the crew deploys a submerged cloth
    sea-anchor (a drogue with $\lambda = 0.15$): it allows the vessel to glide
    smoothly with the deep ocean current while dampening out the violent surface
    chop, keeping the bow pointed in a steady, safe direction.
