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
  locally via the Python scripts (`wrap.py --check`, `rewrite.py --check`)
  and the `pytest` test suite only.
