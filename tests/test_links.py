import os
import re
from tests.conftest import MONOLITHIC_PATTERN

def find_markdown_links(content):
    # Regex to match markdown links: [text](target)
    # Ignore images ![alt](target) if desired, but local images should also resolve
    matches = re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", content)
    return matches

def test_markdown_links(base_dir):
    md_files = []
    # Root markdown files
    for f in os.listdir(base_dir):
        if f.endswith(".md") and not MONOLITHIC_PATTERN.match(f):
            md_files.append(os.path.join(base_dir, f))

    # Subdirectories to scan for markdown links.
    # Excluded directories:
    #   - specs/: Contains machine-readable YAML concept specifications, which are
    #     validated for structural integrity and cross-references by test_specs.py.
    #   - archive/: Contains frozen historical monolithic snapshots that are preserved
    #     as immutable audit artifacts and deliberately not updated.
    for subdir in ["src", "refinery"]:
        sub_path = os.path.join(base_dir, subdir)
        if os.path.exists(sub_path):
            for f in os.listdir(sub_path):
                if f.endswith(".md"):
                    md_files.append(os.path.join(sub_path, f))

    broken_links = []

    for filepath in md_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        links = find_markdown_links(content)
        file_dir = os.path.dirname(filepath)

        for text, target in links:
            target = target.strip()
            # Ignore external links, mailto, scheme links
            if re.match(r"^[a-zA-Z]+://", target) or target.startswith("mailto:"):
                continue

            # Handle anchor links
            target_path = target.split("#")[0]
            if not target_path:
                # Same file anchor
                continue

            # Strip query params if any
            target_path = target_path.split("?")[0]

            resolved_path = os.path.normpath(os.path.join(file_dir, target_path))
            if not os.path.exists(resolved_path):
                broken_links.append((
                    os.path.relpath(filepath, base_dir),
                    text,
                    target,
                    os.path.relpath(resolved_path, base_dir)
                ))

    assert not broken_links, f"Broken markdown links detected: {broken_links}"
