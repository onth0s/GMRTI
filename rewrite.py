import os
import re
import sys
import time
import shutil
import argparse

# -- Assembly manifest
# Each entry: {path, merge_mode}
# merge_mode 'separator': join body parts with '\n\n---\n\n'
# merge_mode 'append': stitch onto previous part without separator

ASSEMBLY_MANIFEST = [
    {"path": "src/00_preamble.md",           "merge_mode": "separator"},
    {"path": "GLOSSARY.md",                  "merge_mode": "append"},
    {"path": "src/01_problem.md",            "merge_mode": "separator"},
    {"path": "src/02_architecture.md",       "merge_mode": "separator"},
    {"path": "src/03_algorithm.md",          "merge_mode": "separator"},
    {"path": "src/04_temporal_anchoring.md", "merge_mode": "separator"},
    {"path": "src/05_metalanguage.md",       "merge_mode": "separator"},
    {"path": "src/06_refinement_vectors.md", "merge_mode": "separator"},
    {"path": "src/07_downstream.md",         "merge_mode": "separator"},
    {"path": "src/08_gaps.md",               "merge_mode": "separator"},
    {"path": "ARCHITECTURE.md",              "merge_mode": "separator"},
    {"path": "METHODOLOGY.md",               "merge_mode": "separator"},
    {"path": "REFINEMENT.md",                "merge_mode": "separator"},
]



def assemble_monolithic_document(base_dir):
    readme_path = os.path.join(base_dir, 'README.md')
    if not os.path.exists(readme_path):
        raise FileNotFoundError(f'Missing root readme: {readme_path}')

    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    header_match = re.search(
        r'^(.*?)(?=\n## Table of Contents)', readme_content, re.DOTALL
    )
    header = header_match.group(1).strip() if header_match else ''

    body_parts = []

    for entry in ASSEMBLY_MANIFEST:
        rel_path = entry['path']
        mode     = entry.get('merge_mode', 'separator')
        filepath = os.path.join(base_dir, rel_path)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f'Critical source file missing: {filepath}')

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if rel_path == 'GLOSSARY.md':
            content = re.sub(
                r'^#\s+Glossary\b', '**0.4 Vocabulary**',
                content, flags=re.MULTILINE
            )
        elif rel_path == 'ARCHITECTURE.md':
            content = re.sub(
                r'^#\s+GMRTI Architectural Model\b',
                '## APPENDIX A — Architectural Model',
                content, flags=re.MULTILINE
            )
        elif rel_path == 'METHODOLOGY.md':
            content = re.sub(
                r'^#\s+GMRTI Methodology & Status Markers\b',
                '## APPENDIX M — Methodology & Status Markers',
                content, flags=re.MULTILINE
            )
        elif rel_path == 'REFINEMENT.md':
            content = re.sub(
                r'^#\s+The Refinement Cycle\b',
                '## APPENDIX R — The Refinement Cycle',
                content, flags=re.MULTILINE
            )

        if mode == 'append':
            if body_parts:
                body_parts[-1] += '\n\n' + content
            else:
                body_parts.append(content)
        else:
            body_parts.append(content)

    body_text      = '\n\n---\n\n'.join(body_parts)
    final_document = header + '\n\n' + body_text + '\n'
    return final_document


def archive_prior_monolithic_files(base_dir, current_output_path=None):
    """
    Enforces AGENTS.md rule: only keep the latest compiled monolithic
    revision in root. Move all prior revisions to archive/.
    """
    archive_dir = os.path.join(base_dir, 'archive')
    os.makedirs(archive_dir, exist_ok=True)

    archived_files = []
    for f in os.listdir(base_dir):
        if re.match(r'^GMRTI_\d+\.md$', f):
            full_path = os.path.join(base_dir, f)
            if (current_output_path
                    and os.path.abspath(full_path)
                    == os.path.abspath(current_output_path)):
                continue
            dest_path = os.path.join(archive_dir, f)
            shutil.move(full_path, dest_path)
            archived_files.append(f)
            print(f'Archived prior monolithic revision: {f} -> archive/{f}')

    return archived_files


def check_monolithic_sync(base_dir):
    """Check whether the root monolithic document matches the current sources.

    Returns a dict with keys: in_sync (bool), mono_file (str|None),
    error (str|None).
    """
    mono_files = [
        f for f in os.listdir(base_dir)
        if re.match(r'^GMRTI_\d+\.md$', f)
    ]

    if not mono_files:
        return {
            'in_sync': False, 'mono_file': None,
            'error': 'No monolithic revision found in root.',
        }

    if len(mono_files) > 1:
        return {
            'in_sync': False, 'mono_file': None,
            'error': f'Rule violation: multiple monolithic files in root: {mono_files}',
        }

    latest      = mono_files[0]
    latest_path = os.path.join(base_dir, latest)
    with open(latest_path, 'r', encoding='utf-8') as f:
        existing_content = f.read()

    assembled = assemble_monolithic_document(base_dir)
    in_sync   = existing_content == assembled
    return {'in_sync': in_sync, 'mono_file': latest, 'error': None}


def create_monolithic_document(
        base_dir=None, output_path=None, dry_run=False, archive=True):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    assembled  = assemble_monolithic_document(base_dir)
    epoch_time = int(time.time())
    if output_path is None:
        output_path = os.path.join(base_dir, f'GMRTI_{epoch_time}.md')

    if dry_run:
        print(
            f'[DRY RUN] Would compile monolithic document to: '
            f'{output_path} ({len(assembled)} bytes)'
        )
        prior = [
            f for f in os.listdir(base_dir)
            if re.match(r'^GMRTI_\d+\.md$', f)
        ]
        if prior:
            print(f'[DRY RUN] Would archive prior revisions: {prior}')
        return output_path

    if archive:
        archive_prior_monolithic_files(
            base_dir, current_output_path=output_path
        )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(assembled)

    print(f'Monolithic document created at: {output_path}')
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Compile modular GMRTI treatise into monolithic document.'
    )
    parser.add_argument(
        '--check', action='store_true',
        help='Check if root monolithic document is in sync.'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Simulate compilation and archival without writing.'
    )
    parser.add_argument(
        '--output', type=str, default=None,
        help='Custom output filepath.'
    )

    args     = parser.parse_args()
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if args.check:
        result = check_monolithic_sync(base_dir)
        if result['error']:
            print(result['error'])
        elif result['in_sync']:
            print(
                f"Root monolithic document {result['mono_file']}"
                f' is fully in sync.'
            )
        else:
            print(
                f"Root monolithic document {result['mono_file']}"
                f' is OUT OF SYNC with source files.'
            )
        sys.exit(0 if result['in_sync'] else 1)

    try:
        create_monolithic_document(
            base_dir=base_dir, output_path=args.output,
            dry_run=args.dry_run
        )
    except Exception as e:
        print(f'Error during compilation: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
