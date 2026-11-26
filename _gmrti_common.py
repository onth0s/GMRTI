"""_gmrti_common.py — Shared constants, manifest, CLI, and atomic UTF-8/LF helpers."""
import argparse
from dataclasses import dataclass
import os
import re
import sys
import tempfile
from typing import NoReturn, TypedDict

MONOLITHIC_PATTERN = re.compile(r"^GMRTI_\d+\.md$")
_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


def parse_code_fence(stripped: str) -> tuple[str, int] | None:
    """Return (fence_char, count) if *stripped* starts with 3+ backticks or tildes."""
    m = _FENCE_RE.match(stripped)
    if m:
        seq = m.group(1)
        return seq[0], len(seq)
    return None


@dataclass
class CodeFenceTracker:
    """Stateful tracker for fenced code blocks (backticks or tildes, >=3 chars)."""

    in_fence: bool = False
    fence_char: str = ""
    fence_len: int = 0

    def step(self, line: str) -> tuple[bool, bool]:
        """Advance state by *line*.

        Returns ``(is_fence_line, inside_fence_body)`` where *is_fence_line* is
        True on the opening or closing fence line itself, and *inside_fence_body*
        is True for lines inside an open fence (excluding the fence lines).
        """
        stripped = line.strip()
        fence = parse_code_fence(stripped)
        if fence:
            f_char, f_count = fence
            if not self.in_fence:
                self.in_fence = True
                self.fence_char = f_char
                self.fence_len = f_count
                return True, False
            is_pure_fence = all(c == self.fence_char for c in stripped)
            if is_pure_fence and f_char == self.fence_char and f_count >= self.fence_len:
                self.in_fence = False
                self.fence_char = ""
                self.fence_len = 0
                return True, False
        return False, self.in_fence


def extract_wikilinks(text: str) -> list[str]:
    """Extract normalized ``[[target]]`` / ``[[target|display]]`` targets from *text*."""
    targets: list[str] = []
    for raw_target in _WIKILINK_RE.findall(text):
        normalized = re.sub(r"\s+", " ", raw_target).strip().rstrip("\\").strip()
        if normalized:
            targets.append(normalized)
    return targets


@dataclass(frozen=True)
class ManifestEntry:
    """One entry in the canonical GMRTI treatise assembly sequence."""

    path: str
    merge_mode: str = "separator"
    heading_transform: tuple[str, str] | None = None


class SyncResult(TypedDict, total=False):
    """Result dict returned by sync-checking functions."""

    in_sync: bool
    error: str | None
    mono_file: str | None


ASSEMBLY_MANIFEST: tuple[ManifestEntry, ...] = (
    ManifestEntry(path="src/00_preamble.md"),
    ManifestEntry(path="src/01_problem.md"),
    ManifestEntry(path="src/02_architecture.md"),
    ManifestEntry(path="src/03_algorithm.md"),
    ManifestEntry(path="src/04_temporal_anchoring.md"),
    ManifestEntry(path="src/05_metalanguage.md"),
    ManifestEntry(path="src/06_refinement_vectors.md"),
    ManifestEntry(path="src/07_downstream.md"),
    ManifestEntry(path="src/08_gaps.md"),
    ManifestEntry(path="src/09_coda.md"),
    ManifestEntry(
        path="ARCHITECTURE.md",
        heading_transform=(
            r"^#\s+GMRTI Architectural Model\b",
            "## APPENDIX A — Architectural Model",
        ),
    ),
    ManifestEntry(
        path="METHODOLOGY.md",
        heading_transform=(
            r"^#\s+GMRTI Methodology & Status Markers\b",
            "## APPENDIX M — Methodology & Status Markers",
        ),
    ),
    ManifestEntry(
        path="REFINEMENT.md",
        heading_transform=(
            r"^#\s+The Refinement Cycle\b",
            "## APPENDIX R — The Refinement Cycle",
        ),
    ),
    ManifestEntry(
        path="GLOSSARY.md",
        heading_transform=(
            r"^#\s+Glossary\b",
            "## APPENDIX G — Glossary",
        ),
    ),
)


def get_repo_root(anchor_file: str | None = None) -> str:
    """Return the absolute repository root directory."""
    target = anchor_file if anchor_file is not None else __file__
    return os.path.dirname(os.path.abspath(target))


def read_utf8(filepath: str) -> str:
    """Read a UTF-8 text file with universal newline normalization."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def write_utf8(filepath: str, content: str) -> None:
    """Atomically write a UTF-8 text file using canonical LF line endings."""
    abs_path = os.path.abspath(filepath)
    parent = os.path.dirname(abs_path)
    if not os.path.isdir(parent):
        raise FileNotFoundError(f"Parent directory does not exist: {parent}")

    fd, tmp_path = tempfile.mkstemp(prefix=".gmrti_tmp_", dir=parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        os.replace(tmp_path, abs_path)
    except Exception:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def list_monolithic_files(base_dir: str) -> list[str]:
    """Return a sorted list of monolithic revision filenames in *base_dir*."""
    return sorted(
        f for f in os.listdir(base_dir) if MONOLITHIC_PATTERN.match(f)
    )


def build_base_parser(
    description: str, check_help: str, dry_run_help: str
) -> argparse.ArgumentParser:
    """Create an ArgumentParser with standard --check and --dry-run flags."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--check", action="store_true", help=check_help)
    parser.add_argument("--dry-run", action="store_true", help=dry_run_help)
    return parser


def exit_for_check(ok: bool, ok_msg: str, fail_msg: str) -> NoReturn:
    """Print status message for --check mode and exit with 0 or 1."""
    print(ok_msg if ok else fail_msg)
    sys.exit(0 if ok else 1)
