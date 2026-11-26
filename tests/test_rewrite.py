import os
import shutil
import pytest
from rewrite import (
    _list_monolithic_files,
    assemble_monolithic_document,
    archive_prior_monolithic_files,
    check_monolithic_sync,
    create_monolithic_document,
)
from _gmrti_common import MONOLITHIC_PATTERN

_COPY_IGNORE = shutil.ignore_patterns(
    "math", "archive", "index.html", ".git", ".pytest_cache", "__pycache__"
)


def test_assemble_monolithic_document_success(base_dir):
    doc = assemble_monolithic_document(base_dir)
    assert doc.startswith('---\ntitle: "GMRTI')
    assert 'kicker: "There must be a Science of Understanding"' in doc
    assert "# GMRTI \u2014 General Method for Refinement and Transmission of Ideas" in doc
    assert "**0.4 Vocabulary**" in doc
    assert "SECTION 1 \u2014 The Problem the GMRTI Addresses" in doc
    assert "SECTION 7 \u2014 Relation to Downstream Applications" in doc
    assert "SECTION 8 \u2014 Known Gaps and Open Challenges" in doc
    assert "## APPENDIX A \u2014 Architectural Model" in doc
    assert "## APPENDIX M \u2014 Methodology & Status Markers" in doc
    assert "## APPENDIX R \u2014 The Refinement Cycle" in doc


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

    archived = archive_prior_monolithic_files(
        str(base_dir), current_output_path=str(current_output)
    )
    assert len(archived) == 2
    assert "GMRTI_1000000001.md" in archived
    assert "GMRTI_1000000002.md" in archived

    archive_dir = base_dir / "archive"
    assert (archive_dir / "GMRTI_1000000001.md").exists()
    assert (archive_dir / "GMRTI_1000000002.md").exists()
    assert current_output.exists()


def test_archive_prior_monolithic_files_deduplicates(tmp_path):
    """Byte-identical prior monoliths are not duplicated in archive/."""
    base_dir = tmp_path / "workspace"
    archive_dir = base_dir / "archive"
    archive_dir.mkdir(parents=True)
    (archive_dir / "GMRTI_1000000001.md").write_text("same content", encoding="utf-8")
    (base_dir / "GMRTI_1000000002.md").write_text("same content", encoding="utf-8")
    current_output = base_dir / "GMRTI_1000000003.md"
    current_output.write_text("new content", encoding="utf-8")

    archived = archive_prior_monolithic_files(
        str(base_dir), current_output_path=str(current_output)
    )
    assert archived == []
    assert not (base_dir / "GMRTI_1000000002.md").exists()
    assert not (archive_dir / "GMRTI_1000000002.md").exists()


@pytest.mark.repo_state
def test_check_monolithic_sync_in_sync(base_dir):
    """check_monolithic_sync returns in_sync=True when root monolithic file matches sources."""
    result = check_monolithic_sync(base_dir)
    assert isinstance(result, dict)
    assert result["in_sync"] is True
    assert result["error"] is None
    assert result["mono_file"] is not None


def test_check_monolithic_sync_missing_and_multiple(tmp_path):
    """check_monolithic_sync reports errors when 0 or >1 monoliths exist in root."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    res_none = check_monolithic_sync(str(empty_dir))
    assert res_none["in_sync"] is False
    assert "No monolithic revision" in res_none["error"]

    (empty_dir / "GMRTI_1.md").write_text("a", encoding="utf-8")
    (empty_dir / "GMRTI_2.md").write_text("b", encoding="utf-8")
    res_multi = check_monolithic_sync(str(empty_dir))
    assert res_multi["in_sync"] is False
    assert "multiple monolithic files" in res_multi["error"]


def test_check_monolithic_sync_out_of_sync(tmp_path, base_dir):
    """check_monolithic_sync returns in_sync=False when monolithic file content differs from assembled."""
    workspace = tmp_path / "workspace"
    shutil.copytree(base_dir, str(workspace), dirs_exist_ok=True, ignore=_COPY_IGNORE)
    mono_files = [f for f in os.listdir(str(workspace)) if MONOLITHIC_PATTERN.match(f)]
    assert mono_files, "Fixture copy produced no monolithic file — test cannot proceed."
    mono_path = workspace / mono_files[0]
    mono_path.write_text("CORRUPTED CONTENT", encoding="utf-8")
    result = check_monolithic_sync(str(workspace))
    assert isinstance(result, dict)
    assert result["in_sync"] is False


def test_create_monolithic_document_dry_run_and_idempotent(tmp_path, base_dir):
    """dry_run=True writes nothing; create_monolithic_document skips when already in sync."""
    workspace = tmp_path / "workspace"
    shutil.copytree(base_dir, str(workspace), dirs_exist_ok=True, ignore=_COPY_IGNORE)
    before_files = set(os.listdir(str(workspace)))
    out_path = create_monolithic_document(base_dir=str(workspace), dry_run=True)
    after_files = set(os.listdir(str(workspace)))
    assert before_files == after_files, "dry_run should not create any files"
    assert out_path.endswith(".md")

    # Idempotent run when already in sync returns existing monolith without archiving
    skipped_path = create_monolithic_document(base_dir=str(workspace))
    assert os.path.basename(skipped_path) in before_files
    assert not (workspace / "archive").exists()

    # Force recompilation writes a target and archives prior
    forced_out = workspace / "GMRTI_9999999999.md"
    create_monolithic_document(base_dir=str(workspace), output_path=str(forced_out), force=True)
    assert forced_out.exists()
    assert (workspace / "archive").exists()


def test_list_monolithic_files_helper(tmp_path):
    """_list_monolithic_files correctly discovers and sorts GMRTI_<digits>.md files."""
    (tmp_path / "GMRTI_1002.md").write_text("rev 2", encoding="utf-8")
    (tmp_path / "GMRTI_1001.md").write_text("rev 1", encoding="utf-8")
    (tmp_path / "README.md").write_text("readme", encoding="utf-8")
    (tmp_path / "GMRTI_notdigits.md").write_text("invalid", encoding="utf-8")
    found = _list_monolithic_files(str(tmp_path))
    assert found == ["GMRTI_1001.md", "GMRTI_1002.md"]


def test_assemble_monolithic_heading_transform_failure(tmp_path, base_dir):
    """ValueError is raised if a required heading transform does not find exactly 1 match."""
    workspace = tmp_path / "workspace"
    shutil.copytree(base_dir, str(workspace), dirs_exist_ok=True, ignore=_COPY_IGNORE)
    glossary_path = workspace / "GLOSSARY.md"
    content = glossary_path.read_text(encoding="utf-8")
    glossary_path.write_text(
        content.replace("# Glossary", "# RemovedHeading"), encoding="utf-8"
    )
    with pytest.raises(ValueError, match="Heading transform failed"):
        assemble_monolithic_document(str(workspace))


def test_custom_output_does_not_archive_root_monolith(tmp_path, base_dir):
    """B1: Writing to --output outside root monolith pattern must not archive root monolith."""
    workspace = tmp_path / "workspace"
    shutil.copytree(base_dir, str(workspace), dirs_exist_ok=True, ignore=_COPY_IGNORE)
    root_monos_before = _list_monolithic_files(str(workspace))
    assert len(root_monos_before) == 1

    custom_out = tmp_path / "custom_build.md"
    create_monolithic_document(
        base_dir=str(workspace), output_path=str(custom_out), force=True
    )
    assert custom_out.exists()
    assert _list_monolithic_files(str(workspace)) == root_monos_before
    assert check_monolithic_sync(str(workspace))["in_sync"] is True


def test_archive_collision_different_content_raises(tmp_path):
    """B2: Colliding archive filename with different content raises FileExistsError."""
    workspace = tmp_path / "workspace"
    archive_dir = workspace / "archive"
    archive_dir.mkdir(parents=True)
    (archive_dir / "GMRTI_100.md").write_text("old archived", encoding="utf-8")
    (workspace / "GMRTI_100.md").write_text("different root", encoding="utf-8")

    with pytest.raises(FileExistsError, match="Archive collision"):
        archive_prior_monolithic_files(str(workspace))


def test_missing_readme_toc_anchor_raises(tmp_path, base_dir):
    """B3: Missing '## Table of Contents' anchor in README raises ValueError."""
    workspace = tmp_path / "workspace"
    shutil.copytree(base_dir, str(workspace), dirs_exist_ok=True, ignore=_COPY_IGNORE)
    (workspace / "README.md").write_text("# GMRTI\n\nNo TOC here.\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Table of Contents"):
        assemble_monolithic_document(str(workspace))


def test_rewrite_check_handles_missing_source_cleanly(tmp_path):
    """B4: rewrite.py --check exits 1 cleanly instead of crashing with traceback."""
    import subprocess
    import sys

    # Point a copy of rewrite.py? Easier: call main() in-process with monkeypatched get_repo_root
    # or test check_monolithic_sync + CLI error path via a small runner.
    code = (
        "import sys, rewrite; "
        f"rewrite.get_repo_root = lambda _=None: {str(tmp_path)!r}; "
        "sys.argv = ['rewrite.py', '--check']; "
        "rewrite.main()"
    )
    (tmp_path / "GMRTI_1.md").write_text("stale", encoding="utf-8")
    res = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert res.returncode == 1
    assert "Error during check:" in res.stdout
    assert "Traceback" not in res.stderr
