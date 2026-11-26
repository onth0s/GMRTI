import glob
import os
import re
from _gmrti_common import MONOLITHIC_PATTERN, CodeFenceTracker, extract_wikilinks


def _strip_fenced_code(content: str) -> str:
    """Return *content* with fenced code blocks removed."""
    tracker = CodeFenceTracker()
    kept: list[str] = []
    for line in content.splitlines():
        is_fence_line, inside_fence = tracker.step(line)
        if not is_fence_line and not inside_fence:
            kept.append(line)
    return "\n".join(kept)


def find_markdown_links(content):
    """Extract [text](target) markdown links outside fenced code blocks."""
    stripped = _strip_fenced_code(content)
    return re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", stripped)


def test_markdown_links(base_dir):
    md_files = []
    for f in os.listdir(base_dir):
        if f.endswith(".md") and not MONOLITHIC_PATTERN.match(f):
            md_files.append(os.path.join(base_dir, f))

    for subdir in ["src", "refinery"]:
        sub_path = os.path.join(base_dir, subdir)
        if os.path.exists(sub_path):
            for f in os.listdir(sub_path):
                if f.endswith(".md"):
                    md_files.append(os.path.join(sub_path, f))

    math_readme = os.path.join(base_dir, "math", "README.md")
    if os.path.exists(math_readme):
        md_files.append(math_readme)

    broken_links = []

    for filepath in md_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        links = find_markdown_links(content)
        file_dir = os.path.dirname(filepath)

        for text, target in links:
            target = target.strip()
            if re.match(r"^[a-zA-Z]+://", target) or target.startswith("mailto:"):
                continue

            target_path = target.split("#")[0]
            if not target_path:
                continue

            target_path = target_path.split("?")[0]
            resolved_path = os.path.normpath(os.path.join(file_dir, target_path))
            if not os.path.exists(resolved_path):
                broken_links.append((
                    os.path.relpath(filepath, base_dir),
                    text,
                    target,
                    os.path.relpath(resolved_path, base_dir),
                ))

    assert not broken_links, f"Broken markdown links detected: {broken_links}"


def test_wikilinks_resolve(base_dir):
    """Every [[wikilink]] in src/ and GLOSSARY.md resolves to a glossary term or heading."""
    glossary_path = os.path.join(base_dir, "GLOSSARY.md")
    with open(glossary_path, "r", encoding="utf-8") as f:
        glossary_text = f.read()

    known_targets = set(re.findall(r"^#### \* (.+)$", glossary_text, flags=re.M))
    src_files = sorted(glob.glob(os.path.join(base_dir, "src", "*.md")))
    for path in src_files:
        with open(path, "r", encoding="utf-8") as f:
            txt = _strip_fenced_code(f.read())
        for heading in re.findall(r"^#{2,3}\s+(.+)$", txt, flags=re.M):
            known_targets.add(heading.strip())

    unresolved = []
    for path in src_files + [glossary_path]:
        with open(path, "r", encoding="utf-8") as f:
            txt = _strip_fenced_code(f.read())
        for target in extract_wikilinks(txt):
            if target not in known_targets:
                unresolved.append((os.path.relpath(path, base_dir), target))

    assert not unresolved, f"Unresolved wikilinks detected: {unresolved}"
