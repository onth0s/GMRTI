# Project Rules & Behavioral Constraints

- **Do Not Restore Deleted Files**: Never run `git restore` (or similar
  commands) on files deleted or pruned in the workspace by the user. If a file
  is deleted or pruned (such as reducing its content to placeholder markers
  like `.gitkeep`), this represents a deliberate user pruning decision. Leave
  them deleted or pruned.

- **Monolithic Revision Archival**: Only keep the latest compiled monolithic
  revision (`GMRTI_<timestamp>.md`) in the workspace root / current working
  directory. All other monolithic revisions must be stored in the
  [archive](file:///c:/Users/Leonardo/001/TXT/GMRTI/archive) directory.

- **No CI/CD or External Automation Infrastructure**: Never add CI pipelines,
  GitHub Actions workflows, pre-commit hooks, cloud build configurations, or
  any other external automation infrastructure to this repository. This
  prohibition is absolute and unconditional. Verification is performed
  locally via the Python scripts (`wrap.py --check`, `rewrite.py --check`),
  the `pytest` test suite, and `cd math && lake build` only.

- **Formal Model Boundary** (`math/`): The Lean 4 package in `math/` is a
  satellite verification artifact. It must never be imported by, referenced
  from, or compiled into the GMRTI treatise sources (`src/`, `GLOSSARY.md`,
  monolith). The treatise acknowledges its existence in exactly one sentence
  in `src/00_preamble.md` and nowhere else. No LaTeX, no theorem statements,
  no Lean 4 syntax of any kind may appear in any treatise source file.

- **`wrap.py` Scope Exclusion**: The `.lean` source files in `math/` are
  formatted by `lake fmt`, not by `wrap.py`. Never add `math/` to the
  `collect_targets` scan in `wrap.py`.

- **Polyphony Strong Proof (DEFERRED — action required when weak proof is
  complete)**: `math/GMRTI/Polyphony.lean` currently proves only the **weak**
  monotonicity form (adding a polyphonic path does not *increase* semantic
  entropy). The **strong** form — that a destination-isomorphic, topologically
  disjoint path *strictly reduces* entropy — requires a partition-structure
  axiom pending resolution of §8b.1 (`src/08_gaps.md`). When the weak proof
  is sorry-free and §8b.1 is resolved, begin the strong proof immediately.
  The strong theorem stub is already present in `Polyphony.lean` as a
  `-- TODO (strong)` comment.

- **Simple Everyday Language for Allegories**: All allegories (`[ALLEGORY]`)
  must be written in plain, grounded, everyday language. They must avoid
  unnecessary jargon, overly academic vocabulary, or convoluted syntax (e.g.,
  write "forces" instead of "vectors", "the factory that makes factories"
  instead of "industrial manufacturing facilities"). An allegory's entire
  purpose is to provide a low-entropy, accessible bridge to an abstract concept.

