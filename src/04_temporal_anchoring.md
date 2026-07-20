## SECTION 4 — Temporal Anchoring

**4a — The Drift Problem** `[STABLE][RESTORED]`

**4a.1** Every semantic covenant is in constant motion. Experience, reflection,
encounter with new ideas, and the passage of time all alter the edge-structure
of a covenant continuously.

**4a.2** This creates a problem for all three transmission modes, but most
acutely for Self-to-Future-Self transmission: the entity that encoded a message
at *t₁* is not semantically identical to the entity that will decode it at *t₂*.

**4a.3** Without temporal anchoring, documentation — the primary technology for
self-to-future-self transmission — is vulnerable to silent distortion: the
author re-reads their own work through a covenant that has drifted, reading
meaning into or out of the text that the original encoding did not contain. This
distortion is typically invisible to the author, which makes it more dangerous
than external transmission failure.

**4b — Temporal Anchoring Operations** `[PROVISIONAL]`

**4b.1** The GMRTI prescribes the following temporal anchoring practices:

- **4b.1i** *Date-stamping of covenant states*: major documents and framework
articulations should be explicitly dated and treated as expressions of the
author's covenant at that moment, not as timeless declarations. This
document's version history is an instance of this practice.
- **4b.1ii** *Drift logging*: where a thinker is aware that their understanding
of a key concept has changed, that change should be explicitly documented,
linking the old edge-structure to the new one and identifying the experience or
argument that drove the transition.
- **4b.1iii** *Reconstruction protocols*: when re-engaging with past work, the
reader — even if identical to the author — should perform a Generative
Reconstruction, attempting to recover the *t₁* edge-structure rather than
reading the document through the current *t₂* covenant.

**4b.2** Temporal anchoring cannot be applied exhaustively without prohibitive
cost. It is therefore a prioritization problem: anchor the edge-clusters most
likely to drift significantly and most critical to the transmission's long-term
integrity. Axiomatic-layer clusters warrant anchoring before Surface clusters,
precisely because their drift is least visible and most consequential.
`[PROVISIONAL]`

**4b.3 — Dynamic Re-Anchoring and Damping Factor Axiom** `[STABLE]`

To stabilize Artifact Anchors against continuous Temporal Drift, GMRTI defines
**Dynamic Re-Anchoring**: treating the anchor not as a static coordinate,
but as a moving average updated via continuous correction vectors.
- **The Damping Factor Axiom**: To prevent anchor oscillation and guarantee
mathematical convergence to a stable anchor, all correction vector updates
$v_t$ are scaled by a damping factor $\lambda < 1.0$ (typically $\lambda =
0.15$). The updated anchor $A_{t+1}$ is defined as:
  $$A_{t+1} = A_t + \lambda (A_{decl} - A_t)$$
- **Convergence Theorem**: Under any bounded correction stream, the anchor
trajectory converges to a stable equilibrium state if the sum of update
magnitudes is finite:
  $$\sum_{t=1}^{\infty} |v_t| < \infty$$
