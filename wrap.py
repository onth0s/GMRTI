import os
import textwrap
import re

def wrap_yaml(text, width=80):
    lines = []
    for line in text.splitlines():
        if len(line) <= width:
            lines.append(line)
            continue
        
        # 1. Key-value string replacement
        key_match = re.match(r"^(\s*)(\w+):\s*\"([^\"]+)\"", line)
        if key_match:
            indent = key_match.group(1)
            key = key_match.group(2)
            val = key_match.group(3)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 2)
            lines.append(f"{indent}{key}: >-")
            for wl in wrapped_val:
                lines.append(f"{indent}  {wl}")
            continue
            
        # 2. List item string replacement
        list_match = re.match(r"^(\s*)-\s*\"([^\"]+)\"", line)
        if list_match:
            indent = list_match.group(1)
            val = list_match.group(2)
            wrapped_val = textwrap.wrap(val, width=width - len(indent) - 4)
            lines.append(f"{indent}- >-")
            for wl in wrapped_val:
                lines.append(f"{indent}    {wl}")
            continue
            
        # Fallback if no regex match (just wrap on characters/words)
        lines.extend(textwrap.wrap(line, width=width, break_long_words=False, break_on_hyphens=False))
        
    return "\n".join(lines)

def wrap_markdown(text, width=80):
    lines = text.splitlines()
    blocks = []
    
    current_block_type = None # 'prose', 'list', 'code', 'quote', 'table'
    current_block_lines = []
    
    in_code = False
    
    for line in lines:
        stripped = line.strip()
        
        # 1. Code block toggle
        if stripped.startswith("```"):
            if current_block_lines:
                blocks.append((current_block_type, current_block_lines))
                current_block_lines = []
                current_block_type = None
            in_code = not in_code
            blocks.append(('code_boundary', [line]))
            continue
            
        if in_code:
            blocks.append(('code_line', [line]))
            continue
            
        # 2. Empty line
        if not stripped:
            if current_block_lines:
                blocks.append((current_block_type, current_block_lines))
                current_block_lines = []
                current_block_type = None
            blocks.append(('empty', ['']))
            continue
            
        # 3. Horizontal rule or heading
        if stripped.startswith("#") or stripped == "---":
            if current_block_lines:
                blocks.append((current_block_type, current_block_lines))
                current_block_lines = []
                current_block_type = None
            blocks.append(('heading', [line]))
            continue
            
        # 4. Table row
        if stripped.startswith("|"):
            if current_block_lines and current_block_type != 'table':
                blocks.append((current_block_type, current_block_lines))
                current_block_lines = []
            current_block_type = 'table'
            current_block_lines.append(line)
            continue
            
        # 5. Blockquote
        if stripped.startswith(">"):
            if current_block_lines and current_block_type != 'quote':
                blocks.append((current_block_type, current_block_lines))
                current_block_lines = []
            current_block_type = 'quote'
            current_block_lines.append(line)
            continue
            
        # 6. List item start
        # Detect list start using regex
        # - list items
        # * list items
        # 1. list items
        # **1a.1** address items
        # - **1a.1i** nested address items
        is_list_start = False
        list_prefixes = [
            r"^\s*-\s+", 
            r"^\s*\*\s+", 
            r"^\s*\d+\.\s+", 
            r"^\s*\d+[a-z]\.[a-zA-Z0-9\.]+\s+", 
            r"^\s*\*\*[a-zA-Z0-9\.]+\*\*\s+",
            r"^\s*-\s+\*\*[a-zA-Z0-9\.]+\*\*\s+"
        ]
        for lp in list_prefixes:
            if re.match(lp, line):
                is_list_start = True
                break
                
        if is_list_start:
            if current_block_lines:
                blocks.append((current_block_type, current_block_lines))
                current_block_lines = []
            current_block_type = 'list'
            current_block_lines.append(line)
            continue
            
        # 7. Standard prose continuation
        if current_block_type is None:
            current_block_type = 'prose'
        elif current_block_type != 'prose':
            blocks.append((current_block_type, current_block_lines))
            current_block_lines = []
            current_block_type = 'prose'
            
        current_block_lines.append(line)
        
    if current_block_lines:
        blocks.append((current_block_type, current_block_lines))
        
    # Rebuild document
    out_lines = []
    for btype, blines in blocks:
        if btype == 'empty':
            out_lines.append('')
        elif btype == 'code_boundary':
            out_lines.extend(blines)
        elif btype == 'code_line':
            # Code lines wrapped on width if long
            for l in blines:
                if len(l) > width:
                    out_lines.extend(textwrap.wrap(l, width=width, break_long_words=False, break_on_hyphens=False))
                else:
                    out_lines.append(l)
        elif btype == 'heading':
            for l in blines:
                if len(l) > width:
                    stripped_l = l.lstrip('#')
                    hashes = l[:len(l)-len(stripped_l)]
                    wrapped_sub = textwrap.wrap(stripped_l.strip(), width=width - len(hashes))
                    out_lines.append(hashes + " " + wrapped_sub[0])
                    for wl in wrapped_sub[1:]:
                        out_lines.append(wl)
                else:
                    out_lines.append(l)
        elif btype == 'table':
            out_lines.extend(blines)
        elif btype == 'quote':
            quote_content_lines = []
            for l in blines:
                stripped_quote = re.sub(r"^>\s*", "", l)
                quote_content_lines.append(stripped_quote)
            quote_text = " ".join(quote_content_lines)
            wrapped_quote = textwrap.wrap(quote_text, width=width - 2, break_long_words=False, break_on_hyphens=False)
            for wq in wrapped_quote:
                out_lines.append("> " + wq)
        elif btype == 'list':
            first_line = blines[0]
            # Match list prefix like "- **1a.1i** " or "**1a.1** " or "- "
            prefix_match = re.match(
                r"^(\s*(?:-\s+|\*\s+|\d+\.\s+)?(?:\*\*[a-zA-Z0-9\.]+\*\*\s+)?)(.*)", 
                first_line
            )
            if prefix_match:
                prefix = prefix_match.group(1)
                content = " ".join([l.strip() for l in blines])
                body = content[len(prefix):]
                
                # Align subsequent indent to prefix length, but limit it
                subsequent_indent = " " * len(prefix)
                if len(subsequent_indent) > 16:
                    subsequent_indent = " " * 4
                
                wrapped = textwrap.wrap(content, width=width, initial_indent="", subsequent_indent=subsequent_indent, break_long_words=False, break_on_hyphens=False)
                # Fix first line to preserve the exact prefix and indentation
                if wrapped:
                    # Replace prefix on first line to ensure no double-prefix or bad alignment
                    indent_only = first_line[:len(first_line)-len(first_line.lstrip())]
                    wrapped[0] = indent_only + prefix.strip() + " " + body[:len(wrapped[0]) - len(prefix)].strip()
                    # Re-wrap if there is leftover body
                    leftover = body[len(wrapped[0]) - len(prefix):].strip()
                    if leftover:
                        wrapped_sub = textwrap.wrap(leftover, width=width - len(subsequent_indent), break_long_words=False, break_on_hyphens=False)
                        wrapped = [wrapped[0]] + [subsequent_indent + wl for wl in wrapped_sub]
                out_lines.extend(wrapped)
            else:
                out_lines.extend(blines)
        elif btype == 'prose':
            content = " ".join([l.strip() for l in blines])
            wrapped = textwrap.wrap(content, width=width, break_long_words=False, break_on_hyphens=False)
            out_lines.extend(wrapped)
            
    return "\n".join(out_lines)

def process_file(filepath):
    print(f"Processing: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    if filepath.endswith(".yaml"):
        wrapped = wrap_yaml(content, width=80)
    else:
        wrapped = wrap_markdown(content, width=80)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(wrapped + "\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    targets = []
    
    # 1. Walk src/
    src_dir = os.path.join(base_dir, "src")
    if os.path.exists(src_dir):
        for f in os.listdir(src_dir):
            if f.endswith(".md"):
                targets.append(os.path.join(src_dir, f))
                
    # 2. Walk specs/
    specs_dir = os.path.join(base_dir, "specs")
    if os.path.exists(specs_dir):
        for f in os.listdir(specs_dir):
            if f.endswith(".yaml"):
                targets.append(os.path.join(specs_dir, f))
                
    # 3. Walk refinery/
    refinery_dir = os.path.join(base_dir, "refinery")
    if os.path.exists(refinery_dir):
        for f in os.listdir(refinery_dir):
            if f.endswith(".md"):
                targets.append(os.path.join(refinery_dir, f))
                
    # 4. Root markdown files
    for f in os.listdir(base_dir):
        if f.endswith(".md") and f != "README.md":
            if not re.match(r"^GMRTI_\d+\.md$", f):
                targets.append(os.path.join(base_dir, f))
                
    targets.append(os.path.join(base_dir, "README.md"))

    for filepath in targets:
        process_file(filepath)

if __name__ == "__main__":
    main()
