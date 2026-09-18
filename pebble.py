"""pebble.py — Programmatic extraction and compilation engine for PEBBLE.md.

Extracts [PLAIN] high-school-accessible entry ramps and [ALLEGORY] worked
examples from the modular GMRTI treatise sources in `src/`, appends the formal
`GLOSSARY.md` and the final Coda, and compiles the unified plain-language
companion `PEBBLE.md`.

Enforces subset parity between the full academic treatise and PEBBLE.md.
"""
import os
import re
import sys
import argparse

# Import canonical manifest from rewrite.py to maintain single source of truth
from rewrite import ASSEMBLY_MANIFEST

# Regex pattern to identify formal status and relational markers to strip
MARKER_STRIP_PATTERN = re.compile(
    r"\s*`?\[(STABLE|PROVISIONAL|OPEN|RECURSIVE|RESTORED|EXCISED|PLAIN|ALLEGORY(?::\s*[^\]]+)?)\]`?",
    re.DOTALL | re.IGNORECASE,
)
RELATIONAL_STRIP_PATTERN = re.compile(r"\s*\[->[a-zA-Z0-9_-]+\]")


def clean_plain_text(text: str) -> str:
    """Strip formal status markers and relational annotations from plain text."""
    text = MARKER_STRIP_PATTERN.sub("", text)
    text = RELATIONAL_STRIP_PATTERN.sub("", text)
    # Clean up empty markdown bold tags or empty backticks
    text = re.sub(r"\*{2,}", "", text)
    text = re.sub(r"`{2,}", "", text)
    return text.strip()


def extract_allegories_from_raw_text(content: str, filename: str = "") -> list[tuple[str, str]]:
    """Extract full [ALLEGORY] blocks from markdown content."""
    if "00_preamble" in filename:
        return []

    allegories = []
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # An allegory bullet or heading starts with (- )?**...
        if (
            (line.startswith("- **") or line.startswith("**"))
            and ("allegory" in line.lower() or "worked didactic instantiation" in line.lower() or "[allegory" in line.lower())
            and not line.strip().startswith("- **2f.3ii")  # exclude inline mention
        ):
            combined_header = line
            # Consume continuation lines of header until closing ** or [tag]
            while i + 1 < len(lines) and ("**" not in combined_header or "[" not in combined_header or "]" not in combined_header):
                if lines[i + 1].strip() == "" or lines[i + 1].startswith("- **") or lines[i + 1].startswith("**"):
                    break
                i += 1
                combined_header += " " + lines[i]

            if "[ALLEGORY" in combined_header.upper():
                m_title = re.search(r"\*\*([^*]+)\*\*", combined_header)
                raw_title = m_title.group(1) if m_title else "Allegory"
                # Strip clause numbers like 1a.5i — or 2a.4iv —
                clean_title = re.sub(r"^[0-9a-z\.]+\s*—\s*", "", raw_title).strip()
                clean_title = re.sub(r"\s*Allegory\s*$", "", clean_title, flags=re.IGNORECASE).strip()
                if not clean_title:
                    clean_title = "Allegory"

                # Extract text after [ALLEGORY...]
                parts = re.split(r"`?\[ALLEGORY(?::\s*[^\]]+)?\]`?", combined_header, flags=re.DOTALL | re.IGNORECASE)
                remainder = parts[-1].strip(" `*") if len(parts) > 1 else ""
                # Strip any trailing status markers like [PROVISIONAL] from remainder
                remainder = clean_plain_text(remainder)
                body_lines = [remainder] if remainder else []
                i += 1

                while i < len(lines):
                    next_line = lines[i]
                    # Stop on next major section or next numbered paragraph/allegory heading
                    if (
                        next_line.startswith("## ")
                        or re.match(r"^\*\*\d+[a-z]?\.\d+", next_line)
                        or re.match(r"^-\s+\*\*\d+[a-z]?\.\d+", next_line)
                        or re.match(r"^\*\*\d+[a-z]?\s*—", next_line)
                    ):
                        break
                    if next_line.strip() == "":
                        if i + 1 < len(lines):
                            peek = lines[i + 1]
                            if (
                                peek.startswith("## ")
                                or re.match(r"^\*\*\d+[a-z]?\.\d+", peek)
                                or re.match(r"^-\s+\*\*\d+[a-z]?\.\d+", peek)
                                or re.match(r"^\*\*\d+[a-z]?\s*—", peek)
                            ):
                                break
                    body_lines.append(next_line.strip())
                    i += 1

                body = " ".join([l for l in body_lines if l]).strip()
                body = clean_plain_text(body)
                if body:
                    allegories.append((clean_title, body))
                continue
        i += 1

    return allegories


def parse_src_file(content: str, filename: str = "") -> dict:
    """Parse a src/ file into major heading and its [PLAIN] and [ALLEGORY] blocks."""
    lines = content.splitlines()
    major_heading = ""
    for l in lines:
        if l.startswith("## SECTION"):
            major_heading = l.strip("# ").strip()
            break

    # 1. Extract plain blocks
    plain_blocks = []
    # Match [PLAIN] followed by paragraph(s)
    # A plain block is tagged with `[PLAIN]` or [PLAIN]
    i = 0
    while i < len(lines):
        line = lines[i]
        if "[PLAIN]" in line and "status markers" not in line.lower() and "entry ramp" not in line.lower():
            # Extract heading if present
            heading = ""
            m_h = re.search(r"\*\*([^*]+)\*\*", line)
            if m_h:
                heading = clean_plain_text(m_h.group(1))
                remainder = line.split("[PLAIN]", 1)[1].strip(" `*")
            else:
                if i > 0 and lines[i - 1].startswith("**"):
                    m_prev = re.search(r"\*\*([^*]+)\*\*", lines[i - 1])
                    if m_prev:
                        heading = clean_plain_text(m_prev.group(1))
                remainder = line.replace("`[PLAIN]`", "").replace("[PLAIN]", "").strip()

            paras = []
            cur_para = [remainder] if remainder else []
            i += 1

            while i < len(lines):
                cur_line = lines[i]
                stripped = cur_line.strip()

                if cur_line.startswith("## ") or cur_line.startswith("**") or cur_line.startswith("- **") or cur_line.startswith("1. **") or cur_line.startswith(r"\[") or cur_line.startswith("$$"):
                    break

                if stripped == "":
                    if cur_para:
                        paras.append(" ".join(cur_para))
                        cur_para = []
                    # Section 0.0 (Why This Exists) has 3 paragraphs; all others have 1 paragraph
                    if "0.0" in heading:
                        if len(paras) >= 3:
                            break
                    else:
                        if len(paras) >= 1:
                            break
                    i += 1
                    continue

                cur_para.append(stripped)
                i += 1

            if cur_para:
                paras.append(" ".join(cur_para))

            full_text = "\n\n".join(paras).strip()
            full_text = clean_plain_text(full_text)
            if full_text:
                plain_blocks.append({"heading": heading, "text": full_text})
            continue
        i += 1

    # 2. Extract allegories
    allegories = extract_allegories_from_raw_text(content, filename)

    return {
        "major_heading": major_heading,
        "plain_blocks": plain_blocks,
        "allegories": allegories,
    }


def assemble_pebble_document(base_dir: str = None) -> str:
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    doc_parts = []

    # Title & Subtitle
    doc_parts.append(
        "# PEBBLE: The Plain-Language Alignment Guide\n\n"
        "> *A high-school-accessible, jargon-free transmission of the General Method\n"
        "> for Refinement and Transmission of Ideas (GMRTI).*"
    )

    src_files = [
        entry["path"]
        for entry in ASSEMBLY_MANIFEST
        if entry["path"].startswith("src/") and entry["path"] != "src/09_coda.md"
    ]

    for rel_path in src_files:
        fpath = os.path.join(base_dir, rel_path)
        if not os.path.exists(fpath):
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        parsed = parse_src_file(content, filename=rel_path)
        if not parsed["plain_blocks"] and not parsed["allegories"]:
            continue

        file_parts = []
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
                + "\n".join([f"> {line}" for line in a_text.splitlines() if line.strip()])
            )
            file_parts.append(allegory_block)

        doc_parts.append("\n\n".join(file_parts))

    # Append GLOSSARY.md verbatim
    glossary_path = os.path.join(base_dir, "GLOSSARY.md")
    if os.path.exists(glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            glossary_content = f.read().strip()

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
        with open(coda_path, "r", encoding="utf-8") as f:
            coda_content = f.read().strip()
        coda_content = clean_plain_text(coda_content)
        doc_parts.append(coda_content)

    final_pebble = "\n\n---\n\n".join(doc_parts) + "\n"
    return final_pebble


def check_pebble_sync(base_dir: str = None) -> dict:
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    pebble_path = os.path.join(base_dir, "PEBBLE.md")
    if not os.path.exists(pebble_path):
        return {
            "in_sync": False,
            "error": "PEBBLE.md does not exist at workspace root.",
        }

    with open(pebble_path, "r", encoding="utf-8") as f:
        existing_content = f.read()

    assembled = assemble_pebble_document(base_dir)
    in_sync = existing_content == assembled
    return {"in_sync": in_sync, "error": None}


def create_pebble_document(
    base_dir: str = None, output_path: str = None, dry_run: bool = False
) -> str:
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    assembled = assemble_pebble_document(base_dir)
    if output_path is None:
        output_path = os.path.join(base_dir, "PEBBLE.md")

    if dry_run:
        print(
            f"[DRY RUN] Would compile PEBBLE.md to: {output_path} ({len(assembled)} bytes)"
        )
        return output_path

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(assembled)

    print(f"PEBBLE.md successfully compiled at: {output_path}")
    return output_path


def main():
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
    base_dir = os.path.dirname(os.path.abspath(__file__))

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
