"""Logic, governance, and Ma.3 dependency guard tests for GMRTI."""
import glob
import os
import re

import pytest
import yaml


def _read_all_src(base_dir: str) -> dict[str, str]:
    files = sorted(glob.glob(os.path.join(base_dir, "src", "*.md")))
    return {
        os.path.relpath(p, base_dir): open(p, encoding="utf-8").read()
        for p in files
    }


def test_no_diachronic_leftovers_v2(base_dir):
    """Prose must describe only the current state (AGENTS.md)."""
    pat = re.compile(
        r"(?:\b(?:pre-resolution|now named|formerly|previously|prior iteration|previous iteration|v0\.[0-8])\b|\bCandidate\b)"
    )
    targets = sorted(glob.glob(os.path.join(base_dir, "src", "*.md"))) + [
        os.path.join(base_dir, p)
        for p in ("GLOSSARY.md", "METHODOLOGY.md", "ARCHITECTURE.md", "REFINEMENT.md", "README.md")
    ]
    hits = []
    for path in targets:
        with open(path, encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if pat.search(line):
                    hits.append((os.path.relpath(path, base_dir), lineno, line.strip()))
    assert not hits, f"Diachronic leftovers found: {hits}"


def test_section_cross_references_resolve(base_dir):
    """Every §N.M citation in src/ must resolve to a defined heading or clause."""
    src_map = _read_all_src(base_dir)
    defined = set()
    for txt in src_map.values():
        defined.update(re.findall(r"^##\s+SECTION\s+(\d+)", txt, flags=re.M))
        defined.update(re.findall(r"^###\s+(\d+[a-z]?)\b", txt, flags=re.M))
        defined.update(
            re.findall(r"(?:^|\s)\*\*(\d+[a-z]?(?:\.\d+[a-z0-9]*)?)\b", txt, flags=re.M)
        )
    missing = []
    for rel, txt in src_map.items():
        for lineno, line in enumerate(txt.splitlines(), 1):
            for ref in re.findall(r"§(\d+[a-z]?(?:\.\d+[a-z0-9]*)?)", line):
                if ref not in defined:
                    missing.append((rel, lineno, f"§{ref}"))
    assert not missing, f"Unresolved § citations: {missing}"


def test_specs_ma3_dependency_invariant(base_dir):
    """Ma.3: STABLE specs must not depend on PROVISIONAL/OPEN specs without boundary."""
    spec_files = sorted(glob.glob(os.path.join(base_dir, "specs", "*.yaml")))
    by_id = {}
    for sf in spec_files:
        data = yaml.safe_load(open(sf, encoding="utf-8"))
        by_id[data["concept_id"]] = data

    violations = []
    for cid, data in by_id.items():
        if data.get("status") != "STABLE":
            continue
        boundaries = set(data.get("dependency_boundary", []))
        for dep in data.get("dependencies", []):
            dep_status = by_id.get(dep, {}).get("status")
            if dep_status in ("PROVISIONAL", "OPEN") and dep not in boundaries:
                violations.append((cid, dep, dep_status))
    assert not violations, f"Ma.3 spec violations (STABLE -> PROVISIONAL/OPEN): {violations}"


def test_key_terms_have_glossary_entries(base_dir):
    """Core named concepts/protocols must have a glossary entry in GLOSSARY.md."""
    glossary_text = open(os.path.join(base_dir, "GLOSSARY.md"), encoding="utf-8").read()
    terms = {t.lower() for t in re.findall(r"^#### \* (.+)$", glossary_text, flags=re.M)}
    required = [
        "Self-Annotation",
        "Maintenance Covenant",
        "Null-Effect Equivalence Axiom",
        "Epistemic Termination",
    ]
    missing = [r for r in required if not any(r.lower() in t for t in terms)]
    assert not missing, f"Missing glossary entries: {missing}"
