import os
import re
import time

def create_monolithic_document():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    readme_path = os.path.join(base_dir, "README.md")
    
    epoch_time = int(time.time())
    output_path = os.path.join(base_dir, f"GMRTI_{epoch_time}.md")

    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Extract header (up to Table of Contents)
    header_match = re.search(r"^(.*?)(?=\n## Table of Contents)", readme_content, re.DOTALL)
    header = header_match.group(1).strip() if header_match else ""

    files_to_include = [
        "src/00_preamble.md",
        "glossary.md",
        "src/01_problem.md",
        "src/02_architecture.md",
        "src/03_algorithm.md",
        "src/04_temporal_anchoring.md",
        "src/05_metalanguage.md",
        "src/06_refinement_vectors.md",
        "src/07_downstream.md",
        "src/08_open_challenges.md",
        "refinery/README.md",
    ]
    
    # Dynamically find refinery R*.md files and sort them
    refinery_dir = os.path.join(base_dir, "refinery")
    if os.path.exists(refinery_dir):
        r_files = [f for f in os.listdir(refinery_dir) if re.match(r"^R\d+\.md$", f)]
        r_files.sort()
        for rf in r_files:
            files_to_include.append(f"refinery/{rf}")

    body_parts = []

    for rel_path in files_to_include:
        filepath = os.path.join(base_dir, rel_path)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                
                # Apply fixes for structural alignment
                if rel_path == "glossary.md":
                    content = content.replace("# Glossary", "**0.4 Vocabulary**")
                    # Append directly to preamble without '---' separator
                    if body_parts:
                        body_parts[-1] += "\n\n" + content
                    else:
                        body_parts.append(content)
                else:
                    if rel_path == "refinery/README.md":
                        content = content.replace("# The Refinery", "## SECTION 10 — Refinery")
                        content = content.replace("unjustified compression is a confirmed failure mode.*", "unjustified compression is a confirmed failure mode (see 6b.4).*")

                    body_parts.append(content)
        else:
            print(f"Warning: {filepath} not found, skipping.")



    # Join the body parts with horizontal rules
    body_text = "\n\n---\n\n".join(body_parts)
    
    # Final assembly (header already ends with a '---', so we don't insert another one here)
    final_document = header + "\n\n" + body_text + "\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_document)

    print(f"Monolithic document created at: {output_path}")

if __name__ == "__main__":
    create_monolithic_document()
