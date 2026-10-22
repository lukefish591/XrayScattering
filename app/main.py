#!/usr/bin/env python3
"""Live illustrative surface + toy lab measurement (Panel).

Not experimental data. Scattering measures intensity, not phase.
"""

from __future__ import annotations

import json
import sys
import time
from functools import lru_cache
from pathlib import Path

_HERE = Path(__file__).resolve().parent
for _extra in (_HERE, _HERE / "src", _HERE.parent / "src"):
    _s = str(_extra)
    if _s not in sys.path:
        sys.path.insert(0, _s)

import matplotlib

try:
    matplotlib.use("Agg")
except Exception:
    pass
import matplotlib.pyplot as plt
import numpy as np
import panel as pn

try:
    from app.explain import explain_block, with_explain
except ImportError:  # panel serve app/main.py
    from explain import explain_block, with_explain
from xray_scattering.sim.analysis import analyse, fit_line_from_measurement
from xray_scattering.sim.correlations import g_of_C
from xray_scattering.sim.forward import simulate_measurement
from xray_scattering.sim.params import MeasureParams, SurfaceParams, params_to_json
from xray_scattering.sim.surface import generate_surface
from xray_scattering.sim.sweep import AXES, plot_report, run_diagnostic_sweep

# MathJax must be loaded in the first extension() call. Bokeh ships
# bokeh-mathjax.min.js; pn.serve(..., inline=True) avoids a CDN.
pn.extension("mathjax", design="native")

BANNER = (
    "ILLUSTRATIVE TOY — not your sample, not measured data. "
    "The rebuilt map is a random-phase draw from the fitted C(R); it is not the original surface."
)
FOOTER = (
    "Illustrative masters-project toy — **not a Cardsharpener product**, "
    "not measured data, and not your sample."
)


def in_pyodide() -> bool:
    return sys.platform == "emscripten" or "pyodide" in sys.modules


def _sliders():
    fam = pn.widgets.Select(
        name="C(R) family",
        options=["self-affine", "gaussian", "capillary"],
        value="self-affine",
    )
    sigma = pn.widgets.FloatSlider(name="σ (Å)", start=1.0, end=12.0, step=0.25, value=5.0)
    xi = pn.widgets.FloatSlider(name="ξ (Å)", start=10.0, end=120.0, step=2.0, value=40.0)
    h = pn.widgets.FloatSlider(name="Hurst h", start=0.2, end=0.9, step=0.05, value=0.5)
    n_end = 96 if in_pyodide() else 192
    N = pn.widgets.IntSlider(name="N (grid)", start=48, end=n_end, step=16, value=96)
    L = pn.widgets.FloatSlider(name="L (Å)", start=192.0, end=768.0, step=32.0, value=384.0)
    seed = pn.widgets.IntInput(name="seed", value=1, start=0, end=10_000)
    reroll = pn.widgets.Button(name="Re-roll seed", button_type="primary")
    islands = pn.widgets.Checkbox(name="Add islands/pits (toy)", value=False)
    phi = pn.widgets.FloatSlider(name="φ coverage", start=0.05, end=0.45, step=0.05, value=0.25)
    delta = pn.widgets.FloatSlider(name="Δ height (Å)", start=4.0, end=24.0, step=1.0, value=12.0)
    iR = pn.widgets.FloatSlider(name="island R (Å)", start=16.0, end=80.0, step=2.0, value=36.0)
    idd = pn.widgets.FloatSlider(name="min spacing d (Å)", start=60.0, end=200.0, step=5.0, value=100.0)

    wav = pn.widgets.FloatSlider(name="λ (Å)", start=0.7, end=2.0, step=0.02, value=1.54)
    alpha = pn.widgets.FloatSlider(name="α (deg)", start=0.15, end=1.2, step=0.05, value=0.55)
    scan = pn.widgets.Select(name="scan", options=["rocking", "specular", "qmap"], value="rocking")
    npts = pn.widgets.IntSlider(name="detector points", start=41, end=121, step=8, value=81)
    rock = pn.widgets.FloatSlider(name="rock range (deg)", start=0.15, end=0.8, step=0.05, value=0.45)
    dq = pn.widgets.FloatSlider(name="resolution Δq (Å⁻¹)", start=0.0, end=0.02, step=0.001, value=0.002)
    xic = pn.widgets.FloatSlider(name="ξ_coh (Å)", start=80.0, end=2000.0, step=20.0, value=600.0)
    foot = pn.widgets.Checkbox(name="footprint 1/sinα", value=True)
    dwba = pn.widgets.Checkbox(name="DWBA |T|² wings (toy)", value=False)
    noise = pn.widgets.FloatSlider(name="noise mix", start=0.0, end=1.0, step=0.05, value=0.0)
    pix = pn.widgets.FloatSlider(name="pixel Δq (Å⁻¹)", start=0.0, end=0.02, step=0.001, value=0.0)
    export = pn.widgets.Button(name="Copy params JSON")
    json_box = pn.widgets.TextAreaInput(name="session params (JSON)", height=120, disabled=True)
    status = pn.pane.Markdown("", sizing_mode="stretch_width")
    return locals()


@lru_cache(maxsize=16)
def _surface_cached(key: tuple):
    p = SurfaceParams(
        family=key[0],
        sigma=key[1],
        xi=key[2],
        h=key[3],
        N=key[7],
        L=key[8],
        seed=key[9],
        islands=key[10],
        phi=key[11],
        delta=key[12],
        island_R=key[13],
        island_d=key[14],
    )
    return generate_surface(p)


def _fig():
    fig, ax = plt.subplots(figsize=(4.4, 3.4))
    return fig, ax


def _heatmap(z, x, title, cmap="cividis"):
    fig, ax = plt.subplots(figsize=(4.6, 3.8))
    step = max(1, z.shape[0] // 128)
    zz = z[::step, ::step]
    extent = [float(x[0]), float(x[-1]), float(x[0]), float(x[-1])]
    im = ax.imshow(zz, origin="lower", cmap=cmap, extent=extent, aspect="equal")
    ax.set_xlabel("x (Å)")
    ax.set_ylabel("y (Å)")
    ax.set_title(title, fontsize=9)
    ax.grid(False)
    fig.colorbar(im, ax=ax, fraction=0.046, label="z (Å)")
    fig.tight_layout()
    return fig


def make_app():
    w = _sliders()

    left_map = pn.pane.Matplotlib(dpi=100, tight=True, sizing_mode="stretch_width")
    left_c = pn.pane.Matplotlib(dpi=100, tight=True, sizing_mode="stretch_width")
    right_det = pn.pane.Matplotlib(dpi=100, tight=True, sizing_mode="stretch_width")
    right_c = pn.pane.Matplotlib(dpi=100, tight=True, sizing_mode="stretch_width")
    right_map = pn.pane.Matplotlib(dpi=100, tight=True, sizing_mode="stretch_width")
    table = pn.pane.HTML("<p>fit vs true</p>")

    def surface_params() -> SurfaceParams:
        return SurfaceParams(
            family=w["fam"].value,
            sigma=float(w["sigma"].value),
            xi=float(w["xi"].value),
            h=float(w["h"].value),
            N=int(w["N"].value),
            L=float(w["L"].value),
            seed=int(w["seed"].value),
            islands=bool(w["islands"].value),
            phi=float(w["phi"].value),
            delta=float(w["delta"].value),
            island_R=float(w["iR"].value),
            island_d=float(w["idd"].value),
        )

    def measure_params() -> MeasureParams:
        return MeasureParams(
            wavelength=float(w["wav"].value),
            alpha_deg=float(w["alpha"].value),
            scan=str(w["scan"].value),
            n_pts=int(w["npts"].value),
            rock_range_deg=float(w["rock"].value),
            dq=float(w["dq"].value),
            xi_coh=float(w["xic"].value),
            footprint=bool(w["foot"].value),
            use_dwba=bool(w["dwba"].value),
            noise=float(w["noise"].value),
            pixel_dq=float(w["pix"].value),
            seed=int(w["seed"].value),
        )

    def refresh(_=None):
        t0 = time.perf_counter()
        sp = surface_params()
        mp = measure_params()
        surf = _surface_cached(sp.cache_key())
        det = simulate_measurement(surf, mp)
        line = fit_line_from_measurement(surf, mp)
        an = analyse(surf, line.qpar, line.intensity, line.qz_ref)

        x = surf.x
        left_map.object = _heatmap(surf.z, x, "True z(x,y) — illustrative")

        fig, ax = plt.subplots(1, 3, figsize=(8.8, 3.0))
        g = g_of_C(an.C_true, sp.sigma)
        ax[0].plot(an.R, an.C_true, "k", label="C(R) theory")
        ax[0].plot(an.R, an.C_emp, "C0--", label="C from map")
        ax[0].set_xlabel("R (Å)")
        ax[0].set_ylabel("C(R) (Å²)")
        ax[0].legend(fontsize=7)
        ax[1].plot(an.R, g, "k", label="g(R)=2σ²−2C")
        ax[1].set_xlabel("R (Å)")
        ax[1].set_ylabel("g(R) (Å²)")
        ax[1].legend(fontsize=7)
        ax[2].semilogy(an.q, an.P_true, "k", label="true PSD")
        ax[2].set_xlabel(r"$q_\parallel$ (Å$^{-1}$)")
        ax[2].set_ylabel("P (arb.)")
        ax[2].legend(fontsize=7)
        fig.suptitle("True C(R), g(R), PSD", fontsize=9)
        fig.tight_layout()
        left_c.object = fig

        fig, ax = plt.subplots(figsize=(5.2, 3.6))
        if det.scan == "qmap":
            im = ax.imshow(
                det.intensity,
                origin="lower",
                aspect="auto",
                extent=[det.x[0], det.x[-1], det.y[0], det.y[-1]],
                cmap="magma",
            )
            ax.set_xlabel(det.xlabel)
            ax.set_ylabel(det.ylabel)
            fig.colorbar(im, ax=ax, fraction=0.046, label="arb.")
        else:
            ax.plot(det.x, det.intensity, "k")
            ax.set_xlabel(det.xlabel)
            ax.set_ylabel(det.ylabel)
            if det.scan != "specular":
                ax.set_yscale("log")
        ax.set_title(det.title, fontsize=9)
        fig.tight_layout()
        right_det.object = fig

        fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.2))
        ax[0].plot(an.R, an.C_true, "k", lw=2, label="true C")
        ax[0].plot(an.R, an.C_fit, "C3", label="fit C")
        if np.isfinite(an.C_inv).any():
            ax[0].plot(an.R, an.C_inv, "C0:", lw=1, label="Hankel invert")
        ax[0].set_xlabel("R (Å)")
        ax[0].set_ylabel("C(R) (Å²)")
        ax[0].legend(fontsize=7)
        ax[1].semilogy(an.q, an.P_true, "k", label="true PSD")
        ax[1].semilogy(an.q, an.P_fit, "C3--", label="fit PSD")
        ax[1].set_xlabel(r"$q_\parallel$ (Å$^{-1}$)")
        ax[1].set_ylabel("P (arb.)")
        ax[1].legend(fontsize=7)
        fig.suptitle("Fit vs true (shapes only)", fontsize=9)
        fig.tight_layout()
        right_c.object = fig

        right_map.object = _heatmap(
            an.z_rebuild,
            x,
            "NOT the original — random-phase rebuild from fitted C(R)",
            cmap="cividis",
        )

        def row(name, true, fit_pair):
            val, err = fit_pair
            err_s = "—" if not np.isfinite(err) else f"{err:.2f}"
            return f"<tr><td>{name}</td><td>{true:.3g}</td><td>{val:.3g}</td><td>{err_s}</td></tr>"

        html = (
            "<table border='1' cellpadding='4'>"
            "<tr><th>param</th><th>true</th><th>fit</th><th>1σ (curve_fit)</th></tr>"
            + row("σ (Å)", sp.sigma, an.fit["sigma"])
            + row("ξ (Å)", sp.xi, an.fit["xi"])
            + row("h", sp.h, an.fit["h"])
            + "</table>"
            f"<p style='font-size:12px'>{an.note}</p>"
        )
        if line.unidentified_xi_h:
            html += (
                "<p style='font-size:12px'><b>Specular has no q∥ — ξ and h are unidentified.</b> "
                "The auxiliary noiseless rocking kernel is a <i>cheat</i>, not a recovery.</p>"
            )
        table.object = html
        payload = params_to_json(sp, mp)
        w["json_box"].value = json.dumps(payload, indent=2)
        dt = time.perf_counter() - t0
        w["status"].object = f"**Update** {dt:.2f}s · N={sp.N} · scan={mp.scan} · illustrative"

    def reroll(_):
        w["seed"].value = int(w["seed"].value) + 1

    w["reroll"].on_click(reroll)

    debounce_handle = {"h": None}

    def schedule_refresh(*_a, **_k):
        if in_pyodide():
            refresh()
            return
        try:
            from tornado.ioloop import IOLoop

            loop = IOLoop.current()
        except Exception:
            refresh()
            return
        if debounce_handle["h"] is not None:
            try:
                loop.remove_timeout(debounce_handle["h"])
            except Exception:
                pass
        debounce_handle["h"] = loop.call_later(0.18, refresh)

    watched = [
        w["fam"],
        w["sigma"],
        w["xi"],
        w["h"],
        w["N"],
        w["L"],
        w["seed"],
        w["islands"],
        w["phi"],
        w["delta"],
        w["iR"],
        w["idd"],
        w["wav"],
        w["alpha"],
        w["scan"],
        w["npts"],
        w["rock"],
        w["dq"],
        w["xic"],
        w["foot"],
        w["dwba"],
        w["noise"],
        w["pix"],
    ]
    for widget in watched:
        widget.param.watch(lambda *a, **k: schedule_refresh(), "value")

    def copy_json(_):
        w["status"].object = "Params JSON is in the box below (session only)."

    w["export"].on_click(copy_json)

    refresh()

    # Diagnostic sweep: locked surface, Run only (not on slider ticks).
    sweep_cache: dict = {"report": None, "fig": None}
    hold_ideal = pn.widgets.Checkbox(
        name="Hold other knobs at ideal (noiseless, Δq=0, ξ_coh=2000 Å, rocking, no footprint)",
        value=True,
    )
    knee_w = pn.widgets.FloatSlider(
        name="knee |Δξ|/ξ", start=0.05, end=0.30, step=0.01, value=0.10
    )
    ngrid_w = pn.widgets.IntSlider(
        name="points per axis",
        start=6,
        end=12,
        step=1,
        value=6 if in_pyodide() else 8,
    )
    axes_w = pn.widgets.MultiChoice(
        name="axes to sweep",
        options=list(AXES),
        value=["xi_coh"],
        max_items=len(AXES),
    )
    run_sweep_btn = pn.widgets.Button(
        name="Run sweep", button_type="primary", width=160
    )
    sweep_status = pn.pane.Markdown(
        "Diagnostic sweep is cached until you click **Run sweep**. "
        "It does not recompute the two-column view. Illustrative.",
        sizing_mode="stretch_width",
        name="sweep-status",
    )
    sweep_summary = pn.pane.Markdown("", sizing_mode="stretch_width", name="sweep-limiter")
    sweep_plot = pn.pane.Matplotlib(
        dpi=90, tight=True, sizing_mode="stretch_width", name="sweep-plots"
    )
    qrange_note = pn.pane.Markdown(
        "qz_min / qz_max are **derived** (not a live control). "
        "`rock_range_deg` is the optional q-window sweep for rocking. "
        "N stays at the current grid (capped at 96 in WASM). "
        "Scores are |σ̂−σ|/σ, |ξ̂−ξ|/ξ, |ĥ−h| and RMS log C(R) — **not** z RMSE. "
        "Specular points flag ξ/h as unidentified; the auxiliary rocking kernel is a cheat.",
        sizing_mode="stretch_width",
    )

    def _run_sweep(_=None):
        t0 = time.perf_counter()
        sp = surface_params()
        if in_pyodide():
            sp = SurfaceParams(**{**sp.__dict__, "N": min(int(sp.N), 96)})
        surf = _surface_cached(sp.cache_key())
        mp = measure_params()
        axes = tuple(axes_w.value) or ("xi_coh",)
        n_jobs_est = max(1, int(ngrid_w.value)) * len(axes)
        sweep_status.object = (
            f"Running diagnostic sweep on locked surface "
            f"(N={sp.N}, ~{n_jobs_est} forward+fit calls)…"
        )
        last_push = {"i": -1}

        def progress(i, n, axis, val):
            if i == last_push["i"]:
                return
            last_push["i"] = i
            sweep_status.object = (
                f"Sweeping **{axis}** = `{val}` ({i}/{n}) — illustrative, not z RMSE"
            )

        try:
            report = run_diagnostic_sweep(
                surf,
                measure=mp,
                hold_ideal=bool(hold_ideal.value),
                knee_thresh=float(knee_w.value),
                n_grid=int(ngrid_w.value),
                axes=axes,
                progress=progress,
            )
        except Exception as exc:
            sweep_status.object = f"Sweep failed: {exc}"
            return
        fig = plot_report(report)
        sweep_cache["report"] = report
        sweep_cache["fig"] = fig
        sweep_plot.object = fig
        sweep_summary.object = f"**{report.summary}**"
        dt = time.perf_counter() - t0
        sweep_status.object = (
            f"Sweep cached ({dt:.1f}s, {len(axes)} axis/axes). "
            "Main view was not recomputed. Click Run sweep to refresh. Illustrative."
        )

    run_sweep_btn.on_click(_run_sweep)

    explain_panes: list = []

    def _explain(key: str):
        block = explain_block(key)
        explain_panes.append(block)
        return block

    def _with(widget, key: str):
        return with_explain(widget, key, sink=explain_panes)

    show_ex = pn.widgets.Checkbox(name="Show explanations", value=True)

    left = pn.Column(
        pn.pane.Markdown("### Surface (truth)"),
        _with(w["fam"], "family"),
        _with(w["sigma"], "sigma"),
        _with(w["xi"], "xi"),
        _with(w["h"], "h"),
        _with(w["N"], "N"),
        _with(w["L"], "L"),
        _with(pn.Row(w["seed"], w["reroll"]), "seed"),
        _with(w["islands"], "islands"),
        _with(w["phi"], "phi"),
        _with(w["delta"], "delta"),
        _with(w["iR"], "island_R"),
        _with(w["idd"], "island_d"),
        left_map,
        _explain("heatmap"),
        left_c,
        _explain("CR"),
        _explain("gR"),
        _explain("psd"),
        sizing_mode="stretch_width",
    )
    right = pn.Column(
        pn.pane.Markdown("### Toy lab measurement"),
        _with(w["wav"], "wavelength"),
        _with(w["alpha"], "alpha"),
        _with(w["scan"], "scan"),
        _with(w["npts"], "npts"),
        _with(w["rock"], "rock"),
        _with(w["dq"], "dq"),
        _with(w["xic"], "xic"),
        _with(w["foot"], "foot"),
        _with(w["dwba"], "dwba"),
        _with(w["noise"], "noise"),
        _with(w["pix"], "pix"),
        right_det,
        _explain("detector"),
        right_c,
        _explain("fit_curves"),
        right_map,
        _explain("rebuild"),
        table,
        _explain("fit_table"),
        w["export"],
        w["json_box"],
        _explain("json"),
        sizing_mode="stretch_width",
    )
    notation_inline = pn.pane.LaTeX(
        r"Notation (inline): \(\sigma\) rms height, \(\xi\) cutoff, "
        r"\(h\) Hurst, \(C(R)=\langle z(R)z(0)\rangle\).",
        renderer="mathjax",
        sizing_mode="stretch_width",
        styles={"font-size": "16px"},
    )
    notation_display = pn.pane.LaTeX(
        r"$$S_{\mathrm{diff}}\propto"
        r"\frac{e^{-q_z^{2}\sigma^{2}}}{q_z^{2}}"
        r"\int_0^{\infty} R\,dR\,J_0(q_\parallel R)\bigl(e^{q_z^{2}C}-1\bigr)$$",
        renderer="mathjax",
        sizing_mode="stretch_width",
        styles={"font-size": "16px"},
    )
    explain_panes.extend([notation_inline, notation_display])

    def _set_explain_visible(*_a, **_k):
        vis = bool(show_ex.value)
        for pane in explain_panes:
            pane.visible = vis

    show_ex.param.watch(_set_explain_visible, "value")

    explain_panes.append(qrange_note)
    diag_body = pn.Column(
        _explain("sweep"),
        qrange_note,
        pn.Row(run_sweep_btn, hold_ideal),
        pn.Row(knee_w, ngrid_w),
        axes_w,
        sweep_status,
        sweep_summary,
        sweep_plot,
        sizing_mode="stretch_width",
        name="diagnostic-sweep",
    )

    wasm_note = ""
    if in_pyodide():
        wasm_note = (
            "\n\nRunning in **WebAssembly** in this browser. Grid size N is capped at 96 "
            "and updates are slower than the local Panel server (python -m app). "
            "A full diagnostic sweep is slow in WASM — run one axis (coherence) with 6 points."
        )
    return pn.Column(
        pn.pane.Markdown(f"# Live surface scattering (illustrative)\n\n{BANNER}{wasm_note}"),
        show_ex,
        w["status"],
        notation_inline,
        notation_display,
        pn.Tabs(
            ("Live view", pn.Row(left, right, sizing_mode="stretch_width")),
            ("Diagnostic sweep", diag_body),
            sizing_mode="stretch_width",
        ),
        pn.pane.Markdown(f"---\n{FOOTER}"),
        sizing_mode="stretch_width",
    )


def serve(port: int = 5009, show: bool = False, **kwargs):
    app = make_app()
    pn.serve(
        app,
        port=port,
        show=show,
        title="X-ray scattering toy",
        address="0.0.0.0",
        inline=True,
        **kwargs,
    )


if __name__ == "__main__":
    serve()
