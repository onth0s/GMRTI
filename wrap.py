import os
import sys
import re
import argparse
import textwrap

def wrap_yaml(text, width=80):
    lines = []
    for line in text.splitlines():
        if len(line) <= width:
            lines.append(line)
            continue

        # 1. Key-value string replacement with quotes: key: "value..."
        key_match = re.match(r"^(\s*)([\w-]+):\s*\"([^\"]+)\"$", line)
        if key_match:
            indent = key_match.group(1)
            key = key_match.group(2)
            val = key_match.group(3)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 2)
            lines.append(f"{indent}{key}: >-")
            for wl in wrapped_val:
                lines.append(f"{indent}  {wl}")
            continue

        # 2. Key-value unquoted long string: key: value...
        key_unquoted = re.match(r"^(\s*)([\w-]+):\s+([^\">|#\s].*)$", line)
        if key_unquoted and not line.strip().startswith("-"):
            indent = key_unquoted.group(1)
            key = key_unquoted.group(2)
            val = key_unquoted.group(3)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 2)
            lines.append(f"{indent}{key}: >-")
            for wl in wrapped_val:
                lines.append(f"{indent}  {wl}")
            continue

        # 3. List item string replacement with quotes: - "value..."
        list_match = re.match(r"^(\s*)-\s*\"([^\"]+)\"$", line)
        if list_match:
            indent = list_match.group(1)
            val = list_match.group(2)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 4)
            lines.append(f"{indent}- >-")
            for wl in wrapped_val:
                lines.append(f"{indent}    {wl}")
            continue

        # 4. List item unquoted long string: - value...
        list_unquoted = re.match(r"^(\s*)-\s+([^\">|#\s].*)$", line)
        if list_unquoted:
            indent = list_unquoted.group(1)
            val = list_unquoted.group(2)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 4)
            lines.append(f"{indent}- >-")
            for wl in wrapped_val:
                lines.append(f"{indent}    {wl}")
            continue

        # 5. Comment replacement
        comment_match = re.match(r"^(\s*)#\s*(.*)$", line)
        if comment_match:
            indent = comment_match.group(1)
            val = comment_match.group(2)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 2)
            for wl in wrapped_val:
                lines.append(f"{indent}# {wl}")
            continue

        # 6. Fallback preserving existing indentation (crucial for block scalars)
        indent_len = len(line) - len(line.lstrip())
        indent = line[:indent_len]
        stripped = line.strip()
        wrapped_sub = textwrap.wrap(
            stripped,
            width=width - indent_len,
            break_long_words=False,
            break_on_hyphens=False
        )
        for wl in wrapped_sub:
            lines.append(f"{indent}{wl}")

    return "\n".join(lines)

def wrap_markdown(text, width=80):
    lines = text.splitlines()
    out = []

    in_code = False
    in_math = False

    current_para = []
    current_type = None  # 'prose', 'list_item', 'indented_line', 'quote', 'table', 'footnote'
    current_prefix = ""
    current_indent = ""

    def flush():
        nonlocal current_para, current_type, current_prefix, current_indent
        if not current_para:
            return

        if current_type == "table":
            out.extend(current_para)
        elif current_type == "quote":
            stripped = [re.sub(r"^>\s*", "", l) for l in current_para]
            content = " ".join(stripped)
            wrapped = textwrap.wrap(
                content,
                width=width - 2,
                break_long_words=False,
                break_on_hyphens=False
            )
            if not wrapped:
                out.append(">")
            else:
                for w in wrapped:
                    out.append("> " + w)
        elif current_type == "footnote":
            first = current_para[0]
            m = re.match(r"^(\[\^[^\]]+\]:\s*)(.*)", first)
            if m:
                fn_prefix = m.group(1)
                body_parts = [m.group(2)] + [l.strip() for l in current_para[1:]]
                content = " ".join(body_parts)
                wrapped = textwrap.wrap(
                    content,
                    width=width - len(fn_prefix),
                    break_long_words=False,
                    break_on_hyphens=False
                )
                if wrapped:
                    out.append(fn_prefix + wrapped[0])
                    sub_indent = "    "
                    for w in wrapped[1:]:
                        sub_wrapped = textwrap.wrap(
                            w,
                            width=width - len(sub_indent),
                            break_long_words=False,
                            break_on_hyphens=False
                        )
                        for sw in sub_wrapped:
                            out.append(sub_indent + sw)
                else:
                    out.append(fn_prefix.rstrip())
            else:
                out.extend(current_para)
        elif current_type == "list_item":
            content = " ".join([l.strip() for l in current_para])
            # Determine subsequent indent: align with prefix or cap at 4 spaces
            sub_indent = " " * len(current_prefix)
            if len(sub_indent) > 8:
                sub_indent = "    "
            wrapped = textwrap.wrap(
                content,
                width=width,
                initial_indent="",
                subsequent_indent=sub_indent,
                break_long_words=False,
                break_on_hyphens=False
            )
            out.extend(wrapped)
        elif current_type == "indented_line":
            content = " ".join([l.strip() for l in current_para])
            wrapped = textwrap.wrap(
                content,
                width=width,
                initial_indent=current_indent,
                subsequent_indent=current_indent,
                break_long_words=False,
                break_on_hyphens=False
            )
            out.extend(wrapped)
        elif current_type == "prose":
            content = " ".join([l.strip() for l in current_para])
            wrapped = textwrap.wrap(
                content,
                width=width,
                break_long_words=False,
                break_on_hyphens=False
            )
            out.extend(wrapped)
        else:
            out.extend(current_para)

        current_para = []
        current_type = None
        current_prefix = ""
        current_indent = ""

    for line in lines:
        stripped = line.strip()

        # 1. Code block fence
        if stripped.startswith("```") or stripped.startswith("````"):
            flush()
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue

        # 2. Math display block ($$)
        if stripped.startswith("$$"):
            flush()
            if stripped.endswith("$$") and len(stripped) > 2:
                out.append(line)
                continue
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

        # 4. Heading or thematic break
        if stripped.startswith("#") or stripped == "---" or stripped == "***":
            flush()
            out.append(line)
            continue

        # 5. Table row
        if stripped.startswith("|"):
            if current_type != "table":
                flush()
            current_type = "table"
            current_para.append(line)
            continue

        # 6. Footnote definition
        if re.match(r"^\[\^[^\]]+\]:\s*", line):
            flush()
            current_type = "footnote"
            current_para.append(line)
            continue

        # 7. Blockquote
        if stripped.startswith(">"):
            if current_type != "quote":
                flush()
            current_type = "quote"
            current_para.append(line)
            continue

        # 8. List item start
        is_list = False
        prefix = ""
        if (
            re.match(r"^\s*[-*+]\s+", line)
            or re.match(r"^\s*\d+\.\s+", line)
            or re.match(r"^\s*-\s+\*\*", line)
            or re.match(r"^\s*\*\*[a-zA-Z0-9\.]+\*\*\s+", line)
        ):
            is_list = True
            m_p = re.match(
                r"^(\s*(?:[-*+]\s+|\d+\.\s+)?(?:\*\*[a-zA-Z0-9\.]+\*\*\s+)?)",
                line
            )
            prefix = m_p.group(1) if m_p else ""

        if is_list and prefix.strip():
            flush()
            current_type = "list_item"
            current_prefix = prefix
            current_para.append(line)
            continue

        # 9. Indented continuation inside list (e.g. 4-space examples or sub-items)
        if (line.startswith("    ") or line.startswith("  ")) and current_type in (
            "list_item",
            "indented_line",
        ):
            flush()
            indent_match = re.match(r"^(\s+)", line)
            current_indent = indent_match.group(1) if indent_match else "    "
            current_type = "indented_line"
            current_para.append(line)
            continue

        # 10. Continuation of current block
        if current_type is not None:
            current_para.append(line)
            continue

        # 11. Standard prose
        current_type = "prose"
        current_para.append(line)

    flush()
    return "\n".join(out)

def process_file(filepath, width=80, check_only=False, dry_run=False):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if filepath.endswith((".yaml", ".yml")):
        wrapped = wrap_yaml(content, width=width)
    else:
        wrapped = wrap_markdown(content, width=width)

    # Ensure single trailing newline
    if not wrapped.endswith("\n"):
        wrapped_output = wrapped + "\n"
    else:
        wrapped_output = wrapped

    needs_change = content != wrapped_output

    if check_only:
        return needs_change

    if dry_run:
        if needs_change:
            print(f"[DRY RUN] Would reformat: {filepath}")
        return needs_change

    if needs_change:
        print(f"Formatted: {filepath}")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(wrapped_output)

    return needs_change

def collect_targets(base_dir):
    targets = []

    # 1. Walk src/
    src_dir = os.path.join(base_dir, "src")
    if os.path.exists(src_dir):
        for f in sorted(os.listdir(src_dir)):
            if f.endswith(".md"):
                targets.append(os.path.join(src_dir, f))

    # 2. Walk specs/
    specs_dir = os.path.join(base_dir, "specs")
    if os.path.exists(specs_dir):
        for f in sorted(os.listdir(specs_dir)):
            if f.endswith((".yaml", ".yml")):
                targets.append(os.path.join(specs_dir, f))

    # 3. Walk refinery/
    refinery_dir = os.path.join(base_dir, "refinery")
    if os.path.exists(refinery_dir):
        for f in sorted(os.listdir(refinery_dir)):
            if f.endswith(".md"):
                targets.append(os.path.join(refinery_dir, f))

    # 4. Root markdown files (except monolithic archives/outputs)
    for f in sorted(os.listdir(base_dir)):
        if f.endswith(".md") and f != "README.md":
            if not re.match(r"^GMRTI_\d+\.md$", f):
                targets.append(os.path.join(base_dir, f))

    readme_path = os.path.join(base_dir, "README.md")
    if os.path.exists(readme_path):
        targets.append(readme_path)

    return targets

def main():
    parser = argparse.ArgumentParser(description="Wrap Markdown and YAML files to fixed width.")
    parser.add_argument("--check", action="store_true", help="Check if files need wrapping without writing.")
    parser.add_argument("--dry-run", action="store_true", help="Show which files would be changed.")
    parser.add_argument("--width", type=int, default=80, help="Line width limit (default: 80).")
    parser.add_argument("--path", type=str, default=None, help="Target file or directory.")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))

    if args.path:
        target_path = os.path.abspath(args.path)
        if os.path.isfile(target_path):
            targets = [target_path]
        elif os.path.isdir(target_path):
            targets = collect_targets(target_path)
        else:
            print(f"Error: path not found: {args.path}")
            sys.exit(1)
    else:
        targets = collect_targets(base_dir)

    changed_count = 0
    for filepath in targets:
        changed = process_file(
            filepath,
            width=args.width,
            check_only=args.check,
            dry_run=args.dry_run
        )
        if changed:
            changed_count += 1
            if args.check:
                print(f"Unformatted: {filepath}")

    if args.check:
        if changed_count > 0:
            print(f"Total unformatted files: {changed_count}")
            sys.exit(1)
        else:
            print("All files are cleanly wrapped.")
            sys.exit(0)

if __name__ == "__main__":
    main()
