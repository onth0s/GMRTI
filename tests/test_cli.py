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


@pytest.mark.repo_state
def test_wrap_check_exits_zero():
    """wrap.py --check exits 0 on a clean, fully-wrapped repository."""
    result = run("wrap.py", "--check")
    assert result.returncode == 0, f"wrap.py --check failed:\n{result.stdout}\n{result.stderr}"


@pytest.mark.repo_state
def test_rewrite_check_exits_zero():
    """rewrite.py --check exits 0 when root monolithic doc is in sync."""
    result = run("rewrite.py", "--check")
    assert result.returncode == 0, f"rewrite.py --check failed:\n{result.stdout}\n{result.stderr}"


@pytest.mark.repo_state
def test_pebble_check_exits_zero():
    """pebble.py --check exits 0 when root PEBBLE.md is in sync."""
    result = run("pebble.py", "--check")
    assert result.returncode == 0, f"pebble.py --check failed:\n{result.stdout}\n{result.stderr}"


@pytest.mark.repo_state
def test_patch_index_check_exits_zero():
    """patch_index.py --check exits 0 when index.html invariants are satisfied."""
    result = run("patch_index.py", "--check")
    assert result.returncode == 0, f"patch_index.py --check failed:\n{result.stdout}\n{result.stderr}"


def test_rewrite_dry_run_exits_zero():
    """rewrite.py --dry-run exits 0."""
    result = run("rewrite.py", "--dry-run")
    assert result.returncode == 0, f"rewrite.py --dry-run failed:\n{result.stdout}\n{result.stderr}"
    assert "DRY RUN" in result.stdout


def test_pebble_dry_run_exits_zero():
    """pebble.py --dry-run exits 0 and emits a DRY RUN message."""
    result = run("pebble.py", "--dry-run")
    assert result.returncode == 0, f"pebble.py --dry-run failed:\n{result.stdout}\n{result.stderr}"
    assert "DRY RUN" in result.stdout


def test_wrap_dry_run_exits_zero():
    """wrap.py --dry-run exits 0."""
    result = run("wrap.py", "--dry-run")
    assert result.returncode == 0, f"wrap.py --dry-run failed:\n{result.stdout}\n{result.stderr}"


def test_wrap_path_and_width_cli(tmp_path):
    """wrap.py --path <file> --width <N> formats a specific target file to given width."""
    long_content = (
        "This is a single very long sentence in prose that will definitely "
        "exceed thirty characters when written out.\n"
    )
    target = tmp_path / "custom.md"
    target.write_text(long_content, encoding="utf-8")

    check_res = run("wrap.py", "--path", str(target), "--width", "35", "--check")
    assert check_res.returncode == 1

    format_res = run("wrap.py", "--path", str(target), "--width", "35")
    assert format_res.returncode == 0

    check_res2 = run("wrap.py", "--path", str(target), "--width", "35", "--check")
    assert check_res2.returncode == 0


def test_wrap_missing_path_exits_nonzero(tmp_path):
    """wrap.py --path on nonexistent path exits 1."""
    res = run("wrap.py", "--path", str(tmp_path / "missing.md"))
    assert res.returncode == 1


def test_rewrite_output_error_exits_nonzero(tmp_path):
    """rewrite.py --output to an invalid directory exits 1."""
    bad_out = tmp_path / "no_such_dir" / "out.md"
    res = run("rewrite.py", "--output", str(bad_out))
    assert res.returncode == 1


def test_pebble_output_error_exits_nonzero(tmp_path):
    """pebble.py --output to an invalid directory exits 1."""
    bad_out = tmp_path / "no_such_dir" / "pebble.md"
    res = run("pebble.py", "--output", str(bad_out))
    assert res.returncode == 1


@pytest.mark.repo_state
def test_inprocess_cli_check_mains(monkeypatch):
    """Verify in-process CLI main() entrypoints for --check against live repo."""
    import patch_index
    import pebble
    import rewrite
    import wrap

    for mod, argv in [
        (wrap, ["wrap.py", "--check"]),
        (rewrite, ["rewrite.py", "--check"]),
        (pebble, ["pebble.py", "--check"]),
        (patch_index, ["patch_index.py", "--check"]),
    ]:
        monkeypatch.setattr(sys, "argv", argv)
        with pytest.raises(SystemExit) as exc:
            mod.main()
        assert exc.value.code == 0


def test_inprocess_cli_dry_run_mains(monkeypatch):
    """Verify in-process CLI main() entrypoints for --dry-run."""
    import patch_index
    import pebble
    import rewrite
    import wrap

    for mod, argv in [
        (wrap, ["wrap.py", "--dry-run"]),
        (rewrite, ["rewrite.py", "--dry-run"]),
        (pebble, ["pebble.py", "--dry-run"]),
        (patch_index, ["patch_index.py", "--dry-run"]),
    ]:
        monkeypatch.setattr(sys, "argv", argv)
        mod.main()

