"""rewrite.py — Monolithic treatise compilation and synchronization engine for GMRTI.

Assembles modular Markdown sources from ``src/``, root governance documents
(``ARCHITECTURE.md``, ``METHODOLOGY.md``, ``REFINEMENT.md``), and ``GLOSSARY.md``
into the unified monolithic treatise ``GMRTI_<timestamp>.md``.

Manages monolithic revision archival in ``archive/`` per AGENTS.md rules
and verifies synchronization between modular sources and root monolithic document.
"""
import argparse
import hashlib
import os
import re
import shutil
import sys
import time

from _gmrti_common import (
    ASSEMBLY_MANIFEST,
    MONOLITHIC_PATTERN,
    SyncResult,
    build_base_parser,
    exit_for_check,
    get_repo_root,
    list_monolithic_files,
    read_utf8,
    write_utf8,
)


def _file_sha256(filepath: str) -> str:
    """Return the SHA-256 hex digest of *filepath*."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


_MONOLITH_FRONTMATTER = """---
title: "GMRTI — General Method for Refinement and Transmission of Ideas"
kicker: "_There must be a Science of Understanding_"
subtitle: "A Living Framework Document · Tenth Iteration (v0.9)"
pills:
  - "epistemology"
  - "semantic-covenants"
  - "transmission"
  - "polyphonic-encoding"
  - "rational-agnosticism"
  - "v0.9"
theme: "dark"
accent: "#3b82f6"
---"""


def assemble_monolithic_document(base_dir: str) -> str:
    readme_path = os.path.join(base_dir, "README.md")
    if not os.path.exists(readme_path):
        raise FileNotFoundError(f"Missing root readme: {readme_path}")

    readme_content = read_utf8(readme_path)
    header_match = re.search(
        r"^(.*?)(?=\n## Table of Contents)", readme_content, re.DOTALL
    )
    if not header_match:
        raise ValueError(
            "README.md is missing '## Table of Contents' anchor."
        )
    header = header_match.group(1).strip()

    body_parts: list[str] = []

    for entry in ASSEMBLY_MANIFEST:
        rel_path = entry.path
        mode = entry.merge_mode
        filepath = os.path.join(base_dir, rel_path)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Critical source file missing: {filepath}")

        content = read_utf8(filepath).strip()

        transform = entry.heading_transform
        if transform:
            pattern, replacement = transform
            content, n = re.subn(
                pattern, replacement, content, flags=re.MULTILINE
            )
            if n != 1:
                raise ValueError(
                    f"Heading transform failed for {rel_path}: "
                    f"expected 1 match, got {n}."
                )

        if mode == "append" and body_parts:
            body_parts[-1] += "\n\n" + content
        else:
            body_parts.append(content)

    body_text = "\n\n---\n\n".join(body_parts)
    return _MONOLITH_FRONTMATTER + "\n\n" + header + "\n\n" + body_text + "\n"


_ARCHIVE_RETENTION = 10


def archive_prior_monolithic_files(
    base_dir: str, current_output_path: str | None = None
) -> list[str]:
    """Enforce AGENTS.md rule: keep only the latest monolith in root.

    Moves prior root revisions to ``archive/``, deduplicating byte-identical
    files and retaining at most ``_ARCHIVE_RETENTION`` unique revisions.
    """
    archive_dir = os.path.join(base_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    archived_hashes: dict[str, str] = {}
    for af in list_monolithic_files(archive_dir):
        af_path = os.path.join(archive_dir, af)
        h = _file_sha256(af_path)
        if h in archived_hashes:
            os.remove(af_path)
            print(f"Removed duplicate archive revision: {af}")
        else:
            archived_hashes[h] = af

    archived_files: list[str] = []
    for f in list_monolithic_files(base_dir):
        full_path = os.path.join(base_dir, f)
        if (
            current_output_path
            and os.path.abspath(full_path)
            == os.path.abspath(current_output_path)
        ):
            continue
        file_hash = _file_sha256(full_path)
        if file_hash in archived_hashes:
            os.remove(full_path)
            print(f"Removed duplicate monolithic revision: {f} (already in archive/)")
        else:
            dest_path = os.path.join(archive_dir, f)
            if os.path.exists(dest_path) and _file_sha256(dest_path) != file_hash:
                raise FileExistsError(
                    f"Archive collision: {dest_path} already exists with different content."
                )
            shutil.move(full_path, dest_path)
            archived_hashes[file_hash] = f
            archived_files.append(f)
            print(f"Archived prior monolithic revision: {f} -> archive/{f}")

    all_archived = list_monolithic_files(archive_dir)
    if len(all_archived) > _ARCHIVE_RETENTION:
        for old_f in all_archived[:-_ARCHIVE_RETENTION]:
            os.remove(os.path.join(archive_dir, old_f))
            print(f"Pruned expired archive revision: {old_f}")

    return archived_files


def check_monolithic_sync(base_dir: str) -> SyncResult:
    """Check whether the root monolithic document matches the current sources.

    Returns a dict with keys: in_sync (bool), mono_file (str|None),
    error (str|None).
    """
    mono_files = list_monolithic_files(base_dir)

    if not mono_files:
        return {
            "in_sync": False,
            "mono_file": None,
            "error": "No monolithic revision found in root.",
        }

    if len(mono_files) > 1:
        return {
            "in_sync": False,
            "mono_file": None,
            "error": f"Rule violation: multiple monolithic files in root: {mono_files}",
        }

    latest = mono_files[0]
    latest_path = os.path.join(base_dir, latest)
    existing_content = read_utf8(latest_path)

    assembled = assemble_monolithic_document(base_dir)
    in_sync = existing_content == assembled
    return {"in_sync": in_sync, "mono_file": latest, "error": None}


def create_monolithic_document(
    base_dir: str | None = None,
    output_path: str | None = None,
    dry_run: bool = False,
    archive: bool = True,
    force: bool = False,
) -> str:
    if base_dir is None:
        base_dir = get_repo_root(__file__)

    assembled = assemble_monolithic_document(base_dir)

    if output_path is None and not force:
        mono_files = list_monolithic_files(base_dir)
        if len(mono_files) == 1:
            existing_path = os.path.join(base_dir, mono_files[0])
            if read_utf8(existing_path) == assembled:
                prefix = "[DRY RUN] " if dry_run else ""
                print(
                    f"{prefix}Root monolithic document {mono_files[0]} "
                    "is already in sync; skipping compilation."
                )
                return existing_path

    is_root_monolith = output_path is None or (
        os.path.dirname(os.path.abspath(output_path)) == os.path.abspath(base_dir)
        and bool(MONOLITHIC_PATTERN.match(os.path.basename(output_path)))
    )

    epoch_time = int(time.time())
    if output_path is None:
        output_path = os.path.join(base_dir, f"GMRTI_{epoch_time}.md")

    if dry_run:
        print(
            f"[DRY RUN] Would compile monolithic document to: "
            f"{output_path} ({len(assembled)} bytes)"
        )
        if archive and is_root_monolith:
            prior = list_monolithic_files(base_dir)
            if prior:
                print(f"[DRY RUN] Would archive prior revisions: {prior}")
        return output_path

    write_utf8(output_path, assembled)
    if archive and is_root_monolith:
        archive_prior_monolithic_files(
            base_dir, current_output_path=output_path
        )
    print(f"Monolithic document created at: {output_path}")
    return output_path


def main() -> None:
    parser = build_base_parser(
        description="Compile modular GMRTI treatise into monolithic document.",
        check_help="Check if root monolithic document is in sync.",
        dry_run_help="Simulate compilation and archival without writing.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output filepath.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Recompile even if the root monolithic document is already in sync.",
    )

    args = parser.parse_args()
    base_dir = get_repo_root(__file__)

    if args.check:
        try:
            result = check_monolithic_sync(base_dir)
        except (FileNotFoundError, OSError, ValueError) as e:
            print(f"Error during check: {e}")
            sys.exit(1)
        if result["error"]:
            exit_for_check(False, "", result["error"])
        exit_for_check(
            result["in_sync"],
            f"Root monolithic document {result['mono_file']} is fully in sync.",
            f"Root monolithic document {result['mono_file']} is OUT OF SYNC with source files.",
        )

    try:
        create_monolithic_document(
            base_dir=base_dir,
            output_path=args.output,
            dry_run=args.dry_run,
            force=args.force,
        )
    except (FileNotFoundError, OSError, ValueError) as e:
        print(f"Error during compilation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
