# Refinery Workspace

This directory functions as the dedicated adversarial audit and refinement
workspace for the General Method for Refinement and Transmission of Ideas
(GMRTI).

## Purpose & Architectural Role

1. **Adversarial Audit Repository**: Houses in-depth dissonance reports (such as
   `refinery/DISSONANCE.md`), providing the raw critiques, citations, and
   analysis
   generated during Refinement Cycle Stage 1 (Adversarial Audit).
2. **Interim Working Artifacts**: Serves as a staging area for candidate edits,
   scratch explorations, and divergence localization notes during active REP
   cycles.
3. **Refinement Cycle Inspection Target**: Formally inspected during Stage 5(b)
   of the Refinement Cycle (§6b.1) to ensure all identified dissonances and gaps
   have been addressed or graduated into canonical status.

## Compilation Boundary

Artifacts within `refinery/` are deliberately **excluded** from the compiled
monolithic treatise (`GMRTI_<timestamp>.md`). They represent the diagnostic
apparatus and historical audit records of the framework rather than the
normative content of the treatise itself.

All Markdown files in `refinery/` are tracked by `wrap.py` to maintain canonical
80-character formatting.
