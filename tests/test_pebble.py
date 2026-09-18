import os
import pytest
from pebble import (
    assemble_pebble_document,
    check_pebble_sync,
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
    # The plain sections before the glossary must not contain formal status markers
    # Split before the glossary section
    plain_part = doc.split("## The Formal Glossary (Academic Reference)")[0]
    assert "[STABLE]" not in plain_part
    assert "[PROVISIONAL]" not in plain_part
    assert "[OPEN]" not in plain_part
    assert "[RECURSIVE]" not in plain_part
    assert "[RESTORED]" not in plain_part
    assert "[EXCISED]" not in plain_part
    assert "[PLAIN]" not in plain_part
    assert "[->causal]" not in plain_part
    assert "[->inferential]" not in plain_part


def test_check_pebble_sync_in_sync(base_dir):
    result = check_pebble_sync(base_dir)
    assert isinstance(result, dict)
    assert result["in_sync"] is True
    assert result["error"] is None


def test_check_pebble_sync_out_of_sync(tmp_path, base_dir):
    pebble_path = tmp_path / "PEBBLE.md"
    pebble_path.write_text("wrong content", encoding="utf-8")
    result = check_pebble_sync(str(tmp_path))
    assert result["in_sync"] is False
