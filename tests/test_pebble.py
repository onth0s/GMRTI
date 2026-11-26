import os
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


def test_check_pebble_sync_in_sync(base_dir):
    result = check_pebble_sync(base_dir)
    assert isinstance(result, dict)
    assert result["in_sync"] is True
    assert result["error"] is None


def test_check_pebble_sync_out_of_sync(tmp_path):
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
