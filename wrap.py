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
import os
import re
import sys
import textwrap

import yaml

from _gmrti_common import (
    MONOLITHIC_PATTERN,
    CodeFenceTracker,
    build_base_parser,
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


def _wrap_yaml_line(line: str, width: int) -> list[str]:
    """Wrap a single YAML line that exceeds *width*."""
    # 1. Key-value string with quotes: key: "value..."
    key_match = re.match(r'^(\s*)([\w-]+):\s*"((?:[^"\\]|\\.)*)"$', line)
    if key_match:
        indent, key, raw_val = key_match.groups()
        val = raw_val.replace('\\"', '"')
        wrapped = _wrap_yaml_scalar(val, width - len(indent) - 2)
        return [f"{indent}{key}: >-"] + [f"{indent}  {wl}" for wl in wrapped]

    # 2. Key-value unquoted long string (excluding flow collections and inline comments)
    key_unquoted = re.match(r'^(\s*)([\w-]+):\s+([^\">|#{\[\s].*)$', line)
    if key_unquoted and not line.strip().startswith("-") and " #" not in key_unquoted.group(3):
        indent, key, val = key_unquoted.groups()
        wrapped = _wrap_yaml_scalar(val, width - len(indent) - 2)
        return [f"{indent}{key}: >-"] + [f"{indent}  {wl}" for wl in wrapped]

    # 3. List item string with quotes: - "value..."
    list_match = re.match(r'^(\s*)-\s*"((?:[^"\\]|\\.)*)"$', line)
    if list_match:
        indent, raw_val = list_match.groups()
        val = raw_val.replace('\\"', '"')
        wrapped = _wrap_yaml_scalar(val, width - len(indent) - 4)
        return [f"{indent}- >-"] + [f"{indent}    {wl}" for wl in wrapped]

    # 4a. List item mapping: - key: value...
    list_mapping = re.match(r'^(\s*-\s+)([\w-]+):\s+([^\">|#{\[\s].*)$', line)
    if list_mapping and " #" not in list_mapping.group(3):
        list_prefix, key, val = list_mapping.groups()
        sub_indent = " " * len(list_prefix) + "  "
        wrapped = _wrap_yaml_scalar(val, width - len(sub_indent))
        return [f"{list_prefix}{key}: >-"] + [f"{sub_indent}{wl}" for wl in wrapped]

    # 4b. List item unquoted long string (excluding flow collections, mappings, comments)
    list_unquoted = re.match(r'^(\s*)-\s+([^\">|#{\[\s].*)$', line)
    if (
        list_unquoted
        and not re.match(r"^[\w-]+:(?:\s|$)", list_unquoted.group(2))
        and " #" not in list_unquoted.group(2)
    ):
        indent, val = list_unquoted.groups()
        wrapped = _wrap_yaml_scalar(val, width - len(indent) - 4)
        return [f"{indent}- >-"] + [f"{indent}    {wl}" for wl in wrapped]

    # 5. Comment line
    comment_match = re.match(r"^(\s*)#\s*(.*)$", line)
    if comment_match:
        indent, val = comment_match.groups()
        wrapped = _wrap_yaml_scalar(val, width - len(indent) - 2)
        return [f"{indent}# {wl}" for wl in wrapped]

    # 6. Fallback preserving existing indentation (crucial for block scalars)
    indent_len = len(line) - len(line.lstrip())
    indent = line[:indent_len]
    return [f"{indent}{wl}" for wl in _wrap_yaml_scalar(line.strip(), width - indent_len)]


def _validate_yaml_wrap(original: str, wrapped: str) -> str:
    """Return *wrapped* if it preserves parsed YAML semantics, else *original*."""
    if wrapped == original:
        return wrapped
    try:
        orig_data = yaml.safe_load(original)
        new_data = yaml.safe_load(wrapped)
        if orig_data != new_data:
            print(
                "Warning: wrap_yaml detected semantic drift; keeping original YAML.",
                file=sys.stderr,
            )
            return original
    except Exception as exc:
        try:
            yaml.safe_load(original)
        except Exception:
            return wrapped
        print(
            f"Warning: wrap_yaml produced invalid YAML ({exc}); keeping original.",
            file=sys.stderr,
        )
        return original
    return wrapped


def wrap_yaml(text: str, width: int = 80) -> str:
    """Wrap YAML lines exceeding *width* while preserving parsed semantics."""
    lines: list[str] = []
    for line in text.splitlines():
        if len(line) <= width:
            lines.append(line)
        else:
            lines.extend(_wrap_yaml_line(line, width))
    return _validate_yaml_wrap(text, "\n".join(lines))


# ── Markdown block flusher ──────────────────────────────────────────────────

_WIKILINK_SPAN_RE = re.compile(r"\[\[[^\]]+\]\]")
_WIKILINK_SPACE_SENTINEL = "\x00"


def _wrap_prose(
    content: str,
    width: int,
    initial_indent: str = "",
    subsequent_indent: str = "",
) -> list[str]:
    """Wrap *content* to *width* without splitting ``[[wikilinks]]`` across lines."""
    protected = _WIKILINK_SPAN_RE.sub(
        lambda m: m.group(0).replace(" ", _WIKILINK_SPACE_SENTINEL),
        content,
    )
    wrapped = textwrap.wrap(
        protected,
        width=max(_MIN_WRAP_WIDTH, width),
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        break_long_words=False,
        break_on_hyphens=False,
    )
    return [ln.replace(_WIKILINK_SPACE_SENTINEL, " ") for ln in wrapped]


def _flush_quote(para: list[str], prefix: str, width: int) -> list[str]:
    quote_prefix = prefix or "> "
    stripped = [re.sub(r"^(?:>\s*)+", "", ln) for ln in para]
    wrapped = _wrap_prose(" ".join(stripped), width - len(quote_prefix))
    if not wrapped:
        return [quote_prefix.rstrip()]
    return [quote_prefix + w for w in wrapped]


def _flush_footnote(para: list[str], width: int) -> list[str]:
    m = re.match(r"^(\[\^[^\]]+\]:\s*)(.*)", para[0])
    if not m:
        return list(para)
    fn_prefix = m.group(1)
    body_parts = [m.group(2)] + [ln.strip() for ln in para[1:]]
    content = " ".join(part for part in body_parts if part)
    if not content:
        return [fn_prefix.rstrip()]
    return _wrap_prose(content, width, initial_indent=fn_prefix, subsequent_indent="    ")


def _flush_block(
    block_type: str | None,
    para: list[str],
    prefix: str,
    indent: str,
    width: int,
) -> list[str]:
    """Return a list of output lines for one accumulated markdown block."""
    if not para:
        return []
    if block_type == _TABLE:
        return list(para)
    if block_type == _QUOTE:
        return _flush_quote(para, prefix, width)
    if block_type == _FOOTNOTE:
        return _flush_footnote(para, width)
    if block_type == _LIST_ITEM:
        sub_indent = " " * len(prefix)
        if len(sub_indent) > 8:
            sub_indent = "    "
        return _wrap_prose(" ".join(ln.strip() for ln in para), width, subsequent_indent=sub_indent)
    if block_type == _INDENTED:
        return _wrap_prose(
            " ".join(ln.strip() for ln in para), width, initial_indent=indent, subsequent_indent=indent
        )
    if block_type == _PROSE:
        return _wrap_prose(" ".join(ln.strip() for ln in para), width)
    raise AssertionError(f"_flush_block: unhandled block_type {block_type!r}")


# ── Line classifier ─────────────────────────────────────────────────────────


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


def _is_setext_underline(stripped: str) -> bool:
    return bool(re.match(r"^(?:=+|-+)$", stripped))


def _is_html_block_line(stripped: str) -> bool:
    return bool(re.match(r"^<[a-zA-Z/!]", stripped))


def _is_table_row(stripped: str) -> bool:
    return stripped.startswith("|")


def _is_footnote(line: str) -> bool:
    return bool(re.match(r"^\[\^[^\]]+\]:\s*", line))


def _quote_prefix_and_body(stripped: str) -> tuple[str, str] | None:
    """If *stripped* is a blockquote line, return (normalized_prefix, body)."""
    m = re.match(r"^((?:>\s*)+)(.*)$", stripped)
    if not m:
        return None
    depth = m.group(1).count(">")
    return (">" * depth) + " ", m.group(2)


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

def _consume_frontmatter(lines: list[str], out: list[str]) -> int:
    """Emit leading YAML frontmatter verbatim and return the starting body index."""
    if lines and lines[0].strip() == "---":
        for fm_end in range(1, len(lines)):
            if lines[fm_end].strip() == "---":
                out.extend(lines[: fm_end + 1])
                return fm_end + 1
    return 0


def wrap_markdown(text: str, width: int = 80) -> str:
    """Reflow Markdown prose, quotes, footnotes, and lists to *width*."""
    lines = text.splitlines()
    out: list[str] = []
    idx = _consume_frontmatter(lines, out)

    fence_tracker = CodeFenceTracker()
    in_math = False
    current_para: list[str] = []
    current_type: str | None = None
    current_prefix = ""
    current_indent = ""

    def flush() -> None:
        nonlocal current_para, current_type, current_prefix, current_indent
        out.extend(
            _flush_block(current_type, current_para, current_prefix, current_indent, width)
        )
        current_para = []
        current_type = None
        current_prefix = ""
        current_indent = ""

    for line in lines[idx:]:
        stripped = line.strip()

        # 1. Code block fence
        is_fence_line, inside_fence = fence_tracker.step(line)
        if is_fence_line:
            if fence_tracker.in_fence:
                flush()
            out.append(line)
            continue
        if inside_fence:
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

        # 4. Setext heading underline (must precede thematic break check for '---')
        if current_type == _PROSE and current_para and _is_setext_underline(stripped):
            out.extend(current_para)
            current_para = []
            current_type = None
            out.append(line)
            continue

        # 5. Heading, thematic break, or HTML block line
        if _is_heading_or_break(stripped) or _is_html_block_line(stripped):
            flush()
            out.append(line)
            continue

        # 6. Table row
        if _is_table_row(stripped):
            if current_type != _TABLE:
                flush()
            current_type = _TABLE
            current_para.append(line)
            continue

        # 7. Footnote definition
        if _is_footnote(line):
            flush()
            current_type = _FOOTNOTE
            current_para.append(line)
            continue

        # 8. Blockquote (callout headers pass through verbatim; grouped by depth)
        quote_info = _quote_prefix_and_body(stripped)
        if quote_info is not None:
            q_prefix, q_body = quote_info
            if re.match(r"^\[!(?:[^\]]*)\]\s*$", q_body):
                flush()
                out.append(line)
                continue
            if re.match(r"^\s*(?:[-*+]\s+|\d+\.\s+)", q_body):
                flush()
                out.append(line)
                continue
            if current_type != _QUOTE or current_prefix != q_prefix:
                flush()
            current_type = _QUOTE
            current_prefix = q_prefix
            current_para.append(line)
            continue

        # 9. List item start
        is_list, prefix = _detect_list_item(line)
        if is_list and prefix.strip():
            flush()
            current_type = _LIST_ITEM
            current_prefix = prefix
            current_para.append(line)
            continue

        # 10. Indented continuation inside list
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

        # 11. Hard line break (two trailing spaces or trailing backslash)
        hard_break = ""
        if line.endswith("  "):
            hard_break = "  "
            line_for_para = line.rstrip(" ")
        elif line.endswith("\\"):
            hard_break = "\\"
            line_for_para = line[:-1]
        else:
            line_for_para = line

        # 12. Continuation of current block or standard prose
        if current_type is None:
            current_type = _PROSE
        current_para.append(line_for_para)

        if hard_break:
            flush()
            if out:
                out[-1] = out[-1] + hard_break

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

def _collect_targets_in_dir(directory: str) -> list[str]:
    """Collect wrappable ``.md`` and ``.yaml``/``.yml`` files directly inside *directory*."""
    excluded = {"AGENTS.md", "PEBBLE.md"}
    targets: list[str] = []
    for f in sorted(os.listdir(directory)):
        full = os.path.join(directory, f)
        if not os.path.isfile(full):
            continue
        if f.endswith((".yaml", ".yml")):
            targets.append(full)
        elif f.endswith(".md") and f not in excluded and not MONOLITHIC_PATTERN.match(f):
            targets.append(full)
    return targets


def _resolve_targets(base_dir: str, path_arg: str | None) -> list[str]:
    """Resolve CLI ``--path`` argument or default repository targets."""
    if not path_arg:
        return collect_targets(base_dir)
    target_path = os.path.abspath(path_arg)
    if os.path.isfile(target_path):
        return [target_path]
    if os.path.isdir(target_path):
        if os.path.abspath(base_dir) == target_path:
            return collect_targets(target_path)
        return _collect_targets_in_dir(target_path)
    print(f"Error: path not found: {path_arg}")
    sys.exit(1)


def main() -> None:
    parser = build_base_parser(
        description="Wrap Markdown and YAML files to fixed width.",
        check_help="Check if files need wrapping without writing.",
        dry_run_help="Show which files would be changed.",
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
    targets = _resolve_targets(base_dir, args.path)

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
