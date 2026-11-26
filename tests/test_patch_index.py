import subprocess
import sys

from patch_index import patch_html, process_index_file


SAMPLE_UNPATCHED = (
    "<!doctype html><html><head>"
    "<style>"
    ":root{--accent:#3b82f6}"
    ".toolbar{display:flex;gap:8px;min-width:0}"
    ".katex-display{overflow-x:auto}"
    "</style>"
    "</head><body><p>Hello</p></body></html>"
)


def test_patch_html_applies_all_invariants():
    patched = patch_html(SAMPLE_UNPATCHED)
    assert "--svg-min-w:0px;" in patched
    assert ".toolbar{display:flex;gap:8px;min-width:0;flex:none}" in patched
    assert ".katex--overflow{" in patched
    assert "function fitInlineMath()" in patched
    assert 'addEventListener("resize"' in patched


def test_patch_html_is_idempotent():
    once = patch_html(SAMPLE_UNPATCHED)
    twice = patch_html(once)
    assert once == twice


def test_process_index_file_dry_run_and_check(tmp_path):
    target = tmp_path / "index.html"
    target.write_text(SAMPLE_UNPATCHED, encoding="utf-8")

    assert process_index_file(str(target), check_only=True) is True
    assert process_index_file(str(target), dry_run=True) is True
    assert target.read_text(encoding="utf-8") == SAMPLE_UNPATCHED

    assert process_index_file(str(target)) is True
    assert process_index_file(str(target), check_only=True) is False


def test_patch_index_cli_check_and_missing_file(tmp_path):
    target = tmp_path / "index.html"
    target.write_text(SAMPLE_UNPATCHED, encoding="utf-8")

    res_fail = subprocess.run(
        [sys.executable, "patch_index.py", "--path", str(target), "--check"],
        capture_output=True,
        text=True,
    )
    assert res_fail.returncode == 1

    res_fix = subprocess.run(
        [sys.executable, "patch_index.py", "--path", str(target)],
        capture_output=True,
        text=True,
    )
    assert res_fix.returncode == 0

    res_ok = subprocess.run(
        [sys.executable, "patch_index.py", "--path", str(target), "--check"],
        capture_output=True,
        text=True,
    )
    assert res_ok.returncode == 0

    res_missing = subprocess.run(
        [sys.executable, "patch_index.py", "--path", str(tmp_path / "nope.html")],
        capture_output=True,
        text=True,
    )
    assert res_missing.returncode == 1
