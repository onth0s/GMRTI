"""pebble.py — Programmatic extraction and compilation engine for PEBBLE.md.

Extracts [PLAIN] high-school-accessible entry ramps and [ALLEGORY] worked
examples from the modular GMRTI treatise sources in ``src/``, appends the formal
``GLOSSARY.md`` and the final Coda, and compiles the unified plain-language
companion ``PEBBLE.md``.

Enforces subset parity between the full academic treatise and PEBBLE.md.
"""
import argparse
import os
import re
import sys

from _gmrti_common import get_repo_root, read_utf8, write_utf8
from rewrite import ASSEMBLY_MANIFEST

# Regex pattern to identify formal status and relational markers to strip
MARKER_STRIP_PATTERN = re.compile(
    r"\s*`?\[(STABLE|PROVISIONAL|OPEN|RECURSIVE|RESTORED|EXCISED|PLAIN|ALLEGORY(?::\s*[^\]]+)?)\]`?",
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
_MULTI_PARA_PLAIN_HEADINGS = ("0.0",)


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
        line.startswith("## ")
        or re.match(r"^\*\*\d+[a-z]?\.\d+", line)
        or re.match(r"^-\s+\*\*\d+[a-z]?\.\d+", line)
        or re.match(r"^\*\*\d+[a-z]?\s*—", line)
    )


def extract_allegories_from_raw_text(
    content: str, filename: str = ""
) -> list[tuple[str, str]]:
    """Extract full [ALLEGORY] blocks from markdown content."""
    if os.path.basename(filename) == "00_preamble.md":
        return []

    allegories: list[tuple[str, str]] = []
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # An allegory bullet or heading starts with (- )?**...
        if (
            (line.startswith("- **") or line.startswith("**"))
            and (
                "allegory" in line.lower()
                or "worked didactic instantiation" in line.lower()
                or "[allegory" in line.lower()
            )
            and not line.strip().startswith("- **2f.3ii")
        ):
            combined_header = line
            while i + 1 < len(lines) and (
                "**" not in combined_header
                or "[" not in combined_header
                or "]" not in combined_header
            ):
                nxt = lines[i + 1]
                if nxt.strip() == "" or nxt.startswith("- **") or nxt.startswith("**"):
                    break
                i += 1
                combined_header += " " + lines[i]

            if "[ALLEGORY" in combined_header.upper():
                m_title = re.search(r"\*\*([^*]+)\*\*", combined_header)
                raw_title = m_title.group(1) if m_title else "Allegory"
                clean_title = re.sub(r"^[0-9a-z\.]+\s*—\s*", "", raw_title).strip()
                clean_title = re.sub(
                    r"\s*Allegory\s*$", "", clean_title, flags=re.IGNORECASE
                ).strip()
                if not clean_title:
                    clean_title = "Allegory"

                parts = re.split(
                    r"`?\[ALLEGORY(?::\s*[^\]]+)?\]`?",
                    combined_header,
                    flags=re.DOTALL | re.IGNORECASE,
                )
                remainder = parts[-1].strip(" `*") if len(parts) > 1 else ""
                remainder = clean_plain_text(remainder)
                body_lines = [remainder] if remainder else []
                i += 1

                while i < len(lines):
                    next_line = lines[i]
                    if _is_next_section_or_clause(next_line):
                        break
                    if next_line.strip() == "":
                        if i + 1 < len(lines) and _is_next_section_or_clause(lines[i + 1]):
                            break
                    body_lines.append(next_line.strip())
                    i += 1

                body = clean_plain_text(" ".join(ln for ln in body_lines if ln).strip())
                if body:
                    allegories.append((clean_title, body))
                continue
        i += 1

    return allegories


def _find_preceding_heading(lines: list[str], idx: int) -> str:
    """Scan backward from *idx* for the nearest bold section heading."""
    for j in range(idx - 1, max(idx - 6, -1), -1):
        if lines[j].strip() == "":
            continue
        if lines[j].startswith("**"):
            m_prev = re.search(r"\*\*([^*]+)\*\*", lines[j])
            if m_prev:
                return clean_plain_text(m_prev.group(1))
        break
    return ""


def parse_src_file(content: str, filename: str = "") -> dict:
    """Parse a src/ file into major heading and its [PLAIN] and [ALLEGORY] blocks."""
    lines = content.splitlines()
    major_heading = ""
    for ln in lines:
        if ln.startswith("## SECTION"):
            major_heading = ln.strip("# ").strip()
            break

    plain_blocks: list[dict[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if _PLAIN_OPENER_RE.match(line.strip()):
            heading = ""
            m_h = re.search(r"\*\*([^*]+)\*\*", line)
            if m_h:
                heading = clean_plain_text(m_h.group(1))
                remainder = line.split("[PLAIN]", 1)[1].strip(" `*")
            else:
                heading = _find_preceding_heading(lines, i)
                remainder = (
                    line.replace("`[PLAIN]`", "").replace("[PLAIN]", "").strip()
                )

            target_paras = (
                3
                if any(tag in heading for tag in _MULTI_PARA_PLAIN_HEADINGS)
                else 1
            )
            paras: list[str] = []
            cur_para = [remainder] if remainder else []
            i += 1

            while i < len(lines):
                cur_line = lines[i]
                stripped = cur_line.strip()

                if cur_line.startswith(
                    ("## ", "**", "- **", "1. **", r"\[", "$$")
                ):
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
            if full_text:
                plain_blocks.append({"heading": heading, "text": full_text})
            continue
        i += 1

    allegories = extract_allegories_from_raw_text(content, filename)

    return {
        "major_heading": major_heading,
        "plain_blocks": plain_blocks,
        "allegories": allegories,
    }


def assemble_pebble_document(base_dir: str | None = None) -> str:
    if base_dir is None:
        base_dir = get_repo_root(__file__)

    doc_parts: list[str] = [
        "# PEBBLE: The Plain-Language Alignment Guide\n\n"
        "> *A high-school-accessible, jargon-free transmission of the General Method\n"
        "> for Refinement and Transmission of Ideas (GMRTI).*"
    ]

    src_files = [
        entry["path"]
        for entry in ASSEMBLY_MANIFEST
        if entry["path"].startswith("src/") and entry["path"] != "src/09_coda.md"
    ]

    for rel_path in src_files:
        fpath = os.path.join(base_dir, rel_path)
        if not os.path.exists(fpath):
            continue

        parsed = parse_src_file(read_utf8(fpath), filename=rel_path)
        if not parsed["plain_blocks"] and not parsed["allegories"]:
            continue

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
                + "\n".join(
                    f"> {ln}" for ln in a_text.splitlines() if ln.strip()
                )
            )
            file_parts.append(allegory_block)

        doc_parts.append("\n\n".join(file_parts))

    # Append GLOSSARY.md with heading demoted from H1 to H3 under H2 wrapper
    glossary_path = os.path.join(base_dir, "GLOSSARY.md")
    if os.path.exists(glossary_path):
        glossary_content = read_utf8(glossary_path).strip()
        glossary_content = re.sub(
            r"^#\s+Glossary\b",
            "### Glossary",
            glossary_content,
            count=1,
            flags=re.MULTILINE,
        )
        glossary_wrapper = (
            "## The Formal Glossary (Academic Reference)\n\n"
            "*The following glossary contains the verbatim formal definitions from\n"
            "the full GMRTI treatise. It is included here for readers who wish to\n"
            "explore the precise academic and mathematical definitions of the framework.*\n\n"
            + glossary_content
        )
        doc_parts.append(glossary_wrapper)

    # Append Coda (src/09_coda.md)
    coda_path = os.path.join(base_dir, "src", "09_coda.md")
    if os.path.exists(coda_path):
        coda_content = clean_plain_text(read_utf8(coda_path).strip())
        doc_parts.append(coda_content)

    return "\n\n---\n\n".join(doc_parts) + "\n"


def check_pebble_sync(base_dir: str | None = None) -> dict:
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
    parser = argparse.ArgumentParser(
        description="Compile modular GMRTI plain blocks into PEBBLE.md."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if root PEBBLE.md document is in sync.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate compilation without writing.",
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
        result = check_pebble_sync(base_dir)
        if result["error"]:
            print(result["error"])
            sys.exit(1)
        elif result["in_sync"]:
            print("Root PEBBLE.md document is fully in sync.")
            sys.exit(0)
        else:
            print("Root PEBBLE.md document is OUT OF SYNC with source files.")
            sys.exit(1)

    try:
        create_pebble_document(
            base_dir=base_dir, output_path=args.output, dry_run=args.dry_run
        )
    except (FileNotFoundError, OSError, ValueError) as e:
        print(f"Error during compilation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
