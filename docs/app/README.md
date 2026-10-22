# Live surface-scattering app (illustrative)

Two-panel Panel toy: a random surface you can edit, and a simulated detector looking at it. **Not experimental data** and **not your sample**.

## Launch

From `xray-scattering/` with the venv on:

```bash
python -m app
```

or

```bash
panel serve app/main.py --port 5009 --address 0.0.0.0
```

Then open http://127.0.0.1:5009 . First paint is typically well under a second at the default grid N=96.

## On-page explanations

A **Show explanations** checkbox at the top of the page (on by default) hides every blurb and **More about …** accordion without recomputing the surface; uncheck it for a clean controls-and-plots view.

Every control and plot has a **one-line blurb** (when explanations are shown) and a collapsed **More about …** accordion. Opening an accordion shows: what the quantity is, a defining equation, how it enters the scattering formula, what to watch when you move the slider, and the toy’s limits.

Equations are `pn.pane.LaTeX` with **MathJax** (Bokeh’s bundled `bokeh-mathjax`). `python -m app` serves with `inline=True` so the MathJax JS is not fetched from a CDN. Display math uses `$$...$$`; inline uses `\(...\)`. Opening an accordion does **not** recompute the surface — explanation panes are static.

The header also shows a notation line (inline σ, ξ, h, C(R)) plus the Born S<sub>diff</sub> display equation (PRB (2.28b), constants dropped).

The page footer states this is an **illustrative masters-project toy, not a Cardsharpener product**.

## Hosting

A static **Pyodide** build runs the same UI in the browser (no Python server). Intended public host: `https://xray.cardsharpener.com`, as a **separate** Cloudflare assets project (`xray-scattering`), not the cardsharpner Worker.

```bash
bash web/build.sh          # or: python -m app.build_static
cd web/dist && python -m http.server 8010
```

Packages pulled in-browser: numpy, scipy, matplotlib, bokeh, panel (plus Pyodide from jsDelivr). Grid N is capped at 96 in WASM. Cold load is ~45–50 MB download / ~120 MB unpacked and took **~99 s** to plots in Chrome here; slider updates ~2 s versus ~0.3 s native. Full deploy steps (wrangler, custom domain, DNS, WASM headers): [`web/README.md`](../../web/README.md). **Do not** attach this app to the production site Worker, Stripe, or KV.

## What you are looking at

**Left — truth.** FFT-filtered Gaussian field with a chosen isotropic C(R). Families:

- self-affine: C(R)=σ² exp[−(R/ξ)^{2h}]
- Gaussian: the h=1 member of that family
- capillary: log-shaped C, then scaled so C(0)=σ²

Optional islands/pits add a two-level disk layer (toy exclusion, not Wu (13)).

Plots: heatmap of z(x,y), theory C(R) vs C estimated from the map, and g(R)=2σ²−2C.

**Right — toy lab.** Born S<sub>diff</sub> from chapter 5 (constants dropped), optional DWBA |T(α)T(β)|², resolution blur, coherence window e<sup>−R/ξ_coh</sup> on C, footprint 1/sinα, pixel rebin, mixed Poisson noise.

Scans: rocking (transverse), specular (Debye–Waller envelope), 2D q<sub>∥</sub>–q<sub>z</sub> map.

The fit table is a least-squares (σ, ξ, h) to the 1D q<sub>∥</sub> line shape. On a **specular** scan there is no q<sub>∥</sub> information, so the fit uses an auxiliary noiseless rocking kernel at the same surface (still a toy, not extra “data”).

The lower-right map is a **random-phase rebuild** from the fitted C(R). Scattering measures intensity, not phase: this is **not** the original surface.

Session JSON in the box is for reproducing sliders; it is not saved to disk unless you copy it.

## Diagnostic sweep

A **Diagnostic sweep** tab next to **Live view** keeps the two-column layout usable. It **locks** the current left-hand surface (σ, ξ, h, family, N, L, seed, islands) and walks **one measurement knob at a time**. Click **Run sweep** — sliders do not start it, and the main view is not recomputed. Results stay cached until you run again.

Swept knobs (log or linear, ~6–12 points): coherence ξ_coh, resolution Δq, noise mix, incidence α, scan type (discrete), and rocking range. `qz_min`/`qz_max` are **derived**, not live controls. N stays at the current grid (capped at 96 in WASM).

Each point reuses the live forward model + fit. Scores (illustrative, **not** z(x,y) RMSE):

- |σ̂−σ|/σ, |ξ̂−ξ|/ξ, |ĥ−h|
- RMS of log C_fit vs C_true (RMS of C is recorded as a sanity check)

The **knee** is the first point from the good end where |Δξ|/ξ exceeds a threshold (default 10%). A summary names which swept quantity is closest to, or past, that knee at the **current** settings — the limiter for this surface.

**Specular** has no q∥: ξ and h are **unidentified**. The live table’s auxiliary noiseless rocking kernel is labelled a **cheat**, not a recovery.

Headless (no UI), from `xray-scattering/` with `PYTHONPATH=src`:

```bash
python -m xray_scattering.sim.sweep --n-grid 8 --axes xi_coh,dq,noise,alpha_deg,scan,rock_range_deg
python -m xray_scattering.sim.sweep --axes xi_coh --json   # coherence only, JSON
```

In the app, open the section, leave axes at `xi_coh` (or pick more), set knee / points, click **Run sweep**. WASM: one axis × 6 points; a full grid is slow.

The **Show explanations** toggle still hides every blurb and More-about accordion, including the sweep copy.

## Parameter guide (defaults)

| Control | Default | Role |
| --- | --- | --- |
| σ | 5 Å | rms height; C(0)=σ² |
| ξ | 40 Å | lateral cutoff of C |
| h | 0.5 | Hurst; small h is jagged |
| N, L | 96, 384 Å | grid; dx=L/N. Larger N is slower |
| λ, α | 1.54 Å, 0.55° | kinematics |
| ξ_coh | 600 Å | damps large-R correlations |
| Δq, pixel | 0.002, 0 | resolution FWHM and bin width |
| noise mix | 0 | 0 is noiseless; 1 is Poisson-dominated |

## Known limits

- Recoverable ξ is bounded by the box L and the pixel dx. ξ ≳ L/3 or ξ ≲ few dx will not fit well.
- Hankel integrals use a finite R<sub>max</sub> and a cosine taper.
- Island structure factor is a dart-thrown disk toy.
- DWBA uses vacuum q and Pyrex-like n from PRB Sec. V as an optical illustration; in-medium q<sub>z</sub>' is omitted.
- Intensities omit (Nb)², area, and flux — shapes only.
- The rebuilt map is statistically equivalent (approximately), never a phase retrieval of z(x,y).
