from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from app.explain import ITEMS, REQUIRED_KEYS, deep_pane, explain_block


def test_catalog_complete_and_has_math():
    assert set(ITEMS) == set(REQUIRED_KEYS)
    assert len(ITEMS) >= 30
    for key, item in ITEMS.items():
        assert item.eq.strip().startswith("$$") and item.eq.strip().endswith("$$"), key
        assert r"\(" in item.inline and r"\)" in item.inline, key
        assert item.blurb and item.what and item.scattering and item.slider and item.limits


def test_explain_block_is_static_panel():
    import panel as pn

    block = explain_block("sigma")
    assert isinstance(block, pn.Column)
    # Accordion starts collapsed
    acc = [c for c in block.objects if isinstance(c, pn.Accordion)][0]
    assert list(acc.active) == []


def test_deep_pane_has_display_and_inline_latex():
    import panel as pn

    pane = deep_pane(ITEMS["sigma"])
    tex = [o for o in pane.objects if isinstance(o, pn.pane.LaTeX)]
    assert len(tex) == 2
    assert tex[0].object.strip().startswith("$$")
    assert r"\(" in tex[1].object


def test_make_app_still_builds():
    import panel as pn
    from app.main import make_app

    app = make_app()
    n_acc = sum(1 for obj in app.select(pn.Accordion))
    assert n_acc == len(ITEMS)
    names = [getattr(obj, "name", "") for obj in app.select()]
    assert "diagnostic-sweep" in names
    tabs = list(app.select(pn.Tabs))
    assert tabs
    titles = " ".join(str(getattr(t, "objects", t)) for t in tabs)
    assert "diagnostic-sweep" in names or "Diagnostic" in titles
    assert any(getattr(b, "name", "") == "Run sweep" for b in app.select(pn.widgets.Button))
    n_tex_top = sum(1 for obj in app.select(pn.pane.LaTeX))
    assert n_tex_top >= 1  # header notation; accordion LaTeX is inside collapsed cards


def test_footer_marks_not_cardsharpener():
    from app.main import FOOTER, in_pyodide, make_app

    assert "not a Cardsharpener product" in FOOTER
    assert in_pyodide() is False
    app = make_app()
    md = " ".join(
        getattr(obj, "object", "") or ""
        for obj in app.select()
        if getattr(obj, "object", None) and isinstance(getattr(obj, "object"), str)
    )
    assert "not a Cardsharpener product" in md


def test_toggle_hides_explanations_without_recompute():
    import panel as pn
    from app.main import _surface_cached, make_app

    app = make_app()
    before = _surface_cached.cache_info()
    boxes = [b for b in app.select(pn.widgets.Checkbox) if b.name == "Show explanations"]
    assert len(boxes) == 1
    toggle = boxes[0]
    blocks = [c for c in app.select(pn.Column) if "explain-ui" in (c.css_classes or [])]
    assert len(blocks) == len(ITEMS)
    assert all(b.visible for b in blocks)

    toggle.value = False
    after_off = _surface_cached.cache_info()
    assert all(not b.visible for b in blocks)
    assert after_off.misses == before.misses
    assert after_off.currsize == before.currsize

    toggle.value = True
    after_on = _surface_cached.cache_info()
    assert all(b.visible for b in blocks)
    assert after_on.misses == before.misses
