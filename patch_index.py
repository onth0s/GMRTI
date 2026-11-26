"""patch_index.py — Idempotent post-processor for generated index.html.

Ensures exported MDD builds in ``index.html`` retain the responsive CSS and
inline-KaTeX overflow guards verified by ``tests/test_index_html_css.py`` and
``tests/test_responsive_layout.py``.

Invocation
----------
    python patch_index.py             # patch index.html in-place if needed
    python patch_index.py --check     # verify compliance; exit 1 if patches needed
    python patch_index.py --dry-run   # report whether index.html would change
    python patch_index.py --path FILE # target a specific HTML file
"""
import os
import re
import sys

from _gmrti_common import (
    build_base_parser,
    exit_for_check,
    get_repo_root,
    read_utf8,
    write_utf8,
)

KATEX_OVERFLOW_CSS = (
    ".katex--overflow{display:block;max-width:100%;overflow-x:auto;"
    "overflow-y:hidden;padding:2px 0}"
)

FIT_INLINE_MATH_JS = """
// Promote only inline KaTeX expressions that overflow their container.
function fitInlineMath() {
  for (const el of document.querySelectorAll(".katex")) {
    if (el.closest(".katex-display")) continue;
    el.classList.remove("katex--overflow");
    const avail = el.parentElement.getBoundingClientRect().width;
    const wide = el.getBoundingClientRect().width;
    if (wide > avail + 2) el.classList.add("katex--overflow");
  }
}
let fitInlineMathRaf;
window.addEventListener("resize", () => {
  cancelAnimationFrame(fitInlineMathRaf);
  fitInlineMathRaf = requestAnimationFrame(fitInlineMath);
});
if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitInlineMath);
fitInlineMath();
""".strip()


def _patch_style(css: str) -> str:
    """Apply required CSS invariants to a <style> block body."""
    # 1. Declare --svg-min-w in :root if referenced/missing
    if "--svg-min-w:" not in css:
        css = re.sub(
            r"(:root\s*\{)",
            r"\1--svg-min-w:0px;",
            css,
            count=1,
        )

    # 2. Ensure base .toolbar rule includes flex:none
    def _add_toolbar_flex(match: re.Match) -> str:
        body = match.group(2)
        if re.search(r"(^|;)\s*flex\s*:\s*none\s*(;|$)", body):
            return match.group(0)
        sep = "" if body.endswith(";") or not body.strip() else ";"
        return f"{match.group(1)}{body}{sep}flex:none{match.group(3)}"

    css = re.sub(
        r"(\.toolbar\s*\{)([^}]*)(\})",
        _add_toolbar_flex,
        css,
        count=1,
    )

    # 3. Inject .katex--overflow rule if missing
    if ".katex--overflow" not in css:
        if ".katex-display{" in css:
            css = css.replace(
                ".katex-display{",
                f"{KATEX_OVERFLOW_CSS}.katex-display{{",
                1,
            )
        else:
            css = css + KATEX_OVERFLOW_CSS

    return css


def patch_html(html: str) -> str:
    """Return patched HTML with all responsive/KaTeX invariants enforced."""
    # Patch first <style>...</style> block
    def _replace_style(match: re.Match) -> str:
        return f"{match.group(1)}{_patch_style(match.group(2))}{match.group(3)}"

    patched = re.sub(
        r"(<style[^>]*>)(.*?)(</style>)",
        _replace_style,
        html,
        count=1,
        flags=re.S,
    )

    # Inject fitInlineMath() and resize listener if missing
    if not re.search(r"function\s+fitInlineMath\s*\(", patched):
        script_tag = f"<script>\n{FIT_INLINE_MATH_JS}\n</script>"
        if "</body>" in patched:
            patched = patched.replace("</body>", f"{script_tag}</body>", 1)
        else:
            patched = patched + script_tag

    return patched


def process_index_file(
    filepath: str, check_only: bool = False, dry_run: bool = False
) -> bool:
    """Inspect or patch *filepath*. Returns True if changes were needed."""
    original = read_utf8(filepath)

    patched = patch_html(original)
    needs_change = original != patched

    if check_only or dry_run:
        if dry_run and needs_change:
            print(f"[DRY RUN] Would patch: {filepath}")
        return needs_change

    if needs_change:
        write_utf8(filepath, patched)
        print(f"Patched: {filepath}")

    return needs_change


def main() -> None:
    parser = build_base_parser(
        description="Idempotently patch index.html responsive CSS and KaTeX guards.",
        check_help="Check if index.html requires patching without writing.",
        dry_run_help="Report whether index.html would be modified.",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Target HTML filepath (defaults to index.html in repo root).",
    )
    args = parser.parse_args()

    base_dir = get_repo_root(__file__)
    target = (
        os.path.abspath(args.path)
        if args.path
        else os.path.join(base_dir, "index.html")
    )

    if not os.path.isfile(target):
        print(f"Error: file not found: {target}")
        sys.exit(1)

    try:
        needs_change = process_index_file(
            target, check_only=args.check, dry_run=args.dry_run
        )
    except OSError as exc:
        print(f"Error processing {target}: {exc}")
        sys.exit(1)

    if args.check:
        exit_for_check(
            not needs_change,
            f"HTML invariants verified: {target}",
            f"Unpatched HTML: {target}",
        )


if __name__ == "__main__":
    main()
