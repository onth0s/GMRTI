"""wrap.py — Markdown and YAML line-width formatter for GMRTI.

Reformats source files in ``src/``, ``specs/``, and ``refinery/`` (plus root
markdown files) to a canonical line width (default 80 characters).

Block-type taxonomy handled by the Markdown wrapper
----------------------------------------------------
- ``table``         — pipe-delimited table rows; passed through verbatim.
- ``quote``         — blockquote paragraphs (``> …``); joined and reflowed.
- ``footnote``      — footnote definitions (``[^n]: …``); reflowed with hanging
                      indent.
- ``list_item``     — ordered/unordered list items; reflowed with continuation
                      indent matching the list marker width.
- ``indented_line`` — indented continuation lines; reflowed preserving indent.
- ``prose``         — plain paragraph text; reflowed freely.

Code blocks (``` or ````) and display-math blocks (``$$`` fence or single-line
``$$...$$``) are always passed through verbatim.

Invocation
----------
    python wrap.py                    # format all tracked files in-place
    python wrap.py --check            # check without writing; exit 1 if any
                                      # file needs reformatting
    python wrap.py --dry-run          # report which files would change
    python wrap.py --path <file|dir>  # target a specific file or directory
    python wrap.py --width N          # use a custom line width (default 80)
"""
import argparse
import os
import re
import sys
import textwrap

from _gmrti_common import (
    MONOLITHIC_PATTERN,
    get_repo_root,
    read_utf8,
    write_utf8,
)

# ── Block-type constants ────────────────────────────────────────────────────

_TABLE = "table"
_QUOTE = "quote"
_FOOTNOTE = "footnote"
_LIST_ITEM = "list_item"
_INDENTED = "indented_line"
_PROSE = "prose"

_MIN_WRAP_WIDTH = 10


# ── YAML wrapper ────────────────────────────────────────────────────────────

def _wrap_yaml_scalar(text: str, target_width: int) -> list[str]:
    """Wrap YAML scalar/comment text safely without splitting words/hyphens."""
    return textwrap.wrap(
        text,
        width=max(_MIN_WRAP_WIDTH, target_width),
        break_long_words=False,
        break_on_hyphens=False,
    )


def wrap_yaml(text: str, width: int = 80) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        if len(line) <= width:
            lines.append(line)
            continue

        # 1. Key-value string replacement with quotes: key: "value..."
        key_match = re.match(r'^(\s*)([\w-]+):\s*"((?:[^"\\]|\\.)*)"$', line)
        if key_match:
            indent, key, raw_val = key_match.groups()
            val = raw_val.replace('\\"', '"')
            wrapped_val = _wrap_yaml_scalar(val, width - len(indent) - 2)
            lines.append(f"{indent}{key}: >-")
            for wl in wrapped_val:
                lines.append(f"{indent}  {wl}")
            continue

        # 2. Key-value unquoted long string: key: value...
        # Exclude flow mappings/sequences ({...}, [...]) from block-scalar conversion
        key_unquoted = re.match(r'^(\s*)([\w-]+):\s+([^\">|#{\[\s].*)$', line)
        if key_unquoted and not line.strip().startswith("-"):
            indent, key, val = key_unquoted.groups()
            wrapped_val = _wrap_yaml_scalar(val, width - len(indent) - 2)
            lines.append(f"{indent}{key}: >-")
            for wl in wrapped_val:
                lines.append(f"{indent}  {wl}")
            continue

        # 3. List item string replacement with quotes: - "value..."
        list_match = re.match(r'^(\s*)-\s*"((?:[^"\\]|\\.)*)"$', line)
        if list_match:
            indent, raw_val = list_match.groups()
            val = raw_val.replace('\\"', '"')
            wrapped_val = _wrap_yaml_scalar(val, width - len(indent) - 4)
            lines.append(f"{indent}- >-")
            for wl in wrapped_val:
                lines.append(f"{indent}    {wl}")
            continue

        # 4a. List item mapping: - key: value...
        list_mapping = re.match(r'^(\s*-\s+)([\w-]+):\s+([^\">|#{\[\s].*)$', line)
        if list_mapping:
            list_prefix, key, val = list_mapping.groups()
            sub_indent = " " * len(list_prefix) + "  "
            wrapped_val = _wrap_yaml_scalar(val, width - len(sub_indent))
            lines.append(f"{list_prefix}{key}: >-")
            for wl in wrapped_val:
                lines.append(f"{sub_indent}{wl}")
            continue

        # 4b. List item unquoted long string: - value...
        # Exclude flow collections ({...}, [...]) and list-of-mappings (- key: val)
        list_unquoted = re.match(r'^(\s*)-\s+([^\">|#{\[\s].*)$', line)
        if list_unquoted and not re.match(r"^[\w-]+:(?:\s|$)", list_unquoted.group(2)):
            indent, val = list_unquoted.groups()
            wrapped_val = _wrap_yaml_scalar(val, width - len(indent) - 4)
            lines.append(f"{indent}- >-")
            for wl in wrapped_val:
                lines.append(f"{indent}    {wl}")
            continue

        # 5. Comment replacement
        comment_match = re.match(r"^(\s*)#\s*(.*)$", line)
        if comment_match:
            indent, val = comment_match.groups()
            wrapped_val = _wrap_yaml_scalar(val, width - len(indent) - 2)
            for wl in wrapped_val:
                lines.append(f"{indent}# {wl}")
            continue

        # 6. Fallback preserving existing indentation (crucial for block scalars)
        indent_len = len(line) - len(line.lstrip())
        indent = line[:indent_len]
        stripped = line.strip()
        for wl in _wrap_yaml_scalar(stripped, width - indent_len):
            lines.append(f"{indent}{wl}")

    return "\n".join(lines)


# ── Markdown block flusher ──────────────────────────────────────────────────

def _flush_block(
    block_type: str | None,
    para: list[str],
    prefix: str,
    indent: str,
    width: int,
) -> list[str]:
    """Return a list of output lines for one accumulated markdown block."""
    out: list[str] = []
    if not para:
        return out

    if block_type == _TABLE:
        out.extend(para)

    elif block_type == _QUOTE:
        stripped = [re.sub(r"^>\s*", "", ln) for ln in para]
        content = " ".join(stripped)
        wrapped = textwrap.wrap(
            content,
            width=max(_MIN_WRAP_WIDTH, width - 2),
            break_long_words=False,
            break_on_hyphens=False,
        )
        if not wrapped:
            out.append(">")
        else:
            for w in wrapped:
                out.append("> " + w)

    elif block_type == _FOOTNOTE:
        first = para[0]
        m = re.match(r"^(\[\^[^\]]+\]:\s*)(.*)", first)
        if m:
            fn_prefix = m.group(1)
            body_parts = [m.group(2)] + [ln.strip() for ln in para[1:]]
            content = " ".join(part for part in body_parts if part)
            if content:
                wrapped = textwrap.wrap(
                    content,
                    width=max(_MIN_WRAP_WIDTH, width),
                    initial_indent=fn_prefix,
                    subsequent_indent="    ",
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                out.extend(wrapped)
            else:
                out.append(fn_prefix.rstrip())
        else:
            out.extend(para)

    elif block_type == _LIST_ITEM:
        content = " ".join(ln.strip() for ln in para)
        sub_indent = " " * len(prefix)
        if len(sub_indent) > 8:
            sub_indent = "    "
        wrapped = textwrap.wrap(
            content,
            width=max(_MIN_WRAP_WIDTH, width),
            initial_indent="",
            subsequent_indent=sub_indent,
            break_long_words=False,
            break_on_hyphens=False,
        )
        out.extend(wrapped)

    elif block_type == _INDENTED:
        content = " ".join(ln.strip() for ln in para)
        wrapped = textwrap.wrap(
            content,
            width=max(_MIN_WRAP_WIDTH, width),
            initial_indent=indent,
            subsequent_indent=indent,
            break_long_words=False,
            break_on_hyphens=False,
        )
        out.extend(wrapped)

    elif block_type == _PROSE:
        content = " ".join(ln.strip() for ln in para)
        wrapped = textwrap.wrap(
            content,
            width=max(_MIN_WRAP_WIDTH, width),
            break_long_words=False,
            break_on_hyphens=False,
        )
        out.extend(wrapped)

    else:
        raise AssertionError(
            f"_flush_block: unhandled block_type {block_type!r}"
        )

    return out


# ── Line classifier ─────────────────────────────────────────────────────────

def _code_fence_backtick_count(stripped: str) -> int:
    """Return the backtick count (3 or 4) if the line is a code fence marker,
    else 0. Checks 4-backtick prefix first to avoid misidentifying ```` as ```.
    """
    for count in (4, 3):
        if stripped.startswith("`" * count):
            return count
    return 0


def _is_math_fence(stripped: str) -> bool:
    """Return True only for a standalone display-math fence toggle: '$$'."""
    return stripped == "$$"


def _is_single_line_display_math(stripped: str) -> bool:
    """Return True for a self-contained single-line display equation '$$...$$'."""
    return (
        stripped.startswith("$$")
        and stripped.endswith("$$")
        and len(stripped) > 4
    )


def _is_heading_or_break(stripped: str) -> bool:
    return stripped.startswith("#") or stripped in ("---", "***")


def _is_table_row(stripped: str) -> bool:
    return stripped.startswith("|")


def _is_footnote(line: str) -> bool:
    return bool(re.match(r"^\[\^[^\]]+\]:\s*", line))


def _is_blockquote(stripped: str) -> bool:
    return stripped.startswith(">")


def _detect_list_item(line: str) -> tuple[bool, str]:
    """Return (is_list, prefix) for the line."""
    if (
        re.match(r"^\s*[-*+]\s+", line)
        or re.match(r"^\s*\d+\.\s+", line)
        or re.match(r"^\s*\*\*[a-zA-Z0-9\.]+\*\*\s+", line)
    ):
        m_p = re.match(
            r"^(\s*(?:[-*+]\s+|\d+\.\s+)?(?:\*\*[a-zA-Z0-9\.]+\*\*\s+)?)",
            line,
        )
        prefix = m_p.group(1) if m_p else ""
        return True, prefix
    return False, ""


# ── Markdown wrapper ────────────────────────────────────────────────────────

def wrap_markdown(text: str, width: int = 80) -> str:
    lines = text.splitlines()
    out: list[str] = []

    in_code = False
    _open_fence_count = 0
    in_math = False

    current_para: list[str] = []
    current_type: str | None = None
    current_prefix = ""
    current_indent = ""

    def flush() -> None:
        nonlocal current_para, current_type, current_prefix, current_indent
        result = _flush_block(
            current_type, current_para, current_prefix, current_indent, width
        )
        out.extend(result)
        current_para = []
        current_type = None
        current_prefix = ""
        current_indent = ""

    for line in lines:
        stripped = line.strip()

        # 1. Code block fence — track opening backtick count so only a
        #    matching (same or greater) closing fence ends the block.
        fence_count = _code_fence_backtick_count(stripped)
        if fence_count:
            if not in_code:
                flush()
                in_code = True
                _open_fence_count = fence_count
                out.append(line)
                continue
            is_pure_fence = all(c == "`" for c in stripped)
            if is_pure_fence and fence_count >= _open_fence_count:
                in_code = False
                _open_fence_count = 0
                out.append(line)
                continue
        if in_code:
            out.append(line)
            continue

        # 2a. Single-line display equation: '$$...$$'
        if _is_single_line_display_math(stripped):
            flush()
            out.append(line)
            continue

        # 2b. Math display block fence (bare '$$')
        if _is_math_fence(stripped):
            flush()
            in_math = not in_math
            out.append(line)
            continue
        if in_math:
            out.append(line)
            continue

        # 3. Empty line
        if not stripped:
            flush()
            out.append("")
            continue

        # 4. Heading or thematic break
        if _is_heading_or_break(stripped):
            flush()
            out.append(line)
            continue

        # 5. Table row
        if _is_table_row(stripped):
            if current_type != _TABLE:
                flush()
            current_type = _TABLE
            current_para.append(line)
            continue

        # 6. Footnote definition
        if _is_footnote(line):
            flush()
            current_type = _FOOTNOTE
            current_para.append(line)
            continue

        # 7. Blockquote
        if _is_blockquote(stripped):
            if current_type != _QUOTE:
                flush()
            current_type = _QUOTE
            current_para.append(line)
            continue

        # 8. List item start
        is_list, prefix = _detect_list_item(line)
        if is_list and prefix.strip():
            flush()
            current_type = _LIST_ITEM
            current_prefix = prefix
            current_para.append(line)
            continue

        # 9. Indented continuation inside list
        if (line.startswith("    ") or line.startswith("  ")) and current_type in (
            _LIST_ITEM,
            _INDENTED,
        ):
            flush()
            indent_match = re.match(r"^(\s+)", line)
            current_indent = indent_match.group(1) if indent_match else "    "
            current_type = _INDENTED
            current_para.append(line)
            continue

        # 10. Continuation of current block
        if current_type is not None:
            current_para.append(line)
            continue

        # 11. Standard prose
        current_type = _PROSE
        current_para.append(line)

    flush()
    return "\n".join(out)


# ── Target collection ───────────────────────────────────────────────────────

def _collect_targets_from_dir(directory: str, extensions: tuple[str, ...]) -> list[str]:
    """Return sorted list of files in directory whose names end with any of extensions."""
    targets: list[str] = []
    if os.path.exists(directory):
        for f in sorted(os.listdir(directory)):
            if any(f.endswith(ext) for ext in extensions):
                targets.append(os.path.join(directory, f))
    return targets


def collect_targets(base_dir: str) -> list[str]:
    """Return an ordered list of files to format in base_dir.

    Scans ``src/``, ``specs/``, ``refinery/``, root ``.md`` files (excluding
    ``README.md``, ``AGENTS.md``, ``PEBBLE.md``, and ``GMRTI_<digits>.md``),
    and ``README.md`` last. Never scans ``math/`` (formatted by ``lake fmt``).
    """
    targets: list[str] = []

    targets.extend(_collect_targets_from_dir(os.path.join(base_dir, "src"), (".md",)))
    targets.extend(
        _collect_targets_from_dir(os.path.join(base_dir, "specs"), (".yaml", ".yml"))
    )
    targets.extend(
        _collect_targets_from_dir(os.path.join(base_dir, "refinery"), (".md",))
    )

    excluded_root_files = {"README.md", "AGENTS.md", "PEBBLE.md"}
    for f in sorted(os.listdir(base_dir)):
        if f.endswith(".md") and f not in excluded_root_files:
            if not MONOLITHIC_PATTERN.match(f):
                targets.append(os.path.join(base_dir, f))

    readme_path = os.path.join(base_dir, "README.md")
    if os.path.exists(readme_path):
        targets.append(readme_path)

    return targets


# ── File I/O ────────────────────────────────────────────────────────────────

def _read_and_dispatch(filepath: str, width: int) -> tuple[str, str]:
    """Read file and dispatch to the appropriate wrap function."""
    content = read_utf8(filepath)
    if filepath.endswith((".yaml", ".yml")):
        wrapped = wrap_yaml(content, width=width)
    else:
        wrapped = wrap_markdown(content, width=width)
    return content, wrapped


def process_file(
    filepath: str, width: int = 80, check_only: bool = False, dry_run: bool = False
) -> bool:
    content, wrapped = _read_and_dispatch(filepath, width)
    wrapped_output = wrapped if wrapped.endswith("\n") else wrapped + "\n"
    needs_change = content != wrapped_output

    if check_only:
        return needs_change

    if dry_run:
        if needs_change:
            print(f"[DRY RUN] Would reformat: {filepath}")
        return needs_change

    if needs_change:
        print(f"Formatted: {filepath}")
        write_utf8(filepath, wrapped_output)

    return needs_change


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wrap Markdown and YAML files to fixed width."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if files need wrapping without writing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show which files would be changed.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=80,
        help="Line width limit (default: 80).",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Target file or directory.",
    )

    args = parser.parse_args()
    base_dir = get_repo_root(__file__)

    if args.path:
        target_path = os.path.abspath(args.path)
        if os.path.isfile(target_path):
            targets = [target_path]
        elif os.path.isdir(target_path):
            targets = collect_targets(target_path)
        else:
            print(f"Error: path not found: {args.path}")
            sys.exit(1)
    else:
        targets = collect_targets(base_dir)

    changed_count = 0
    try:
        for filepath in targets:
            changed = process_file(
                filepath,
                width=args.width,
                check_only=args.check,
                dry_run=args.dry_run,
            )
            if changed:
                changed_count += 1
                if args.check:
                    print(f"Unformatted: {filepath}")
    except OSError as exc:
        print(f"Error processing file: {exc}")
        sys.exit(1)

    if args.check:
        if changed_count > 0:
            print(f"Total unformatted files: {changed_count}")
            sys.exit(1)
        print("All files are cleanly wrapped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
