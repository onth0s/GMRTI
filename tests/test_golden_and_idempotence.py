import glob
import os
import yaml

from pebble import assemble_pebble_document
from rewrite import assemble_monolithic_document
from wrap import wrap_markdown, wrap_yaml


def _build_golden_repo(root):
    """Create a minimal deterministic GMRTI treatise fixture for golden tests."""
    (root / "README.md").write_text(
        "# GMRTI — Golden Fixture\n\nIntro line.\n\n## Table of Contents\n\n- Item\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "GLOSSARY.md").write_text(
        "# Glossary\n\n- **Term** — Definition.\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "ARCHITECTURE.md").write_text(
        "# GMRTI Architectural Model\n\nArch body.\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "METHODOLOGY.md").write_text(
        "# GMRTI Methodology & Status Markers\n\nMethod body.\n",
        encoding="utf-8",
        newline="\n",
    )
    (root / "REFINEMENT.md").write_text(
        "# The Refinement Cycle\n\nRefine body.\n",
        encoding="utf-8",
        newline="\n",
    )

    src = root / "src"
    src.mkdir()
    files = {
        "00_preamble.md": (
            "## SECTION 0 — Preamble\n\n"
            "**0.0 Why This Exists** `[STABLE]`\n\n"
            "`[PLAIN]`\n\n"
            "First plain paragraph.\n\n"
            "Second plain paragraph.\n\n"
            "Third plain paragraph.\n\n"
            "Fourth paragraph not in plain.\n"
        ),
        "01_problem.md": (
            "## SECTION 1 — Problem\n\n"
            "**1.1 Core Gap** `[STABLE]` `[->causal]`\n\n"
            "`[PLAIN]` Plain problem summary.\n\n"
            "Formal academic body.\n\n"
            "- **1.1i — Stone Bridge Allegory** `[ALLEGORY]` A simple stone bridge.\n"
        ),
        "02_architecture.md": "## SECTION 2 — Architecture\n\nFormal arch.\n",
        "03_algorithm.md": "## SECTION 3 — Algorithm\n\nFormal alg.\n",
        "04_temporal_anchoring.md": "## SECTION 4 — Temporal\n\nFormal temp.\n",
        "05_metalanguage.md": "## SECTION 5 — Metalanguage\n\nFormal meta.\n",
        "06_refinement_vectors.md": "## SECTION 6 — Refinement\n\nFormal ref.\n",
        "07_downstream.md": "## SECTION 7 — Downstream\n\nFormal down.\n",
        "08_gaps.md": "## SECTION 8 — Gaps\n\nFormal gaps.\n",
        "09_coda.md": "## SECTION 9 — Coda\n\nThe Pebble and the Boulder.\n",
    }
    for name, text in files.items():
        (src / name).write_text(text, encoding="utf-8", newline="\n")


_EXPECTED_MONOLITH = (
    "# GMRTI — Golden Fixture\n\n"
    "Intro line.\n\n"
    "## SECTION 0 — Preamble\n\n"
    "**0.0 Why This Exists** `[STABLE]`\n\n"
    "`[PLAIN]`\n\n"
    "First plain paragraph.\n\n"
    "Second plain paragraph.\n\n"
    "Third plain paragraph.\n\n"
    "Fourth paragraph not in plain.\n\n"
    "**0.4 Vocabulary**\n\n"
    "- **Term** — Definition.\n\n"
    "---\n\n"
    "## SECTION 1 — Problem\n\n"
    "**1.1 Core Gap** `[STABLE]` `[->causal]`\n\n"
    "`[PLAIN]` Plain problem summary.\n\n"
    "Formal academic body.\n\n"
    "- **1.1i — Stone Bridge Allegory** `[ALLEGORY]` A simple stone bridge.\n\n"
    "---\n\n"
    "## SECTION 2 — Architecture\n\nFormal arch.\n\n"
    "---\n\n"
    "## SECTION 3 — Algorithm\n\nFormal alg.\n\n"
    "---\n\n"
    "## SECTION 4 — Temporal\n\nFormal temp.\n\n"
    "---\n\n"
    "## SECTION 5 — Metalanguage\n\nFormal meta.\n\n"
    "---\n\n"
    "## SECTION 6 — Refinement\n\nFormal ref.\n\n"
    "---\n\n"
    "## SECTION 7 — Downstream\n\nFormal down.\n\n"
    "---\n\n"
    "## SECTION 8 — Gaps\n\nFormal gaps.\n\n"
    "---\n\n"
    "## SECTION 9 — Coda\n\nThe Pebble and the Boulder.\n\n"
    "---\n\n"
    "## APPENDIX A — Architectural Model\n\nArch body.\n\n"
    "---\n\n"
    "## APPENDIX M — Methodology & Status Markers\n\nMethod body.\n\n"
    "---\n\n"
    "## APPENDIX R — The Refinement Cycle\n\nRefine body.\n"
)

_EXPECTED_PEBBLE = (
    "# PEBBLE: The Plain-Language Alignment Guide\n\n"
    "> *A high-school-accessible, jargon-free transmission of the General Method\n"
    "> for Refinement and Transmission of Ideas (GMRTI).*\n\n"
    "---\n\n"
    "## SECTION 0 — Preamble\n\n"
    "### 0.0 Why This Exists\n\n"
    "First plain paragraph.\n\n"
    "Second plain paragraph.\n\n"
    "Third plain paragraph.\n\n"
    "---\n\n"
    "## SECTION 1 — Problem\n\n"
    "### 1.1 Core Gap\n\n"
    "Plain problem summary.\n\n"
    "> **Allegory: Stone Bridge**\n"
    ">\n"
    "> A simple stone bridge.\n\n"
    "---\n\n"
    "## The Formal Glossary (Academic Reference)\n\n"
    "*The following glossary contains the verbatim formal definitions from\n"
    "the full GMRTI treatise. It is included here for readers who wish to\n"
    "explore the precise academic and mathematical definitions of the framework.*\n\n"
    "### Glossary\n\n"
    "- **Term** — Definition.\n\n"
    "---\n\n"
    "## SECTION 9 — Coda\n\n"
    "The Pebble and the Boulder.\n"
)


def test_golden_monolith_assembly(tmp_path):
    _build_golden_repo(tmp_path)
    assert assemble_monolithic_document(str(tmp_path)) == _EXPECTED_MONOLITH


def test_golden_pebble_assembly(tmp_path):
    _build_golden_repo(tmp_path)
    assert assemble_pebble_document(str(tmp_path)) == _EXPECTED_PEBBLE


def test_wrap_markdown_idempotent_on_src(base_dir):
    src_files = sorted(glob.glob(os.path.join(base_dir, "src", "*.md")))
    assert src_files
    for path in src_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        once = wrap_markdown(content, width=80)
        twice = wrap_markdown(once, width=80)
        assert once == twice, f"wrap_markdown not idempotent on {path}"


def test_wrap_yaml_semantic_roundtrip_on_specs(base_dir):
    spec_files = sorted(glob.glob(os.path.join(base_dir, "specs", "*.yaml")))
    assert spec_files
    for path in spec_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        wrapped = wrap_yaml(content, width=80)
        assert yaml.safe_load(content) == yaml.safe_load(wrapped), (
            f"wrap_yaml changed parsed YAML semantics in {path}"
        )
        assert wrap_yaml(wrapped, width=80) == wrapped, (
            f"wrap_yaml not idempotent on {path}"
        )
