"""_gmrti_common.py — Shared constants and UTF-8/LF file helpers for GMRTI scripts."""
import os
import re

MONOLITHIC_PATTERN = re.compile(r"^GMRTI_\d+\.md$")


def get_repo_root(anchor_file: str | None = None) -> str:
    """Return the absolute repository root directory."""
    target = anchor_file if anchor_file is not None else __file__
    return os.path.dirname(os.path.abspath(target))


def read_utf8(filepath: str) -> str:
    """Read a UTF-8 text file with universal newline normalization."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_utf8(filepath: str, content: str) -> None:
    """Write a UTF-8 text file using canonical LF line endings."""
    with open(filepath, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def list_monolithic_files(base_dir: str) -> list[str]:
    """Return a sorted list of monolithic revision filenames in *base_dir*."""
    return sorted(
        f for f in os.listdir(base_dir) if MONOLITHIC_PATTERN.match(f)
    )
