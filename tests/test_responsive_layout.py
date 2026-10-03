"""Rendered-layout regression tests for index.html.

These are the tests that would actually have caught the mobile layout bug.

The bug: inline KaTeX has no horizontal-overflow guard (``display`` math has
one via ``.katex-display{overflow-x:auto}``), and ``.katex-base`` is
``white-space:nowrap`` + ``width:min-content``. One long expression --
``Σ={GameActive,ResignationDeclared,...}`` at 650px inside a 328px ``<li>`` --
therefore widened the whole document to a *constant* 685px regardless of
viewport, and ``html{overflow-x:hidden}`` clipped it. No scrollbar appeared, so
it read as "the layout got wider for no reason" rather than as an overflow.

No test touched index.html before this file, which is why it shipped.

Widths sit either side of every breakpoint in the stylesheet
(480/560/640/641/768/900/901/1024) plus the common phone sizes. A single page
visit performs every measurement, so adding a width costs ~1s rather than a test.

Skipped automatically when Playwright or its browser binaries are unavailable,
so the suite still passes on a machine without them.

Run with: python -m pytest tests/test_responsive_layout.py -v
"""

import os

import pytest

# Either side of every media-query breakpoint, plus common device widths.
BREAKPOINT_WIDTHS = [
    320,  # smallest supported phone
    360,
    375,  # iPhone SE / mini
    414,  # iPhone XR/11
    540,
    640,  # last width where search collapses to a toggle
    641,  # first width where the search box is inline
    768,
    900,  # last width where the sidebar is off-canvas
    901,  # first width where the desktop grid returns -- the topbar overflowed here
    940,
    1024,
]

# Search collapses behind a toggle at <=640px, so search mode is only reachable
# below that width.
SEARCH_TOGGLE_WIDTHS = [320, 375, 414, 480, 640]

# An active query is what fills in #searchCount, and that counter is what reserved
# 62px of toolbar and overflowed the topbar at 901-1024px.
ACTIVE_QUERY_WIDTHS = [320, 640, 901, 940, 1024]

# The mode switch is JS-hidden while there are no mirror blocks. It is ~140px
# wide when shown, so it is the topbar's worst case once mirror content exists.
MODE_SWITCH_WIDTHS = [768, 901, 1024]

ROTATION_SEQUENCE = [375, 900, 320, 768, 1024, 360]

QUERY = "covenant"

# Everything a single test needs, measured in one pass so each width costs one
# page visit rather than one visit per assertion.
MEASURE_JS = """
() => {
  const de = document.documentElement;
  const topbar = document.querySelector('.topbar');
  const counter = document.getElementById('searchCount');
  const bad = [];

  for (const k of document.querySelectorAll('.katex')) {
    if (k.closest('.katex-display')) continue;          // display math scrolls already
    const txt = k.textContent.trim().replace(/\\s+/g, ' ').slice(0, 60);
    if (k.classList.contains('katex--overflow')) {
      // A promoted expression must scroll, not crop: its overflow-y is hidden, so
      // vertical excess means ascenders / big-operator overhang got cut off.
      const vClip = k.scrollHeight - k.clientHeight;
      if (vClip > 1) bad.push({ reason: 'vertically clipped', txt, vClip });
    } else {
      const avail = k.parentElement.getBoundingClientRect().width;
      const wide = k.getBoundingClientRect().width;
      if (wide > avail + 2) {
        bad.push({ reason: 'over-wide inline math not contained', txt,
                   wide: +wide.toFixed(1), avail: +avail.toFixed(1) });
      }
    }
  }

  return {
    vw: de.clientWidth,
    pageOverflow: de.scrollWidth - de.clientWidth,
    topbarOverflow: topbar.scrollWidth - topbar.clientWidth,
    badMath: bad,
    counterText: (counter.textContent || '').trim(),
    counterWidth: +counter.getBoundingClientRect().width.toFixed(1),
    counterCropped: counter.scrollWidth - counter.clientWidth,
  };
}
"""


@pytest.fixture(scope="session")
def browser():
    """Headless Chromium, or a skip if Playwright/browsers are not installed."""
    api = pytest.importorskip(
        "playwright.sync_api", reason="playwright is not installed"
    )
    with api.sync_playwright() as driver:
        try:
            instance = driver.chromium.launch()
        except Exception as exc:  # pragma: no cover - environment dependent
            pytest.skip(
                "chromium unavailable (run `python -m playwright install`): " f"{exc}"
            )
        yield instance
        instance.close()


@pytest.fixture(scope="session")
def index_url(base_dir):
    return "file:///" + os.path.join(base_dir, "index.html").replace("\\", "/")


def visit(browser, url, width, setup=None):
    """Open index.html at *width*, optionally interact, then measure.

    Returns ``(measurement, page_errors)``. Page errors are surfaced because a
    thrown exception in the layout guard would silently leave every expression
    unscoped while still looking like a pass.
    """
    page = browser.new_page(viewport={"width": width, "height": 800})
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    try:
        page.goto(url, wait_until="load")
        page.wait_for_timeout(900)  # let the inlined KaTeX fonts settle
        if setup is not None:
            setup(page)
        return page.evaluate(MEASURE_JS), errors
    finally:
        page.close()


def open_search(page):
    """Enter the collapsed search mode used at <=640px."""
    toggle = page.locator("#searchToggle")
    if toggle.is_visible():
        toggle.click()
        page.wait_for_timeout(300)


def open_search_and_query(page):
    open_search(page)
    page.fill("#search", QUERY)
    page.wait_for_timeout(600)


def force_mode_switch(page):
    """Reveal the reading-mode switch the page hides absent mirror content."""
    page.evaluate(
        "() => { document.getElementById('modeSwitch').style.display = 'inline-flex'; }"
    )
    page.wait_for_timeout(200)


def assert_clean(measurement, errors, context):
    assert not errors, f"{context}: uncaught page errors -> {errors}"
    assert measurement["pageOverflow"] <= 0, (
        f"{context}: document is {measurement['pageOverflow']}px wider than the "
        f"{measurement['vw']}px viewport. Content runs off the right edge and is "
        "clipped by html{overflow-x:hidden}, so no scrollbar reveals it."
    )
    assert measurement["topbarOverflow"] <= 0, (
        f"{context}: the topbar overflows its own box by "
        f"{measurement['topbarOverflow']}px at {measurement['vw']}px -- the search row "
        "is wider than the screen."
    )
    assert not measurement["badMath"], (
        f"{context}: inline KaTeX is not contained -> {measurement['badMath']}"
    )


@pytest.mark.parametrize("width", BREAKPOINT_WIDTHS)
def test_layout_fits_at_width(browser, index_url, width):
    """The document, the topbar, and every inline math expression must fit."""
    measurement, errors = visit(browser, index_url, width)
    assert measurement["vw"] == width
    assert_clean(measurement, errors, f"default layout @{width}px")


@pytest.mark.parametrize("width", SEARCH_TOGGLE_WIDTHS)
def test_search_mode_fits_at_width(browser, index_url, width):
    """Opening the collapsed search box must not widen anything.

    This is the state the bug was reported from: at <=640px the search box is
    hidden behind a toggle, and once opened it shares the row with the toolbar.
    """
    measurement, errors = visit(browser, index_url, width, setup=open_search)
    assert_clean(measurement, errors, f"search mode @{width}px")


@pytest.mark.parametrize("width", ACTIVE_QUERY_WIDTHS)
def test_active_query_fits_at_width(browser, index_url, width):
    """A live query -- and the result counter it fills in -- must not widen anything."""
    measurement, errors = visit(
        browser, index_url, width, setup=open_search_and_query
    )
    assert_clean(measurement, errors, f"active query @{width}px")


@pytest.mark.parametrize("width", MODE_SWITCH_WIDTHS)
def test_topbar_fits_with_mode_switch_shown(browser, index_url, width):
    """The topbar must still fit with the reading-mode switch visible.

    The switch is hidden by JS only because the current build has no mirror
    blocks. Showing it adds ~140px to the row, making this the topbar's worst
    case the moment mirror content is added.
    """
    measurement, errors = visit(browser, index_url, width, setup=force_mode_switch)
    assert_clean(measurement, errors, f"mode switch shown @{width}px")


@pytest.mark.parametrize("width", [901, 940, 1024])
def test_search_counter_stays_readable(browser, index_url, width):
    """``#searchCount`` must be laid out at content width, not clipped or collapsed.

    It used to reserve ``min-width:62px`` while being hidden at <=900px only, so
    from 901px to 1024px it held 62px of a topbar that had no room for it.
    """
    measurement, errors = visit(
        browser, index_url, width, setup=open_search_and_query
    )
    assert_clean(measurement, errors, f"active query @{width}px")
    assert measurement["counterText"], f"@{width}px: search counter is empty"
    assert measurement["counterWidth"] > 0, (
        f"@{width}px: search counter collapsed to zero width -- a flex item with "
        "min-width:0 and no content budget disappears entirely"
    )
    assert measurement["counterCropped"] <= 1, (
        f"@{width}px: search counter is cropped by "
        f"{measurement['counterCropped']}px -- text={measurement['counterText']!r}"
    )


def test_no_overflow_after_orientation_change(browser, index_url):
    """Rotating or resizing must re-fit the layout, not keep stale measurements.

    The guard runs on load and on a rAF-debounced resize; if that hook were
    dropped the page would look correct until the first rotation.
    """
    page = browser.new_page(viewport={"width": ROTATION_SEQUENCE[0], "height": 800})
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    results = []
    try:
        page.goto(index_url, wait_until="load")
        page.wait_for_timeout(900)
        for width in ROTATION_SEQUENCE:
            page.set_viewport_size({"width": width, "height": 800})
            page.wait_for_timeout(500)
            results.append(page.evaluate(MEASURE_JS))
    finally:
        page.close()

    assert not errors, f"uncaught page errors during rotation -> {errors}"
    for measurement in results:
        assert_clean(measurement, errors, f"after resizing to {measurement['vw']}px")