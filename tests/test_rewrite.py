import os
import shutil
import pytest
from rewrite import assemble_monolithic_document, archive_prior_monolithic_files

def test_assemble_monolithic_document_success():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc = assemble_monolithic_document(base_dir)
    assert doc.startswith("# GMRTI — General Method for Refinement and Transmission of Ideas")
    assert "**0.4 Vocabulary**" in doc
    assert "SECTION 1 — The Problem the GMRTI Addresses" in doc
    assert "SECTION 7 — Relation to Downstream Applications" in doc

def test_assemble_monolithic_missing_file_fails(tmp_path):
    # Empty dir should raise FileNotFoundError
    with pytest.raises(FileNotFoundError):
        assemble_monolithic_document(str(tmp_path))

def test_archive_prior_monolithic_files(tmp_path):
    # Create simulated root directory with multiple monolithic revisions
    base_dir = tmp_path / "workspace"
    base_dir.mkdir()
    (base_dir / "GMRTI_1000000001.md").write_text("rev 1", encoding="utf-8")
    (base_dir / "GMRTI_1000000002.md").write_text("rev 2", encoding="utf-8")
    current_output = base_dir / "GMRTI_1000000003.md"
    current_output.write_text("rev 3", encoding="utf-8")

    archived = archive_prior_monolithic_files(str(base_dir), current_output_path=str(current_output))
    assert len(archived) == 2
    assert "GMRTI_1000000001.md" in archived
    assert "GMRTI_1000000002.md" in archived

    archive_dir = base_dir / "archive"
    assert (archive_dir / "GMRTI_1000000001.md").exists()
    assert (archive_dir / "GMRTI_1000000002.md").exists()
    assert current_output.exists()
