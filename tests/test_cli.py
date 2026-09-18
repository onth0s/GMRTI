import os
import subprocess
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON = sys.executable


def run(script, *args):
    return subprocess.run(
        [PYTHON, script] + list(args),
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )


def test_wrap_check_exits_zero():
    """wrap.py --check exits 0 on a clean, fully-wrapped repository."""
    result = run("wrap.py", "--check")
    assert result.returncode == 0, f"wrap.py --check failed:\n{result.stdout}\n{result.stderr}"


def test_rewrite_check_exits_zero():
    """rewrite.py --check exits 0 when root monolithic doc is in sync."""
    result = run("rewrite.py", "--check")
    assert result.returncode == 0, f"rewrite.py --check failed:\n{result.stdout}\n{result.stderr}"


def test_rewrite_dry_run_exits_zero():
    """rewrite.py --dry-run exits 0 and emits a DRY RUN message."""
    result = run("rewrite.py", "--dry-run")
    assert result.returncode == 0, f"rewrite.py --dry-run failed:\n{result.stdout}\n{result.stderr}"
    assert "DRY RUN" in result.stdout, "Expected '[DRY RUN]' in output"


def test_wrap_dry_run_exits_zero():
    """wrap.py --dry-run exits 0."""
    result = run("wrap.py", "--dry-run")
    assert result.returncode == 0, f"wrap.py --dry-run failed:\n{result.stdout}\n{result.stderr}"


def test_wrap_path_and_width_cli(tmp_path):
    """wrap.py --path <file> --width <N> formats a specific target file to given width."""
    long_content = "This is a single very long sentence in prose that will definitely exceed thirty characters when written out.\n"
    target = tmp_path / "custom.md"
    target.write_text(long_content, encoding="utf-8")

    # Verify --check detects it
    check_res = run("wrap.py", "--path", str(target), "--width", "35", "--check")
    assert check_res.returncode == 1

    # Now format it
    format_res = run("wrap.py", "--path", str(target), "--width", "35")
    assert format_res.returncode == 0

    # Verify now clean
    check_res2 = run("wrap.py", "--path", str(target), "--width", "35", "--check")
    assert check_res2.returncode == 0
