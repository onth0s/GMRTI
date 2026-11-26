import os
import re
from tests.conftest import MONOLITHIC_PATTERN

_FENCED_CODE_RE = re.compile(r"```.*?```|````.*?````", re.S)


def find_markdown_links(content):
    """Extract [text](target) markdown links outside fenced code blocks."""
    stripped = _FENCED_CODE_RE.sub("", content)
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
