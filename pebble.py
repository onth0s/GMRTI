"""pebble.py — Programmatic extraction and compilation engine for PEBBLE.md.

Extracts [PLAIN] high-school-accessible entry ramps and [ALLEGORY] worked
examples from the modular GMRTI treatise sources in ``src/``, appends the formal
``GLOSSARY.md`` and the final Coda, and compiles the unified plain-language
companion ``PEBBLE.md``.

Enforces subset parity between the full academic treatise and PEBBLE.md.
"""
import os
import re
import sys

from _gmrti_common import (
    ASSEMBLY_MANIFEST,
    CodeFenceTracker,
    SyncResult,
    build_base_parser,
    exit_for_check,
    extract_wikilinks,
    get_repo_root,
    read_utf8,
    write_utf8,
)

# Regex pattern to identify formal status and relational markers to strip
MARKER_STRIP_PATTERN = re.compile(
    r"\s*`?\[(STABLE|PROVISIONAL|OPEN|RECURSIVE|PLAIN|ALLEGORY(?::\s*[^\]]+)?)\]`?",
    re.DOTALL | re.IGNORECASE,
)
RELATIONAL_STRIP_PATTERN = re.compile(r"\s*\[->[a-zA-Z0-9_-]+\]")

# [PLAIN] block opener: starts the line (optionally after a bold clause heading),
# excluding bulleted status-marker definitions in §0.3.
_PLAIN_OPENER_RE = re.compile(
    r"^(?:\*\*[^*]+\*\*\s+)?`?\[PLAIN\]`?(?:\s|$)", re.IGNORECASE
)

# Section 0.0 ("Why This Exists") has a 3-paragraph plain preamble; all other
# sections have a single-paragraph [PLAIN] entry ramp.
_MULTI_PARA_PLAIN_PREFIXES = ("0.0 ",)
_MULTI_PARA_PLAIN_EXACT = ("0.0",)

# Clauses explicitly excluded from PEBBLE allegory extraction (guarded by test).
_EXCLUDED_ALLEGORY_PREFIXES = ("- **2f.3ii",)


def clean_plain_text(text: str) -> str:
    """Strip formal status markers and relational annotations from plain text.

    Preserves legitimate ``**bold**`` emphasis and `` `code` `` spans while
    removing empty marker remnants.
    """
    text = MARKER_STRIP_PATTERN.sub("", text)
    text = RELATIONAL_STRIP_PATTERN.sub("", text)
    text = re.sub(r"\*\*\s*\*\*", "", text)
    text = re.sub(r"(?<!`)``(?!`)", "", text)
    return text.strip()


def _is_next_section_or_clause(line: str) -> bool:
    """Return True if *line* begins a new heading or numbered treatise clause."""
    return bool(
        line.startswith(("## ", "### ", "```", "~~~"))
        or re.match(r"^\*\*\d+[a-z]?\.\d+", line)
        or re.match(r"^-\s+\*\*\d+[a-z]?\.\d+", line)
        or re.match(r"^\*\*\d+[a-z]?\s*—", line)
    )


def _is_allegory_opener(line: str) -> bool:
    """Return True if *line* starts an extractable allegory clause."""
    if not (line.startswith("- **") or line.startswith("**")):
        return False
    if line.strip().startswith(_EXCLUDED_ALLEGORY_PREFIXES):
        return False
    lower = line.lower()
    return (
        "allegory" in lower
        or "worked didactic instantiation" in lower
        or "[allegory" in lower
    )


def _clean_allegory_title(combined_header: str) -> str:
    """Extract and normalize the display title from an allegory header."""
    m_title = re.search(r"\*\*([^*]+)\*\*", combined_header)
    raw_title = m_title.group(1) if m_title else "Allegory"
    clean_title = re.sub(r"^[0-9a-z\.]+\s*—\s*", "", raw_title).strip()
    clean_title = re.sub(
        r"\s*Allegory\s*$", "", clean_title, flags=re.IGNORECASE
    ).strip()
    return clean_title or "Allegory"


def _collect_allegory_header(lines: list[str], start_idx: int) -> tuple[str, int]:
    """Combine multi-line allegory header starting at *start_idx*; return (header, next_idx)."""
    combined = lines[start_idx]
    i = start_idx
    while i + 1 < len(lines) and (
        "**" not in combined or "[" not in combined or "]" not in combined
    ):
        nxt = lines[i + 1]
        if nxt.strip() == "" or nxt.startswith("- **") or nxt.startswith("**"):
            break
        i += 1
        combined += " " + lines[i]
    return combined, i + 1


def _collect_allegory_body(lines: list[str], start_idx: int, remainder: str) -> tuple[str, int]:
    """Collect allegory body lines from *start_idx* until next clause/section."""
    body_lines = [remainder] if remainder else []
    i = start_idx
    while i < len(lines):
        next_line = lines[i]
        if _is_next_section_or_clause(next_line):
            break
        if (
            next_line.strip() == ""
            and i + 1 < len(lines)
            and _is_next_section_or_clause(lines[i + 1])
        ):
            break
        body_lines.append(next_line.strip())
        i += 1
    body = clean_plain_text(" ".join(ln for ln in body_lines if ln).strip())
    return body, i


def extract_allegories_from_raw_text(
    content: str, filename: str = ""
) -> list[tuple[str, str]]:
    """Extract full [ALLEGORY] blocks from markdown content."""
    if os.path.basename(filename) == "00_preamble.md":
        return []

    allegories: list[tuple[str, str]] = []
    lines = content.splitlines()
    fence_tracker = CodeFenceTracker()
    i = 0
    while i < len(lines):
        line = lines[i]
        is_fence_line, inside_fence = fence_tracker.step(line)
        if is_fence_line or inside_fence or not _is_allegory_opener(line):
            i += 1
            continue

        combined_header, next_i = _collect_allegory_header(lines, i)
        if "[ALLEGORY" not in combined_header.upper():
            i = next_i
            continue

        clean_title = _clean_allegory_title(combined_header)
        parts = re.split(
            r"`?\[ALLEGORY(?::\s*[^\]]+)?\]`?",
            combined_header,
            flags=re.DOTALL | re.IGNORECASE,
        )
        remainder = clean_plain_text(
            parts[-1].strip(" `*") if len(parts) > 1 else ""
        )
        body, i = _collect_allegory_body(lines, next_i, remainder)
        if body:
            allegories.append((clean_title, body))

    return allegories


def _find_preceding_heading(lines: list[str], idx: int) -> str:
    """Scan backward from *idx* for the nearest bold or ### section heading."""
    for j in range(idx - 1, max(idx - 6, -1), -1):
        stripped = lines[j].strip()
        if stripped == "" or clean_plain_text(stripped) == "":
            continue
        if stripped.startswith("### "):
            return clean_plain_text(stripped[4:].strip())
        if lines[j].startswith("**"):
            m_prev = re.search(r"\*\*([^*]+)\*\*", lines[j])
            if m_prev:
                return clean_plain_text(m_prev.group(1))
        break
    return ""


def _plain_para_limit(heading: str) -> int:
    """Return how many paragraphs a [PLAIN] block should consume."""
    if heading in _MULTI_PARA_PLAIN_EXACT or heading.startswith(
        _MULTI_PARA_PLAIN_PREFIXES
    ):
        return 3
    return 1


def _extract_plain_block(lines: list[str], start_idx: int) -> tuple[dict[str, str] | None, int]:
    """Consume one [PLAIN] block starting at *start_idx*; return (block_or_None, next_idx)."""
    line = lines[start_idx]
    m_h = re.search(r"\*\*([^*]+)\*\*", line)
    if m_h:
        heading = clean_plain_text(m_h.group(1))
        remainder = line.split("[PLAIN]", 1)[1].strip(" `*")
    else:
        heading = _find_preceding_heading(lines, start_idx)
        remainder = line.replace("`[PLAIN]`", "").replace("[PLAIN]", "").strip()

    target_paras = _plain_para_limit(heading)
    paras: list[str] = []
    cur_para = [remainder] if remainder else []
    i = start_idx + 1

    while i < len(lines):
        cur_line = lines[i]
        stripped = cur_line.strip()

        if cur_line.startswith(("## ", "### ", "**", "- **", "1. **", r"\[", "$$", "```", "~~~")):
            break

        if stripped == "":
            if cur_para:
                paras.append(" ".join(cur_para))
                cur_para = []
            if len(paras) >= target_paras:
                break
            i += 1
            continue

        cur_para.append(stripped)
        i += 1

    if cur_para:
        paras.append(" ".join(cur_para))

    full_text = clean_plain_text("\n\n".join(paras).strip())
    block = {"heading": heading, "text": full_text} if full_text else None
    return block, i


def parse_src_file(content: str, filename: str = "") -> dict:
    """Parse a src/ file into major heading and its [PLAIN] and [ALLEGORY] blocks."""
    lines = content.splitlines()
    major_heading = ""
    for ln in lines:
        if ln.startswith("## SECTION"):
            major_heading = ln.strip("# ").strip()
            break

    plain_blocks: list[dict[str, str]] = []
    fence_tracker = CodeFenceTracker()
    i = 0
    while i < len(lines):
        line = lines[i]
        is_fence_line, inside_fence = fence_tracker.step(line)
        if is_fence_line or inside_fence:
            i += 1
            continue
        if _PLAIN_OPENER_RE.match(line.strip()):
            block, i = _extract_plain_block(lines, i)
            if block is not None:
                plain_blocks.append(block)
            continue
        i += 1

    return {
        "major_heading": major_heading,
        "plain_blocks": plain_blocks,
        "allegories": extract_allegories_from_raw_text(content, filename),
    }


def _filter_glossary_for_pebble(glossary_content: str, body_text: str) -> str:
    """Keep only glossary entries referenced by [[wikilinks]] in PEBBLE (plus transitive deps)."""
    parts = re.split(r"(?=^#### \* )", glossary_content, flags=re.M)
    if len(parts) <= 1:
        return glossary_content

    header = parts[0].rstrip()
    entries: list[tuple[str, str]] = []
    entry_map: dict[str, str] = {}
    for block in parts[1:]:
        first_line = block.splitlines()[0]
        term = first_line[len("#### * "):].strip()
        entries.append((term, block.strip()))
        entry_map[term] = block.strip()

    needed = set(extract_wikilinks(body_text))
    needed.update({"GMRTI", "Metaagnosticism"})

    # Transitive closure over wikilinks inside selected glossary entries
    queue = [t for t in needed if t in entry_map]
    visited = set(queue)
    while queue:
        cur = queue.pop()
        for dep in extract_wikilinks(entry_map[cur]):
            if dep in entry_map and dep not in visited:
                visited.add(dep)
                queue.append(dep)

    kept = [block for term, block in entries if term in visited]
    if not kept:
        return glossary_content
    return header + "\n\n" + "\n\n".join(kept)


def _render_section_pebble(parsed: dict) -> str:
    """Render one parsed ``src/`` section into PEBBLE markdown."""
    file_parts: list[str] = []
    if parsed["major_heading"]:
        file_parts.append(f"## {parsed['major_heading']}")

    for block in parsed["plain_blocks"]:
        h = block["heading"]
        t = block["text"]
        if h and h != parsed["major_heading"]:
            file_parts.append(f"### {h}\n\n{t}")
        else:
            file_parts.append(t)

    for title, a_text in parsed["allegories"]:
        allegory_block = (
            f"> **Allegory: {title}**\n>\n"
            + "\n".join(f"> {ln}" for ln in a_text.splitlines() if ln.strip())
        )
        file_parts.append(allegory_block)

    return "\n\n".join(file_parts)


def _build_pebble_glossary(base_dir: str, body_text: str) -> str:
    """Load, demote, and filter ``GLOSSARY.md`` for PEBBLE."""
    glossary_path = os.path.join(base_dir, "GLOSSARY.md")
    if not os.path.exists(glossary_path):
        raise FileNotFoundError(f"Critical source file missing: {glossary_path}")
    glossary_content = read_utf8(glossary_path).strip()
    glossary_content = re.sub(
        r"^#\s+Glossary\b",
        "### Glossary",
        glossary_content,
        count=1,
        flags=re.MULTILINE,
    )
    glossary_content = _filter_glossary_for_pebble(glossary_content, body_text)
    return (
        "## The Formal Glossary (Minimum Sufficient Reference)\n\n"
        "*The following glossary contains the formal definitions from the full\n"
        "GMRTI treatise that are directly referenced in this guide.*\n\n"
        + glossary_content
    )


def assemble_pebble_document(base_dir: str | None = None) -> str:
    if base_dir is None:
        base_dir = get_repo_root(__file__)

    doc_parts: list[str] = [
        "# PEBBLE: The Plain-Language Alignment Guide\n\n"
        "> *A high-school-accessible, jargon-free transmission of the General Method\n"
        "> for Refinement and Transmission of Ideas (GMRTI).*"
    ]

    src_files = [
        entry.path
        for entry in ASSEMBLY_MANIFEST
        if entry.path.startswith("src/") and entry.path != "src/09_coda.md"
    ]

    for rel_path in src_files:
        fpath = os.path.join(base_dir, rel_path)
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"Critical source file missing: {fpath}")

        parsed = parse_src_file(read_utf8(fpath), filename=rel_path)
        if parsed["plain_blocks"] or parsed["allegories"]:
            doc_parts.append(_render_section_pebble(parsed))

    doc_parts.append(_build_pebble_glossary(base_dir, "\n\n".join(doc_parts)))

    coda_path = os.path.join(base_dir, "src", "09_coda.md")
    if not os.path.exists(coda_path):
        raise FileNotFoundError(f"Critical source file missing: {coda_path}")
    doc_parts.append(clean_plain_text(read_utf8(coda_path).strip()))

    return "\n\n---\n\n".join(doc_parts) + "\n"


def check_pebble_sync(base_dir: str | None = None) -> SyncResult:
    if base_dir is None:
        base_dir = get_repo_root(__file__)

    pebble_path = os.path.join(base_dir, "PEBBLE.md")
    if not os.path.exists(pebble_path):
        return {
            "in_sync": False,
            "error": "PEBBLE.md does not exist at workspace root.",
        }

    existing_content = read_utf8(pebble_path)
    assembled = assemble_pebble_document(base_dir)
    return {"in_sync": existing_content == assembled, "error": None}


def create_pebble_document(
    base_dir: str | None = None,
    output_path: str | None = None,
    dry_run: bool = False,
) -> str:
    if base_dir is None:
        base_dir = get_repo_root(__file__)

    assembled = assemble_pebble_document(base_dir)
    if output_path is None:
        output_path = os.path.join(base_dir, "PEBBLE.md")

    if dry_run:
        print(
            f"[DRY RUN] Would compile PEBBLE.md to: {output_path} ({len(assembled)} bytes)"
        )
        return output_path

    write_utf8(output_path, assembled)
    print(f"PEBBLE.md successfully compiled at: {output_path}")
    return output_path


def main() -> None:
    parser = build_base_parser(
        description="Compile modular GMRTI plain blocks into PEBBLE.md.",
        check_help="Check if root PEBBLE.md document is in sync.",
        dry_run_help="Simulate compilation without writing.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Custom output filepath.",
    )

    args = parser.parse_args()
    base_dir = get_repo_root(__file__)

    if args.check:
        try:
            result = check_pebble_sync(base_dir)
        except (FileNotFoundError, OSError, ValueError) as e:
            print(f"Error during check: {e}")
            sys.exit(1)
        if result["error"]:
            exit_for_check(False, "", result["error"])
        exit_for_check(
            result["in_sync"],
            "Root PEBBLE.md document is fully in sync.",
            "Root PEBBLE.md document is OUT OF SYNC with source files.",
        )

    try:
        create_pebble_document(
            base_dir=base_dir, output_path=args.output, dry_run=args.dry_run
        )
    except (FileNotFoundError, OSError, ValueError) as e:
        print(f"Error during compilation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
