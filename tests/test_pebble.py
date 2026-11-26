import os
import pytest
from pebble import (
    assemble_pebble_document,
    check_pebble_sync,
    clean_plain_text,
    create_pebble_document,
)


def test_assemble_pebble_document_success(base_dir):
    doc = assemble_pebble_document(base_dir)
    assert doc.startswith("# PEBBLE: The Plain-Language Alignment Guide")
    assert "SECTION 0 — Preamble and Document Conventions" in doc
    assert "SECTION 1 — The Problem the GMRTI Addresses" in doc
    assert "SECTION 2 — Foundational Architecture" in doc
    assert "SECTION 7 — Relation to Downstream Applications" in doc
    assert "The Formal Glossary (Academic Reference)" in doc
    assert "### Glossary" in doc
    assert "\n# Glossary\n" not in doc
    assert "SECTION 9 — Coda" in doc


def test_pebble_contains_science_preamble(base_dir):
    doc = assemble_pebble_document(base_dir)
    assert "Man is a creature of Science." in doc
    assert "Epistemology didn't begin with Newton" in doc
    assert "Science began with burning meat" in doc
    assert "And there must be a Science of Understanding." in doc


def test_pebble_contains_glossary(base_dir):
    doc = assemble_pebble_document(base_dir)
    assert "The Formal Glossary (Academic Reference)" in doc
    assert "**GMRTI** — General Method for Refinement and Transmission of Ideas" in doc
    assert "**COMOSÍ**" in doc
    assert "**METAAGNOSTICISM**" in doc


def test_pebble_contains_coda(base_dir):
    doc = assemble_pebble_document(base_dir)
    assert "The Pebble and the Boulder" in doc
    assert "Sisyphus got a boulder" in doc
    assert "The pebble was never the problem." in doc


def test_pebble_excludes_status_markers(base_dir):
    doc = assemble_pebble_document(base_dir)
    plain_part = doc.split("## The Formal Glossary (Academic Reference)")[0]
    for marker in (
        "[STABLE]",
        "[PROVISIONAL]",
        "[OPEN]",
        "[RECURSIVE]",
        "[RESTORED]",
        "[EXCISED]",
        "[PLAIN]",
        "[->causal]",
        "[->inferential]",
    ):
        assert marker not in plain_part


def test_clean_plain_text_preserves_bold_and_code():
    raw = "This is **very important** `[STABLE]` with `code` [->causal] and ****."
    cleaned = clean_plain_text(raw)
    assert "**very important**" in cleaned
    assert "`code`" in cleaned
    assert "[STABLE]" not in cleaned
    assert "[->causal]" not in cleaned
    assert "****" not in cleaned


@pytest.mark.repo_state
def test_check_pebble_sync_in_sync(base_dir):
    result = check_pebble_sync(base_dir)
    assert isinstance(result, dict)
    assert result["in_sync"] is True
    assert result["error"] is None


def test_check_pebble_sync_out_of_sync(tmp_path, base_dir):
    import shutil

    shutil.copytree(os.path.join(base_dir, "src"), str(tmp_path / "src"))
    shutil.copy2(os.path.join(base_dir, "GLOSSARY.md"), str(tmp_path / "GLOSSARY.md"))
    pebble_path = tmp_path / "PEBBLE.md"
    pebble_path.write_text("wrong content", encoding="utf-8")
    result = check_pebble_sync(str(tmp_path))
    assert result["in_sync"] is False


def test_check_pebble_sync_missing(tmp_path):
    result = check_pebble_sync(str(tmp_path))
    assert result["in_sync"] is False
    assert "does not exist" in result["error"]


def test_create_pebble_document_writes_and_dry_run(tmp_path, base_dir):
    out_file = tmp_path / "PEBBLE_OUT.md"
    dry = create_pebble_document(base_dir=base_dir, output_path=str(out_file), dry_run=True)
    assert dry == str(out_file)
    assert not out_file.exists()

    written = create_pebble_document(base_dir=base_dir, output_path=str(out_file))
    assert written == str(out_file)
    assert out_file.exists()
    assert out_file.read_text(encoding="utf-8").startswith("# PEBBLE:")


def test_parse_src_file_10_0_only_takes_one_paragraph():
    """B5: Heading '10.0 ...' must not match '0.0' multi-paragraph preamble rule."""
    from pebble import parse_src_file

    sample = (
        "## SECTION 10 — Test\n\n"
        "**10.0 Not Preamble** `[STABLE]`\n\n"
        "`[PLAIN]` First paragraph only.\n\n"
        "Second paragraph is academic prose, not plain.\n"
    )
    parsed = parse_src_file(sample, filename="src/10_test.md")
    assert len(parsed["plain_blocks"]) == 1
    assert parsed["plain_blocks"][0]["text"] == "First paragraph only."


def test_assemble_pebble_missing_source_raises(tmp_path):
    """B6: Missing manifest source files raise FileNotFoundError."""
    import pytest

    with pytest.raises(FileNotFoundError, match="Critical source file missing"):
        assemble_pebble_document(str(tmp_path))


def test_excluded_allegory_anchor_still_exists(base_dir):
    """B7: Guard that excluded clause 2f.3ii still exists in src/02_architecture.md."""
    arch_path = os.path.join(base_dir, "src", "02_architecture.md")
    with open(arch_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "- **2f.3ii" in content
