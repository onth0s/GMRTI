import os
import yaml
import pytest
from wrap import wrap_yaml, wrap_markdown, process_file


def test_wrap_yaml_preserves_block_scalar_indentation():
    sample = (
        "concept_id: GMRTI-TEST\n"
        "name: \"A test concept\"\n"
        "invariants:\n"
        "  - >-\n"
        "      Self-Annotation is the foundational sandbox covenant that needs"
        " extra length to trigger wrapping across multiple lines cleanly.\n"
    )
    wrapped = wrap_yaml(sample, width=60)
    parsed = yaml.safe_load(wrapped)
    assert parsed["concept_id"] == "GMRTI-TEST"
    assert "Self-Annotation" in parsed["invariants"][0]
    for line in wrapped.splitlines():
        if any(w in line for w in ["Self-Annotation", "foundational", "cleanly"]):
            assert line.startswith("      ")


def test_wrap_yaml_converts_long_quotes_to_block_scalar():
    sample = (
        'long_val: "This is a very long string that should be converted'
        ' into a block scalar automatically when it exceeds width."'
    )
    wrapped = wrap_yaml(sample, width=50)
    parsed = yaml.safe_load(wrapped)
    assert "long_val" in parsed
    assert wrapped.startswith("long_val: >-")


def test_wrap_markdown_indented_list_continuation():
    sample = (
        "1.  **Causal**: Concept A physically makes Concept B happen.\n"
        "    *Example*: *Fire* makes *Smoke*.\n"
        "2.  **Inferential**: If A is true, B must also be true."
    )
    wrapped = wrap_markdown(sample, width=80)
    lines = wrapped.splitlines()
    assert lines[0].startswith("1.  **Causal**")
    assert lines[1].startswith("    *Example*:")
    assert lines[2].startswith("2.  **Inferential**")


def test_wrap_markdown_protects_math_blocks():
    sample = "$$\nA_{t+1} = A_t + very long math expression that would otherwise exceed eighty characters\n$$"
    wrapped = wrap_markdown(sample, width=50)
    assert "$$" in wrapped
    assert len(wrapped.splitlines()) == 3


def test_wrap_markdown_protects_code_blocks():
    sample = "```python\ndef very_long_function_name_that_should_never_be_wrapped_by_a_markdown_formatter():\n    pass\n```"
    wrapped = wrap_markdown(sample, width=50)
    assert "def very_long_function_name_that_should_never_be_wrapped_by_a_markdown_formatter():" in wrapped


def test_wrap_markdown_footnote():
    sample = "[^1]: The precise formula is: Updated Guide = Current Guide + lambda * delta."
    wrapped = wrap_markdown(sample, width=40)
    lines = wrapped.splitlines()
    assert lines[0].startswith("[^1]: ")
    assert len(lines) > 1
    assert lines[1].startswith("    ")


# ── Phase 2 new tests ───────────────────────────────────────────────────────

def test_wrap_markdown_blockquote_reflowed():
    """Blockquote lines are joined and reflowed within width - 2."""
    sample = "> This is a blockquote that is much longer than eighty characters and must be reflowed by the wrapper."
    wrapped = wrap_markdown(sample, width=50)
    for line in wrapped.splitlines():
        assert line.startswith("> "), f"Missing '> ' prefix: {line!r}"
        assert len(line) <= 50, f"Exceeds width: {line!r}"


def test_wrap_markdown_table_rows_pass_through():
    """Table rows pass through verbatim — never reflowed."""
    sample = (
        "| A | B | Very long cell that would exceed target width |\n"
        "| --- | --- | --- |\n"
        "| v1 | v2 | v3 |"
    )
    wrapped = wrap_markdown(sample, width=40)
    lines = wrapped.splitlines()
    assert lines[0].startswith("| A")
    assert lines[1].startswith("| ---")
    assert lines[2].startswith("| v1")


def test_wrap_markdown_four_backtick_fence_protected():
    """4-backtick fences are treated as code blocks and not reflowed."""
    inner = "This is a very long line inside a four-backtick fence that must not be wrapped at all."
    sample = "````markdown\n" + inner + "\n````"
    wrapped = wrap_markdown(sample, width=40)
    assert inner in wrapped


def test_wrap_markdown_prose_reflowed():
    """Plain prose paragraphs are reflowed to the target width."""
    long_line = (
        "The semantic covenant is the totality of meaning-relations held by"
        " a rational entity at a given moment."
    )
    wrapped = wrap_markdown(long_line, width=50)
    for line in wrapped.splitlines():
        assert len(line) <= 50, f"Exceeds width: {line!r}"
    assert "semantic covenant" in wrapped
    assert "rational entity" in wrapped


def test_process_file_round_trip_idempotent(tmp_path):
    """process_file is idempotent: a second pass produces no changes."""
    sample = "# Heading\n\nShort paragraph that fits within eighty characters.\n\n- Item one\n- Item two\n"
    target = tmp_path / "test.md"
    target.write_text(sample, encoding="utf-8")
    process_file(str(target), width=80)
    after_first = target.read_text(encoding="utf-8")
    changed_second = process_file(str(target), width=80)
    after_second = target.read_text(encoding="utf-8")
    assert after_first == after_second, "process_file is not idempotent"
    assert not changed_second, "Second pass should detect no changes"


def test_wrap_yaml_unquoted_long_key_value():
    """Branch 2: unquoted long key-value lines become block scalars."""
    sample = "description: This is a very long unquoted value that goes well beyond the fifty character limit set here."
    wrapped = wrap_yaml(sample, width=50)
    assert "description: >-" in wrapped
    parsed = yaml.safe_load(wrapped)
    assert "long unquoted value" in parsed["description"]


def test_wrap_yaml_unquoted_long_list_item():
    """Branch 4: unquoted long list items become block scalars."""
    sample = "items:\n  - This is a very long unquoted list item that exceeds the fifty character line limit by quite a lot."
    wrapped = wrap_yaml(sample, width=50)
    assert "- >-" in wrapped
    parsed = yaml.safe_load(wrapped)
    assert "long unquoted list item" in parsed["items"][0]


def test_wrap_yaml_long_comment_reflowed():
    """Branch 5: long YAML comments are reflowed to target width."""
    sample = "# This is a very long YAML comment that should be reflowed by the wrap_yaml function to fit within the width limit."
    wrapped = wrap_yaml(sample, width=50)
    for line in wrapped.splitlines():
        assert line.startswith("# "), f"Missing '# ' prefix: {line!r}"
        assert len(line) <= 50, f"Exceeds width: {line!r}"


def test_wrap_markdown_empty_blockquote():
    """Empty blockquote line '>' preserves '>' marker."""
    sample = ">"
    wrapped = wrap_markdown(sample, width=50)
    assert wrapped == ">"


def test_wrap_markdown_bold_prefixed_clause():
    """Bold clause identifier without leading dash is recognized as a list/item prefix."""
    sample = "**1a.1** This is a bold prefixed clause that exceeds the wrap limit and must flow cleanly."
    wrapped = wrap_markdown(sample, width=40)
    lines = wrapped.splitlines()
    assert lines[0].startswith("**1a.1**")
    assert len(lines) > 1
    # For prefixes longer than 8 chars (e.g. "**1a.1** " = 9), sub_indent caps at 4 spaces
    assert lines[1].startswith("    ")


def test_process_file_dry_run(tmp_path):
    """process_file with dry_run=True reports changes needed without modifying file."""
    sample = "# Heading\n\nThis is a very long paragraph that will definitely need to be wrapped to eighty columns.\n"
    target = tmp_path / "dry_run_test.md"
    target.write_text(sample, encoding="utf-8")

    needs_change = process_file(str(target), width=40, dry_run=True)
    assert needs_change is True
    assert target.read_text(encoding="utf-8") == sample, "File should remain unmodified during dry_run"


def test_wrap_yaml_flow_sequence_mapping_not_converted_to_block_scalar():
    """Flow sequences like deps: [A, B] should not be converted to 'deps: >-'."""
    sample = "dependencies: [GMRTI-COVENANT, GMRTI-ENTROPY, GMRTI-TOPOLOGY, GMRTI-DEPTH]"
    wrapped = wrap_yaml(sample, width=30)
    assert "dependencies: >-" not in wrapped
    assert "dependencies: [" in wrapped or "dependencies:" in wrapped


def test_wrap_markdown_single_line_display_math():
    """Single-line display math $$...$$ passes through verbatim without toggling state."""
    sample = "Intro paragraph.\n\n$$H_s(S) = \\log_2 |\\{G_R : G_R \\text{ is compatible with } S\\}|$$\n\nOutro paragraph."
    wrapped = wrap_markdown(sample, width=40)
    assert "$$H_s(S) = \\log_2 |\\{G_R : G_R \\text{ is compatible with } S\\}|$$" in wrapped


def test_wrap_markdown_nested_fences():
    """3-backtick code block inside 4-backtick fence is preserved."""
    sample = "````markdown\n```python\nprint('hello')\n```\n````"
    wrapped = wrap_markdown(sample, width=40)
    assert "```python" in wrapped
    assert "print('hello')" in wrapped


def test_collect_targets_excludes_agents_md(base_dir):
    """collect_targets must never include AGENTS.md in targets."""
    from wrap import collect_targets
    targets = collect_targets(base_dir)
    target_basenames = [os.path.basename(t) for t in targets]
    assert "AGENTS.md" not in target_basenames
    assert "README.md" in target_basenames
