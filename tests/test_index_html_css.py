"""Static CSS/structure invariants for index.html.

index.html is the only tracked HTML artifact in this repository (.gitignore
excludes ``*.html`` but re-includes ``index.html``). It is hand-authored and
~660 KB, so nothing else in the test suite touches it. These checks are
deliberately cheap -- they parse the stylesheet as text and assert invariants
that the rendered-layout tests in test_responsive_layout.py rely on. A broken
invariant fails here in milliseconds instead of requiring a browser.

Run with: python -m pytest tests/test_index_html_css.py -v
"""

import os
import re

import pytest

VIEWPORT_META = re.compile(
    r'<meta\s+name=["\']viewport["\']\s+content=["\']width=device-width', re.I
)

# A CSS length that reserves horizontal space, e.g. min-width:62px / 62.5px
FIXED_MIN_WIDTH = re.compile(r"min-width\s*:\s*(\d+(?:\.\d+)?)px", re.I)

RESIZE_MARKER = re.compile(r"""addEventListener\(\s*["']resize["']""")


def read_index_html(base_dir):
    with open(os.path.join(base_dir, "index.html"), "r", encoding="utf-8") as fp:
        return fp.read()


def style_blocks(html):
    """Return the contents of every <style> element, concatenated."""
    return "\n".join(
        m.group(1) for m in re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S)
    )


def _parse_rules(css, media, rules):
    """Recursively collect ``(selector, body, media)`` triples from *css*.

    Blocks belonging to at-rules that hold nested rules (``@media``,
    ``@supports``, ``@keyframes``, ...) are descended into rather than reported,
    so rules found inside one carry the at-rule prelude as *media*. Recursing --
    rather than pushing onto a shared stack -- is what keeps a rule that follows
    a top-level ``@media`` block from inheriting that block's condition.
    """
    i, n, sel_start = 0, len(css), 0
    while i < n:
        ch = css[i]
        if ch == "{":
            prelude = css[sel_start:i].strip()
            depth, j = 1, i + 1
            while j < n and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            body = css[i + 1 : j - 1]
            if prelude.startswith("@"):
                _parse_rules(body, f"{media} {prelude}".strip(), rules)
            else:
                rules.append((prelude, body, media))
            sel_start = j
            i = j
            continue
        if ch == ";":
            # statement at-rule such as @import -- carries no block
            sel_start = i + 1
        i += 1


def iter_rules(css):
    """Yield ``(selector, body, media)`` for every style rule in *css*."""
    stripped = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)
    rules = []
    _parse_rules(stripped, "", rules)
    return rules


def base_rules(css):
    """Rules that are not inside any ``@media`` / ``@supports`` block."""
    return [(s, b) for s, b, media in iter_rules(css) if not media]


def selector_targets(selector, cls):
    """True if *selector* includes *cls* as a whole selector, not a variant.

    ``.toolbar`` matches, ``body.search-mode .toolbar`` and
    ``.toolbar-foo`` do not -- that distinction matters when telling a base
    declaration apart from a descendant or breakpoint override.
    """
    return any(part.strip() == cls for part in selector.split(","))


@pytest.fixture(scope="module")
def index_css(base_dir):
    return style_blocks(read_index_html(base_dir))


def test_css_parser_separates_base_rules_from_breakpoints(index_css):
    """Sanity check on the helper every other test here depends on.

    If this fails, the other tests are answering the wrong question -- e.g.
    mistaking the ``@media (max-width:900px)`` override for the base rule,
    which is precisely how the regression this file guards slipped through.
    """
    bases = [s for s, _, _ in iter_rules(index_css) if not _]
    assert ".toolbar" in bases, "base '.toolbar' rule not found outside any media query"
    # A rule that sits after the top-level @media blocks must NOT inherit them.
    assert any(
        media for _, _, media in iter_rules(index_css)
    ), "expected breakpoint-scoped rules to be present"
    assert len(bases) < len(iter_rules(index_css)), (
        "no rules were classified as breakpoint-scoped; the parser is not descending "
        "into @media blocks"
    )


def test_no_undefined_css_custom_properties(base_dir, index_css):
    """Every ``var(--x)`` reference must resolve to a declaration.

    Regression guard: ``--surface2``, ``--surface3`` and ``--text-muted`` were
    referenced 23 times but never declared (the real names are ``--surface-2``,
    ``--surface-3`` and ``--muted``). An undefined custom property makes the
    whole declaration invalid at computed-value time, so those elements silently
    fell back to transparent backgrounds and inherited text colour.
    """
    html = read_index_html(base_dir)
    declared = set(re.findall(r"(--[A-Za-z0-9_-]+)\s*:", index_css))
    referenced = set(re.findall(r"var\(\s*(--[A-Za-z0-9_-]+)", html))
    undefined = sorted(referenced - declared)
    assert not undefined, (
        "index.html references CSS custom properties that are never declared: "
        f"{undefined}. Each one silently invalidates the declaration that uses it."
    )


def test_search_count_declared_once(index_css):
    """``.search-count`` must have exactly one base declaration.

    It was declared twice in the base stylesheet; the second copy silently
    dropped ``min-width:62px`` and ``text-align:center`` from the first.
    """
    matches = [
        (s, b) for s, b in base_rules(index_css) if selector_targets(s, ".search-count")
    ]
    assert len(matches) == 1, (
        f"expected exactly one base '.search-count' declaration, found {len(matches)}: "
        f"{[s for s, _ in matches]}"
    )


def test_search_count_reserves_no_fixed_width(index_css):
    """``.search-count`` must not reserve a fixed horizontal width.

    ``min-width:62px`` is only cancelled by the ``@media (max-width:900px)`` hide,
    so between 901px and 1024px -- where the topbar has no room -- it forced the
    toolbar to shrink below its content and pushed the non-shrinkable icon buttons
    past the right edge of the screen.
    """
    for selector, body in base_rules(index_css):
        if not selector_targets(selector, ".search-count"):
            continue
        reserved = [w for w in FIXED_MIN_WIDTH.findall(body) if float(w) > 0]
        assert not reserved, (
            f"'.search-count' reserves fixed min-width:{reserved}px in its base rule. "
            "A flex item with a fixed min-width cannot shrink out of the way when the "
            "topbar runs out of room."
        )


def test_toolbar_does_not_shrink_in_base_rule(index_css):
    """``.toolbar`` must be ``flex:none`` in the base rule, not only in a breakpoint.

    ``.toolbar{flex:none}`` used to live solely inside ``@media (max-width:900px)``.
    Above 900px the toolbar was ``flex:0 1 auto``, so it shrank below its content and
    its ``flex:none`` children (#themeBtn, #settingsBtn) spilled out of it.
    """
    matches = [
        (s, b) for s, b in base_rules(index_css) if selector_targets(s, ".toolbar")
    ]
    assert len(matches) == 1, f"expected exactly one base '.toolbar' rule, found {len(matches)}"
    selector, body = matches[0]
    assert re.search(r"(^|;)\s*flex\s*:\s*none\s*(;|$)", body), (
        f"base '.toolbar' rule is not flex:none -> {selector}{{{body}}}. The toolbar must "
        "refuse to shrink below its content; '.brand span' already has "
        "text-overflow:ellipsis to absorb the squeeze."
    )


def test_inline_katex_has_overflow_guard(base_dir, index_css):
    """Inline KaTeX needs an explicit overflow guard plus the pass that applies it.

    Display math scrolls via ``.katex-display{overflow-x:auto}``. Inline math has no
    overflow container, while ``.katex .katex-base`` is ``white-space:nowrap`` with
    ``width:min-content`` -- so one long expression becomes an unbreakable box that
    widens the whole document past the viewport, where ``html{overflow-x:hidden}``
    silently clips it.
    """
    guard = [
        (s, b) for s, b, _ in iter_rules(index_css) if selector_targets(s, ".katex--overflow")
    ]
    assert guard, "no '.katex--overflow' rule found; inline KaTeX has no overflow guard"

    body = guard[0][1].replace(" ", "")
    assert "overflow-x:auto" in body, (
        f"'.katex--overflow' must scroll horizontally, got: {{{guard[0][1]}}}"
    )
    assert "max-width:100%" in body, (
        f"'.katex--overflow' must be capped at max-width:100%, got: {{{guard[0][1]}}}"
    )

    html = read_index_html(base_dir)
    assert re.search(r"function\s+fitInlineMath\s*\(", html), (
        "no fitInlineMath() definition found; the '.katex--overflow' class is never applied"
    )
    assert re.search(r"fitInlineMath\s*\(\s*\)", html), "fitInlineMath() is never called"


def test_math_fit_pass_reruns_on_resize(base_dir):
    """The fit pass must re-run on resize, or rotating the device reintroduces the bug.

    Matching is window-based rather than bracket-balanced: the handler is
    ``addEventListener("resize", () => {...})`` and a naive ``[^)]*`` pattern
    stops at the ``()`` of the arrow function before ever reaching the body.
    """
    html = read_index_html(base_dir)
    hooked = any(
        "fitInlineMath" in html[m.end() : m.end() + 400] for m in RESIZE_MARKER.finditer(html)
    )
    assert hooked, (
        "no resize listener re-runs fitInlineMath; rotating the device would leave stale "
        "'.katex--overflow' classes and reintroduce the horizontal overflow"
    )


def test_viewport_meta_present(base_dir):
    """Without ``width=device-width`` a mobile browser lays out at ~980px and the
    media queries never fire, silently disabling every mobile breakpoint."""
    assert VIEWPORT_META.search(read_index_html(base_dir)), (
        "index.html is missing <meta name='viewport' content='width=device-width,...'>"
    )