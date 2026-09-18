# GMRTI Formal Model (Lean 4)

A standalone satellite verification artifact providing machine-checked proofs
for the quantitative claims latent in the General Method for Refinement and
Transmission of Ideas (GMRTI).

## Boundary & Architectural Scope

Per `AGENTS.md`:
- This package is an independent satellite artifact. It is never imported by,
  referenced from, or compiled into the GMRTI treatise sources (`src/`, `GLOSSARY.md`,
  or monolithic compilations).
- Source files are formatted with `lake fmt`, not `wrap.py`.

## Modules & Verified Claims

| Module | Purpose | Key Verified Theorems |
|---|---|---|
| `GMRTI.Covenant` | Labeled directed multigraph covenant representation | Sub-covenant order `≤`, edge insertion monotonicity |
| `GMRTI.Entropy` | Hartley Semantic Entropy $H_s(S) = \log_2 \|X\|$ | Subset monotonicity of compatible topologies, $H_s$ non-increasing |
| `GMRTI.Distance` | Operational test probe metric and Comosí predicate | Symmetry, reflexivity of functional congruence |
| `GMRTI.Refinement` | Iterative constraint injection during Refinement Cycle | Entropy reduction under repair, strict shrinkage on effective repairs |
| `GMRTI.Temporal` | Exponential smoothing & Lag-Bounded Tracking (§4b.3) | One-step error bound, steady-state invariant $\|A - D\| \le \delta / \lambda$, Lag-Bounded Tracking Principle $\|A_{t+1} - D_t\| \le \delta \frac{1 - \lambda}{\lambda}$ |
| `GMRTI.Polyphony` | Multipath transmission under alternative routes | Weak monotonicity theorem (entropy non-increasing under polyphonic augmentation). *Strong form deferred pending §8b.1.* |

## Building & Verification

Verify the entire formal model locally:

```bash
cd math
lake build
```