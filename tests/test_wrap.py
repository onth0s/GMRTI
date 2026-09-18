import yaml
import pytest
from wrap import wrap_yaml, wrap_markdown

def test_wrap_yaml_preserves_block_scalar_indentation():
    sample = """concept_id: GMRTI-TEST
name: "A test concept"
invariants:
  - >-
      Self-Annotation is the foundational sandbox covenant that needs extra length to trigger wrapping across multiple lines cleanly.
"""
    wrapped = wrap_yaml(sample, width=60)
    # Parse with PyYAML to ensure syntax remains valid
    parsed = yaml.safe_load(wrapped)
    assert parsed["concept_id"] == "GMRTI-TEST"
    assert "Self-Annotation" in parsed["invariants"][0]

    # Verify no line inside the block scalar drops to 0 indent
    for line in wrapped.splitlines():
        if "Self-Annotation" in line or "foundational" in line or "cleanly" in line:
            assert line.startswith("      ")

def test_wrap_yaml_converts_long_quotes_to_block_scalar():
    sample = 'long_val: "This is a very long string that should be converted into a block scalar automatically when it exceeds width."'
    wrapped = wrap_yaml(sample, width=50)
    parsed = yaml.safe_load(wrapped)
    assert "long_val" in parsed
    assert wrapped.startswith("long_val: >-")

def test_wrap_markdown_indented_list_continuation():
    sample = """1.  **Causal** (`[->causal]`): Concept A physically makes Concept B happen.
    *Example*: *Fire* `[->causal]` *Smoke*.
2.  **Inferential** (`[->inferential]`): If Concept A is true, Concept B must also be true."""

    wrapped = wrap_markdown(sample, width=80)
    lines = wrapped.splitlines()
    assert lines[0].startswith("1.  **Causal**")
    assert lines[1].startswith("    *Example*:")
    assert lines[2].startswith("2.  **Inferential**")

def test_wrap_markdown_protects_math_blocks():
    sample = """$$
A_{t+1} = A_t + \\lambda (A_{decl} - A_t) + \\text{very long math expression that would otherwise exceed eighty characters}
$$"""
    wrapped = wrap_markdown(sample, width=50)
    assert "$$" in wrapped
    # Inner math expression must not be reflowed into prose
    lines = wrapped.splitlines()
    assert len(lines) == 3

def test_wrap_markdown_protects_code_blocks():
    sample = """```python
def very_long_function_name_that_should_never_be_wrapped_by_a_markdown_formatter():
    pass
```"""
    wrapped = wrap_markdown(sample, width=50)
    assert "def very_long_function_name_that_should_never_be_wrapped_by_a_markdown_formatter():" in wrapped

def test_wrap_markdown_footnote():
    sample = "[^1]: The precise formula is: Updated Guide = Current Guide + lambda * delta."
    wrapped = wrap_markdown(sample, width=40)
    lines = wrapped.splitlines()
    assert lines[0].startswith("[^1]: ")
    assert len(lines) > 1
    assert lines[1].startswith("    ")
