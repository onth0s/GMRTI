"""wrap.py — Markdown and YAML line-width formatter for GMRTI.

Reformats source files in ``src/``, ``specs/``, and ``refinery/`` (plus root
markdown files) to a canonical line width (default 80 characters).

Block-type taxonomy handled by the Markdown wrapper
----------------------------------------------------
- ``table``       — pipe-delimited table rows; passed through verbatim.
- ``quote``       — blockquote paragraphs (``> …``); joined and reflowed.
- ``footnote``    — footnote definitions (``[^n]: …``); reflowed with hanging
                    indent.
- ``list_item``   — ordered/unordered list items; reflowed with continuation
                    indent matching the list marker width.
- ``indented_line`` — indented continuation lines; reflowed preserving indent.
- ``prose``       — plain paragraph text; reflowed freely.

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
import os
import sys
import re
import argparse
import textwrap

# ── Pattern constants ───────────────────────────────────────────────────────
MONOLITHIC_PATTERN = re.compile(r"^GMRTI_\d+\.md$")

# ── Block-type constants ────────────────────────────────────────────────────

_TABLE        = "table"
_QUOTE        = "quote"
_FOOTNOTE     = "footnote"
_LIST_ITEM    = "list_item"
_INDENTED     = "indented_line"
_PROSE        = "prose"


# ── YAML wrapper ────────────────────────────────────────────────────────────

def wrap_yaml(text, width=80):
    lines = []
    for line in text.splitlines():
        if len(line) <= width:
            lines.append(line)
            continue

        # 1. Key-value string replacement with quotes: key: "value..."
        key_match = re.match(r"^(\s*)([\w-]+):\s*\"([^\"]+)\"$", line)
        if key_match:
            indent = key_match.group(1)
            key = key_match.group(2)
            val = key_match.group(3)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 2)
            lines.append(f"{indent}{key}: >-")
            for wl in wrapped_val:
                lines.append(f"{indent}  {wl}")
            continue

        # 2. Key-value unquoted long string: key: value...
        # Exclude flow mappings/sequences ({...}, [...]) from being converted to block scalars
        key_unquoted = re.match(r"^(\s*)([\w-]+):\s+([^\">|#{\[\s].*)$", line)
        if key_unquoted and not line.strip().startswith("-"):
            indent = key_unquoted.group(1)
            key = key_unquoted.group(2)
            val = key_unquoted.group(3)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 2)
            lines.append(f"{indent}{key}: >-")
            for wl in wrapped_val:
                lines.append(f"{indent}  {wl}")
            continue

        # 3. List item string replacement with quotes: - "value..."
        list_match = re.match(r"^(\s*)-\s*\"([^\"]+)\"$", line)
        if list_match:
            indent = list_match.group(1)
            val = list_match.group(2)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 4)
            lines.append(f"{indent}- >-")
            for wl in wrapped_val:
                lines.append(f"{indent}    {wl}")
            continue

        # 4. List item unquoted long string: - value...
        list_unquoted = re.match(r"^(\s*)-\s+([^\">|#\s].*)$", line)
        if list_unquoted:
            indent = list_unquoted.group(1)
            val = list_unquoted.group(2)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 4)
            lines.append(f"{indent}- >-")
            for wl in wrapped_val:
                lines.append(f"{indent}    {wl}")
            continue

        # 5. Comment replacement
        comment_match = re.match(r"^(\s*)#\s*(.*)$", line)
        if comment_match:
            indent = comment_match.group(1)
            val = comment_match.group(2)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 2)
            for wl in wrapped_val:
                lines.append(f"{indent}# {wl}")
            continue

        # 6. Fallback preserving existing indentation (crucial for block scalars)
        indent_len = len(line) - len(line.lstrip())
        indent = line[:indent_len]
        stripped = line.strip()
        wrapped_sub = textwrap.wrap(
            stripped,
            width=width - indent_len,
            break_long_words=False,
            break_on_hyphens=False,
        )
        for wl in wrapped_sub:
            lines.append(f"{indent}{wl}")

    return "\n".join(lines)


# ── Markdown block flusher ──────────────────────────────────────────────────

def _flush_block(block_type, para, prefix, indent, width):
    """Return a list of output lines for one accumulated markdown block."""
    out = []
    if not para:
        return out

    if block_type == _TABLE:
        out.extend(para)

    elif block_type == _QUOTE:
        stripped = [re.sub(r"^>\s*", "", l) for l in para]
        content = " ".join(stripped)
        wrapped = textwrap.wrap(
            content,
            width=width - 2,
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
            body_parts = [m.group(2)] + [l.strip() for l in para[1:]]
            content = " ".join(body_parts)
            wrapped = textwrap.wrap(
                content,
                width=width - len(fn_prefix),
                break_long_words=False,
                break_on_hyphens=False,
            )
            if wrapped:
                out.append(fn_prefix + wrapped[0])
                sub_indent = "    "
                for w in wrapped[1:]:
                    sub_wrapped = textwrap.wrap(
                        w,
                        width=width - len(sub_indent),
                        break_long_words=False,
                        break_on_hyphens=False,
                    )
                    for sw in sub_wrapped:
                        out.append(sub_indent + sw)
            else:
                out.append(fn_prefix.rstrip())
        else:
            out.extend(para)

    elif block_type == _LIST_ITEM:
        content = " ".join([l.strip() for l in para])
        sub_indent = " " * len(prefix)
        if len(sub_indent) > 8:
            sub_indent = "    "
        wrapped = textwrap.wrap(
            content,
            width=width,
            initial_indent="",
            subsequent_indent=sub_indent,
            break_long_words=False,
            break_on_hyphens=False,
        )
        out.extend(wrapped)

    elif block_type == _INDENTED:
        content = " ".join([l.strip() for l in para])
        wrapped = textwrap.wrap(
            content,
            width=width,
            initial_indent=indent,
            subsequent_indent=indent,
            break_long_words=False,
            break_on_hyphens=False,
        )
        out.extend(wrapped)

    elif block_type == _PROSE:
        content = " ".join([l.strip() for l in para])
        wrapped = textwrap.wrap(
            content,
            width=width,
            break_long_words=False,
            break_on_hyphens=False,
        )
        out.extend(wrapped)

    else:
        # This branch is unreachable given the known block-type constants.
        # If a new block_type is added without a handler, fail immediately.
        raise AssertionError(
            f"_flush_block: unhandled block_type {block_type!r}"
        )

    return out


# ── Line classifier ─────────────────────────────────────────────────────────

def _code_fence_backtick_count(stripped):
    """Return the backtick count (3 or 4) if the line is a code fence marker,
    else 0.  Checks 4-backtick prefix first to avoid misidentifying ```` as ```.
    """
    for count in (4, 3):
        prefix = "`" * count
        if stripped.startswith(prefix):
            return count
    return 0


def _is_math_fence(stripped):
    """Return True only for a *standalone* display-math fence toggle: exactly '$$'.

    A line like '$$x = 1$$' is a single-line display equation and must NOT
    toggle the in_math state machine — use _is_single_line_display_math for
    those.
    """
    return stripped == "$$"


def _is_single_line_display_math(stripped):
    """Return True for a self-contained single-line display equation: '$$...$$'
    where content exists between the opening and closing markers.
    """
    return (
        stripped.startswith("$$")
        and stripped.endswith("$$")
        and len(stripped) > 4
    )


def _is_heading_or_break(stripped):
    return stripped.startswith("#") or stripped in ("---", "***")


def _is_table_row(stripped):
    return stripped.startswith("|")


def _is_footnote(line):
    return bool(re.match(r"^\[\^[^\]]+\]:\s*", line))


def _is_blockquote(stripped):
    return stripped.startswith(">")


def _detect_list_item(line):
    """Return (is_list, prefix) for the line."""
    if (
        re.match(r"^\s*[-*+]\s+", line)
        or re.match(r"^\s*\d+\.\s+", line)
        or re.match(r"^\s*-\s+\*\*", line)
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

def wrap_markdown(text, width=80):
    lines = text.splitlines()
    out = []

    in_code = False
    _open_fence_count = 0   # backtick count of the fence that opened in_code
    in_math = False

    current_para   = []
    current_type   = None
    current_prefix = ""
    current_indent = ""

    def flush():
        nonlocal current_para, current_type, current_prefix, current_indent
        result = _flush_block(current_type, current_para, current_prefix, current_indent, width)
        out.extend(result)
        current_para   = []
        current_type   = None
        current_prefix = ""
        current_indent = ""

    for line in lines:
        stripped = line.strip()

        # 1. Code block fence — track opening backtick count (W-08) so only a
        #    matching (same or greater) closing fence ends the block.
        fence_count = _code_fence_backtick_count(stripped)
        if fence_count:
            if not in_code:
                flush()
                in_code = True
                _open_fence_count = fence_count
                out.append(line)
                continue
            # inside a code block: only close on a *pure* fence line (no
            # info-string) whose backtick count >= the opening count.
            is_pure_fence = all(c == "`" for c in stripped)
            if is_pure_fence and fence_count >= _open_fence_count:
                in_code = False
                _open_fence_count = 0
                out.append(line)
                continue
        if in_code:
            out.append(line)
            continue

        # 2a. Single-line display equation: '$$...$$' on one line — flush and
        #     pass through verbatim; does NOT toggle in_math state.
        if _is_single_line_display_math(stripped):
            flush()
            out.append(line)
            continue

        # 2b. Math display block fence (bare '$$') — toggles in_math state.
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
            current_type   = _LIST_ITEM
            current_prefix = prefix
            current_para.append(line)
            continue

        # 9. Indented continuation inside list
        if (line.startswith("    ") or line.startswith("  ")) and current_type in (
            _LIST_ITEM,
            _INDENTED,
        ):
            flush()
            indent_match   = re.match(r"^(\s+)", line)
            current_indent = indent_match.group(1) if indent_match else "    "
            current_type   = _INDENTED
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

def _collect_targets_from_dir(directory, extensions):
    """Return sorted list of files in directory whose names end with any of extensions."""
    targets = []
    if os.path.exists(directory):
        for f in sorted(os.listdir(directory)):
            if any(f.endswith(ext) for ext in extensions):
                targets.append(os.path.join(directory, f))
    return targets


def collect_targets(base_dir):
    """Return an ordered list of files to format in base_dir.

    Scans the following locations with a **shallow** (non-recursive) listing:

    - ``src/``      — ``.md`` files only
    - ``specs/``    — ``.yaml`` / ``.yml`` files only
    - ``refinery/`` — ``.md`` files only
    - Root of base_dir — all ``.md`` files except ``README.md`` and files
      matching the monolithic-archive pattern ``GMRTI_<digits>.md``
    - ``README.md`` (always last)

    .. important::
        This function does **not** recurse into subdirectories.  If a nested
        subdirectory is added inside ``src/``, ``specs/``, or ``refinery/``,
        its files will be silently skipped.  Update ``_collect_targets_from_dir``
        calls here when the directory structure changes.
    """
    targets = []

    # 1. Walk src/  — markdown only
    targets.extend(_collect_targets_from_dir(
        os.path.join(base_dir, "src"), (".md",)
    ))

    # 2. Walk specs/  — YAML only
    targets.extend(_collect_targets_from_dir(
        os.path.join(base_dir, "specs"), (".yaml", ".yml")
    ))

    # 3. Walk refinery/  — markdown only
    targets.extend(_collect_targets_from_dir(
        os.path.join(base_dir, "refinery"), (".md",)
    ))

    # 4. Root markdown files (except monolithic archives/outputs and governance files)
    # AGENTS.md is a strict behavioral constraints file; exclude to prevent prose reflow.
    # PEBBLE.md is a compiled artifact; exclude to prevent prose reflow.
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

def _read_and_dispatch(filepath, width):
    """Read file and dispatch to the appropriate wrap function.

    Returns (original_content, wrapped_content).
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if filepath.endswith((".yaml", ".yml")):
        wrapped = wrap_yaml(content, width=width)
    else:
        wrapped = wrap_markdown(content, width=width)

    return content, wrapped


def process_file(filepath, width=80, check_only=False, dry_run=False):
    content, wrapped = _read_and_dispatch(filepath, width)

    # Ensure single trailing newline
    if not wrapped.endswith("\n"):
        wrapped_output = wrapped + "\n"
    else:
        wrapped_output = wrapped

    needs_change = content != wrapped_output

    if check_only:
        return needs_change

    if dry_run:
        if needs_change:
            print(f"[DRY RUN] Would reformat: {filepath}")
        return needs_change

    if needs_change:
        print(f"Formatted: {filepath}")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(wrapped_output)

    return needs_change


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Wrap Markdown and YAML files to fixed width.")
    parser.add_argument("--check",   action="store_true", help="Check if files need wrapping without writing.")
    parser.add_argument("--dry-run", action="store_true", help="Show which files would be changed.")
    parser.add_argument("--width",   type=int, default=80, help="Line width limit (default: 80).")
    parser.add_argument("--path",    type=str, default=None, help="Target file or directory.")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))

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

    if args.check:
        if changed_count > 0:
            print(f"Total unformatted files: {changed_count}")
            sys.exit(1)
        else:
            print("All files are cleanly wrapped.")
            sys.exit(0)


if __name__ == "__main__":
    main()
