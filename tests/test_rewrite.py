import os
import shutil
import pytest
from rewrite import (
    assemble_monolithic_document,
    archive_prior_monolithic_files,
    check_monolithic_sync,
    create_monolithic_document,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_assemble_monolithic_document_success():
    doc = assemble_monolithic_document(BASE_DIR)
    assert doc.startswith("# GMRTI \u2014 General Method for Refinement and Transmission of Ideas")
    assert "**0.4 Vocabulary**" in doc
    assert "SECTION 1 \u2014 The Problem the GMRTI Addresses" in doc
    assert "SECTION 7 \u2014 Relation to Downstream Applications" in doc
    assert "SECTION 8 \u2014 Known Gaps and Open Challenges" in doc



def test_assemble_monolithic_missing_file_fails(tmp_path):
    with pytest.raises(FileNotFoundError):
        assemble_monolithic_document(str(tmp_path))


def test_archive_prior_monolithic_files(tmp_path):
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


def test_check_monolithic_sync_in_sync():
    """check_monolithic_sync returns in_sync=True when root monolithic file matches sources."""
    result = check_monolithic_sync(BASE_DIR)
    assert isinstance(result, dict)
    assert result["in_sync"] is True
    assert result["error"] is None
    assert result["mono_file"] is not None


def test_check_monolithic_sync_out_of_sync(tmp_path):
    """check_monolithic_sync returns in_sync=False when monolithic file content differs from assembled."""
    base_dir = tmp_path / "workspace"
    shutil.copytree(BASE_DIR, str(base_dir), dirs_exist_ok=True)
    # Corrupt the monolithic file
    mono_files = [f for f in os.listdir(str(base_dir)) if f.startswith("GMRTI_") and f.endswith(".md")]
    if mono_files:
        mono_path = base_dir / mono_files[0]
        mono_path.write_text("CORRUPTED CONTENT", encoding="utf-8")
        result = check_monolithic_sync(str(base_dir))
        assert isinstance(result, dict)
        assert result["in_sync"] is False



def test_create_monolithic_document_dry_run(tmp_path):
    """dry_run=True returns an output path but writes nothing."""
    base_dir = tmp_path / "workspace"
    shutil.copytree(BASE_DIR, str(base_dir), dirs_exist_ok=True)
    before_files = set(os.listdir(str(base_dir)))
    out_path = create_monolithic_document(base_dir=str(base_dir), dry_run=True)
    after_files = set(os.listdir(str(base_dir)))
    assert before_files == after_files, "dry_run should not create any files"
    assert out_path.endswith(".md")
