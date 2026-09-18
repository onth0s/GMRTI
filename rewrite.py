import os
import re
import sys
import time
import shutil
import argparse

def assemble_monolithic_document(base_dir):
    readme_path = os.path.join(base_dir, "README.md")
    if not os.path.exists(readme_path):
        raise FileNotFoundError(f"Missing root readme: {readme_path}")

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Extract header (up to Table of Contents)
    header_match = re.search(r"^(.*?)(?=\n## Table of Contents)", readme_content, re.DOTALL)
    header = header_match.group(1).strip() if header_match else ""

    files_to_include = [
        "src/00_preamble.md",
        "GLOSSARY.md",
        "ARCHITECTURE.md",
        "METHODOLOGY.md",
        "REFINEMENT.md",
        "src/01_problem.md",
        "src/02_architecture.md",
        "src/03_algorithm.md",
        "src/04_temporal_anchoring.md",
        "src/05_metalanguage.md",
        "src/06_refinement_vectors.md",
        "src/07_downstream.md",
    ]

    body_parts = []

    for rel_path in files_to_include:
        filepath = os.path.join(base_dir, rel_path)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Critical source file missing: {filepath}")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Structural alignment for GLOSSARY.md
        if rel_path == "GLOSSARY.md":
            content = re.sub(r"^#\s+Glossary\b", "**0.4 Vocabulary**", content, flags=re.MULTILINE)
            # Append directly to preamble without '---' separator
            if body_parts:
                body_parts[-1] += "\n\n" + content
            else:
                body_parts.append(content)
        else:
            body_parts.append(content)

    body_text = "\n\n---\n\n".join(body_parts)
    final_document = header + "\n\n" + body_text + "\n"
    return final_document

def archive_prior_monolithic_files(base_dir, current_output_path=None):
    """
    Enforces AGENTS.md rule: Only keep the latest compiled monolithic revision
    in root. Move all prior monolithic revisions to archive/.
    """
    archive_dir = os.path.join(base_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    archived_files = []
    for f in os.listdir(base_dir):
        if re.match(r"^GMRTI_\d+\.md$", f):
            full_path = os.path.join(base_dir, f)
            if current_output_path and os.path.abspath(full_path) == os.path.abspath(current_output_path):
                continue
            dest_path = os.path.join(archive_dir, f)
            shutil.move(full_path, dest_path)
            archived_files.append(f)
            print(f"Archived prior monolithic revision: {f} -> archive/{f}")

    return archived_files

def check_monolithic_sync(base_dir):
    """Checks if the existing root monolithic document matches the current sources."""
    mono_files = [f for f in os.listdir(base_dir) if re.match(r"^GMRTI_\d+\.md$", f)]
    if not mono_files:
        print("No monolithic revision found in root.")
        return False

    if len(mono_files) > 1:
        print(f"Rule violation: multiple monolithic files in root: {mono_files}")
        return False

    latest_mono_path = os.path.join(base_dir, mono_files[0])
    with open(latest_mono_path, "r", encoding="utf-8") as f:
        existing_content = f.read()

    assembled = assemble_monolithic_document(base_dir)
    if existing_content == assembled:
        print(f"Root monolithic document {mono_files[0]} is fully in sync.")
        return True
    else:
        print(f"Root monolithic document {mono_files[0]} is OUT OF SYNC with source files.")
        return False

def create_monolithic_document(base_dir=None, output_path=None, dry_run=False):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    assembled = assemble_monolithic_document(base_dir)

    epoch_time = int(time.time())
    if output_path is None:
        output_path = os.path.join(base_dir, f"GMRTI_{epoch_time}.md")

    if dry_run:
        print(f"[DRY RUN] Would compile monolithic document to: {output_path} ({len(assembled)} bytes)")
        prior = [f for f in os.listdir(base_dir) if re.match(r"^GMRTI_\d+\.md$", f)]
        if prior:
            print(f"[DRY RUN] Would archive prior revisions: {prior}")
        return output_path

    # First, archive prior monolithic files before writing the new one
    archive_prior_monolithic_files(base_dir, current_output_path=output_path)

    # Write new monolithic document
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(assembled)

    print(f"Monolithic document created at: {output_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Compile modular GMRTI treatise into monolithic document.")
    parser.add_argument("--check", action="store_true", help="Check if root monolithic document is in sync.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate compilation and archival without writing.")
    parser.add_argument("--output", type=str, default=None, help="Custom output filepath.")

    args = parser.parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if args.check:
        in_sync = check_monolithic_sync(base_dir)
        sys.exit(0 if in_sync else 1)

    try:
        create_monolithic_document(base_dir=base_dir, output_path=args.output, dry_run=args.dry_run)
    except Exception as e:
        print(f"Error during compilation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
