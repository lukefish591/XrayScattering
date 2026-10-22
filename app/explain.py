"""Static blurbs and MathJax deep dives for the live toy.

Content is built once. Changing sliders must not rebuild these panes.
Equations use pn.pane.LaTeX with renderer='mathjax'. Display: $$...$$.
Inline: \\( ... \\). Grounded in docs/maths ch. 2–8 and the app's actual toys.
"""

from __future__ import annotations

from dataclasses import dataclass

import panel as pn

ACCORDION_CSS = """
.bk-Accordion {
  margin-top: 0 !important;
}
.bk-Accordion .bk-card-header {
  padding: 4px 8px !important;
  font-size: 12px !important;
}
.explain-blurb {
  font-size: 11.5px;
  color: #3a3a3a;
  line-height: 1.4;
  margin: 0 0 2px 0;
}
.explain-sec {
  font-size: 13px;
  line-height: 1.45;
  margin: 0.4em 0 0.2em 0;
}
"""


@dataclass(frozen=True)
class Item:
    title: str
    blurb: str
    what: str
    eq: str
    inline: str
    scattering: str
    slider: str
    limits: str


def _md(text: str) -> pn.pane.Markdown:
    return pn.pane.Markdown(
        text,
        disable_math=True,
        sizing_mode="stretch_width",
        styles={"font-size": "13px"},
    )


def _tex(src: str) -> pn.pane.LaTeX:
    return pn.pane.LaTeX(
        src,
        renderer="mathjax",
        sizing_mode="stretch_width",
        styles={"font-size": "15px"},
    )


def deep_pane(item: Item) -> pn.Column:
    return pn.Column(
        _md(f"**What it is.** {item.what}"),
        _md("**Defining equation**"),
        _tex(item.eq),
        _tex(item.inline),
        _md(f"**In the scattering formula.** {item.scattering}"),
        _md(f"**When you move the control.** {item.slider}"),
        _md(f"**Limits in this toy.** {item.limits}"),
        sizing_mode="stretch_width",
        margin=(4, 8, 8, 8),
    )


def explain_block(key: str) -> pn.Column:
    item = ITEMS[key]
    acc = pn.Accordion(
        (item.title, deep_pane(item)),
        toggle=True,
        active=[],
        sizing_mode="stretch_width",
        stylesheets=[ACCORDION_CSS],
    )
    blurb = pn.pane.HTML(
        f"<p class='explain-blurb'>{item.blurb}</p>",
        sizing_mode="stretch_width",
        margin=(2, 0, 0, 0),
        stylesheets=[ACCORDION_CSS],
    )
    return pn.Column(
        blurb,
        acc,
        margin=(0, 0, 8, 0),
        sizing_mode="stretch_width",
        css_classes=["explain-ui"],
        name=f"explain-{key}",
    )


def with_explain(widget, key: str, sink: list | None = None) -> pn.Column:
    block = explain_block(key)
    if sink is not None:
        sink.append(block)
    return pn.Column(widget, block, sizing_mode="stretch_width")


ITEMS: dict[str, Item] = {
    "family": Item(
        title="More about C(R) family",
        blurb="Which isotropic correlation shape the random field is built from. Self-affine is PRB (2.25); Gaussian is that family at h=1; capillary is a log g(R) then rescaled to your σ.",
        what="A stationary isotropic random field is specified by one function C(R)=⟨z(R)z(0)⟩, not by a photograph of z. Chapter 4. Three families are offered; islands are an extra two-level layer, not a fourth C(R).",
        eq=r"$$C_{\mathrm{sa}}(R)=\sigma^{2}\exp\bigl[-(R/\xi)^{2h}\bigr]$$",
        inline=r"Gaussian is that formula with \(h=1\). Capillary starts from a log \(g(R)\) (ch. 6) and is then scaled so \(C(0)=\sigma^{2}\).",
        scattering="Born S_diff (ch. 5, PRB (2.28b)) is the Hankel transform of e^{q_z² C}−1. Changing family changes that kernel, hence the rocking line shape. Specular Debye–Waller only sees σ, not the family, if a cutoff exists.",
        slider="Self-affine: h and ξ both matter. Gaussian: the h slider is ignored (forced to 1). Capillary: ξ/h are unused; IR cutoff ξ_ir=80 Å and B=8 are internal defaults, then C is scaled to the σ slider.",
        limits="Not a materials library. Capillary here is not a measured liquid (no k_B T/γ). PRB Sec. II.D log g without IR cutoff has no δ-function specular; this toy always scales C(0) to σ² so a cutoff is implied.",
    ),
    "sigma": Item(
        title="More about σ",
        blurb="Root-mean-square height of the zero-mean surface. Sets C(0)=σ² and the Debye–Waller factor e^{−q_z² σ²}.",
        what="σ = √⟨z²⟩ after subtracting the mean plane (ch. 3). It is a vertical scale, not a lateral one. PRB Sec. V quotes σ=7.6 Å for their Pyrex — illustration, not your sample.",
        eq=r"$$C(0)=\sigma^{2},\qquad S_{\mathrm{spec}}\propto e^{-q_z^{2}\sigma^{2}}/q_z^{2}$$",
        inline=r"The characteristic function of a Gaussian height difference is \(\langle e^{-iq_z X}\rangle=e^{-q_z^{2}g/2}\) with \(g(0)=0\) and \(g(\infty)=2\sigma^{2}\) if C dies (ch. 3, 5).",
        scattering="Larger σ kills specular faster as q_z grows and, through e^{q_z² C}−1, fattens diffuse. At small q_z σ the diffuse kernel linearises to C itself (PRB (4.43)).",
        slider="The heatmap colour range grows; C(R) at R=0 jumps as σ²; g(R) saturates near 2σ²; specular drops faster; rocking overall scale is normalised in the toy so look at shape and at the fit table.",
        limits="The generator rescales the FFT field to this σ after drawing, so the map always matches the slider even on a small grid. Islands add extra height contrast on top, then the map is re-centred (mean removed) but not re-forced to σ.",
    ),
    "xi": Item(
        title="More about ξ",
        blurb="Lateral cutoff of C(R): beyond ξ, heights forget each other. Sets the width of the diffuse peak in q∥ ~ 2π/ξ.",
        what="PRB (2.9)/(2.25) introduced ξ so that an ideal self-affine g(R)∝R^{2h} (which diverges) saturates. Physically: the hill size above which the surface looks like a finite-amplitude field, not an unbounded walk.",
        eq=r"$$C(R)=\sigma^{2}\exp\bigl[-(R/\xi)^{2h}\bigr]$$",
        inline=r"Large islands in real space are narrow features in \(q_\parallel\) (ch. 2 scaling / uncertainty).",
        scattering="S_diff(q∥) is the Hankel transform of e^{q_z² C(R)}−1. Stretching ξ squeezes that transform toward q∥=0: a sharper near-specular ridge.",
        slider="Heatmap features get broader. C(R) decays more slowly. PSD piles up at small q. The rocking curve peaks more tightly around q_x=0. Fit ξ is only trustworthy between a few dx and ~L/3.",
        limits="Unused for the capillary family (IR cutoff is internal). Coherence ξ_coh is a different length: it multiplies C by e^{−R/ξ_coh} in the detector model only, not on the true map.",
    ),
    "h": Item(
        title="More about Hurst h",
        blurb="Roughness exponent: small h is jagged (high-q PSD), h→1 is rolling hills. Surface fractal dimension D_s=3−h (PRB (2.8)).",
        what="Self-affine, not self-similar: z scales differently from x,y (ch. 5.3). Also called α in some roughness literature. PRB Pyrex illustration used h=0.2.",
        eq=r"$$g(R)=2\sigma^{2}\bigl(1-e^{-(R/\xi)^{2h}}\bigr),\qquad D_s=3-h$$",
        inline=r"At large \(q_z\) and no cutoff, PRB (2.22) has \(S(q_\parallel=0)\propto q_z^{-2-2/h}\); this toy always has a cutoff.",
        scattering="h tilts the short-R cusp of C, hence the high-q∥ tail of S_diff. Specular (only σ) does not see h.",
        slider="Lower h: heatmap looks noisier at small scales; C(R) drops faster just off R=0; PSD is flatter at large q. Gaussian family ignores this slider (h=1).",
        limits="Fit h is weakly constrained on a short rocking cut, especially with resolution blur. Bounds in the fitter are 0.15–0.95.",
    ),
    "N": Item(
        title="More about N (grid)",
        blurb="Number of samples along x and y. Pixel size dx=L/N. Larger N is slower and only needed when ξ is not many pixels.",
        what="The FFT generator (ch. 3–4) draws one period-L torus of N×N heights. That is a realisation of the random field, not the ensemble.",
        eq=r"$$\Delta x=L/N,\qquad q_{\max}\sim\pi/\Delta x$$",
        inline=r"Nyquist: features smaller than \(\sim 2\Delta x\) cannot live on the grid.",
        scattering="N does not enter S_diff, which is computed from the analytic C(R), not from the pixel map. N does affect the empirical C from the heatmap and the rebuilt map.",
        slider="Bigger N: finer heatmap, empirical C closer to theory, slower updates. Default 96 is the performance target (well under a second).",
        limits="The surface is periodic. Very large N (192) can exceed 1 s once measurement and fit run too.",
    ),
    "L": Item(
        title="More about L (box)",
        blurb="Physical side length of the map (Å). Together with N it sets dx. ξ should sit comfortably inside L.",
        what="One periodic patch of area L². Ergodicity (ch. 3): averaging over this patch stands in for the ensemble ⟨z(0)z(R)⟩.",
        eq=r"$$C(\mathbf{R})\approx\frac{1}{A}\int_A d^{2}R'\,z(\mathbf{R}')z(\mathbf{R}'+\mathbf{R})$$",
        inline=r"If \(\xi\gtrsim L/3\), that integral never sees C decay, and a fit cannot recover \(\xi\).",
        scattering="Born integrals use R_max=max(6ξ, 0.45 L) with a cosine taper — a numerical cutoff, not an extra physical ξ.",
        slider="Larger L at fixed N coarsens dx (loses high-q). Larger L at fixed dx needs larger N (not automatic here).",
        limits="Not a beam footprint. Footprint is a separate 1/sinα intensity weight on the detector curve.",
    ),
    "seed": Item(
        title="More about seed / re-roll",
        blurb="RNG seed for the Gaussian field (and islands). Same seed ⇒ identical map. Re-roll adds 1. Scattering of a Gaussian field should barely care which realisation you drew.",
        what="A random field has many realisations sharing C(R) (ch. 3). Intensity formulas use ⟨e^{−iq_z X}⟩, an ensemble object. One map is for looking; S_diff in this app is computed from the analytic C, not from that one map.",
        eq=r"$$z=\mathcal{F}^{-1}\!\bigl[\tilde\eta(\mathbf{q})\,\sqrt{P(\mathbf{q})}\bigr]$$",
        inline=r"Here \(\tilde\eta\) is white Gaussian noise; \(P\) is the FFT of \(C\) (Wiener–Khinchin, ch. 4). The field is then rescaled to \(\sigma\).",
        scattering="Changing seed changes the heatmap and empirical C (sampling noise) and the rebuilt map (different draw). The detector curve, being from analytic C, stays put unless islands are on (islands are placed with the same seed).",
        slider="Re-roll: watch the heatmap rearrange while C(R) theory overlay stays put. With islands, disk centres jump and the detector can move a little via the changed height field only through σ-like contrast — actually the detector still uses analytic C of the continuous family, not the island layer. So seed mainly teaches that one picture ≠ the statistic.",
        limits="The rebuilt map uses seed+3, on purpose, so it cannot coincide with the left map even if C matched perfectly.",
    ),
    "islands": Item(
        title="More about islands/pits (toy)",
        blurb="Optional two-level disks of height Δ on the Gaussian field. Not a Gaussian height-difference process — Physica A 1996 is the right language, not PRB’s e^{−q_z² g/2}.",
        what="Coverage φ of thickness Δ with in-plane form factor of a disk (ch. 7). This app darts disks with a minimum spacing, then optionally thins them toward φ. It does not implement Wu’s S(q) (13).",
        eq=r"$$R(q_z)=R_F\bigl[1-4\phi(1-\phi)\sin^{2}(q_z\Delta/2)\bigr]$$",
        inline=r"That is Physica (11) for the specular of a two-level film. Diffuse involves \(|f(q_\parallel)|^{2}\) and a structure factor \(S(q_\parallel)\) which this toy does not put on the detector.",
        scattering="The live detector still uses the continuous-family Born kernel. Islands are shown on the true map so you can see a two-level morphology; they are not yet wired into S_diff. Treat the right-hand column as the Gaussian/self-affine/capillary surface underneath.",
        slider="Tick the box: disks appear on the heatmap; rms is no longer exactly the σ slider. Detector and fit still follow the continuous C(R).",
        limits="Honest gap: island S is visual only. Do not read the fit table as a Physica (φ,Δ) analysis.",
    ),
    "phi": Item(
        title="More about coverage φ",
        blurb="Target area fraction of disks when islands are on. Specular two-level contrast is largest near φ=1/2 (Physica (11)).",
        what="φ is the probability a random surface point sits on an island (ch. 7.2). Bare fraction is 1−φ.",
        eq=r"$$\bigl\langle e^{-iq_z z}\bigr\rangle=(1-\phi)+\phi\,e^{-iq_z\Delta}$$",
        inline=r"The factor \(4\phi(1-\phi)\) in Physica (11) is a downward parabola peaked at \(\phi=1/2\).",
        scattering="Would modulate specular oscillations if the detector used the two-level formula. In this app it only changes how many disks are kept on the map.",
        slider="Higher φ: more (or larger total) disk area. Placement may miss the target when disks overlap the exclusion zone.",
        limits="Dart-throwing with a coverage trim, not a grand-canonical equilibrium.",
    ),
    "delta": Item(
        title="More about island height Δ",
        blurb="Step height of each disk (Å). Sets the q_z oscillation period 2π/Δ in a true two-level specular (Physica).",
        what="If every island has the same thickness, h_pdf(ζ)=δ(ζ−Δ) and h(q_z)=e^{−iq_z Δ} (Physica (9)). Pits are Δ<0; here Δ is a positive add-on.",
        eq=r"$$\Delta q_z = 2\pi/\Delta$$",
        inline=r"Kiessig-like fringes from a single step: period \(\Delta q_z=2\pi/\Delta\), not a multilayer stack (ch. 7).",
        scattering="Would appear in |⟨e^{−iq_z z}⟩|². Not in the current detector kernel.",
        slider="Taller disks: stronger contrast on the heatmap. Mean is subtracted after adding disks.",
        limits="No size distribution of Δ; one value only.",
    ),
    "island_R": Item(
        title="More about island radius",
        blurb="Disk radius (Å). A disk form factor is 2J_1(q∥ R)/(q∥ R); large R ⇒ narrow peak in q∥ (ch. 2, 7).",
        what="Form factor f(q∥) is the FT of the island shape (Physica (3)). Physica’s fits used a Gaussian average of |f|² rather than a pure disk.",
        eq=r"$$f(q_\parallel)\propto \frac{2J_1(q_\parallel R)}{q_\parallel R}$$",
        inline=r"First zero of \(J_1\) is near \(q_\parallel R\approx 3.83\), so a 36 Å disk has a form-factor node around \(0.11\,\mathrm{\AA}^{-1}\).",
        scattering="Would multiply S_diff. Not applied on the right-hand plots.",
        slider="Bigger R: fatter disks, fewer fit in the box at fixed min-spacing.",
        limits="Hard disks, not Wu’s in-plane correlation g_pair.",
    ),
    "island_d": Item(
        title="More about min spacing d",
        blurb="Exclusion diameter: dart-thrown centres cannot sit closer than d. A cheap stand-in for a hole in S(q) at small q, not Wu (13).",
        what="A liquid-like island gas has S(q)→0 as q→0 if the film cannot compress (coverage conserved) and a peak near 2π/d (ch. 7). This toy only enforces a hard minimum distance.",
        eq=r"$$S(q)\to 0\quad(q\to 0)\quad\text{for conserved coverage (ideal)}$$",
        inline=r"Earlier explorations needed a modest packing fraction to avoid \(S<0\); this live app does not compute \(S(q)\) at all.",
        scattering="Unused in the detector.",
        slider="Larger d: fewer islands, more regular looking gaps.",
        limits="Not a pair-correlation function g_pair(r).",
    ),
    "heatmap": Item(
        title="More about the true heatmap",
        blurb="One realisation of z(x,y). Colour is height in Å. Illustrative — not an AFM of your sample.",
        what="Drawn as an FFT-filtered Gaussian field matching C(R), then optionally disks. The beam, if it averages many patches, does not measure this picture (ch. 3).",
        eq=r"$$P(\mathbf{q}_\parallel)=\int d^{2}R\,C(\mathbf{R})\,e^{-i\mathbf{q}_\parallel\cdot\mathbf{R}}$$",
        inline=r"The map is \(\mathcal{F}^{-1}[\tilde\eta\sqrt{P}]\), rescaled so \(\mathrm{std}(z)=\sigma\).",
        scattering="Used for empirical C(R) on the left. Detector intensity is not |FT(this map)|²; it is the Born kernel of the analytic C.",
        slider="σ, ξ, h, family, seed, islands all rewrite the picture. Measurement sliders do not — the surface is cached.",
        limits="Periodic box. Colour scale autoscale, so a flat-looking image may still have small σ.",
    ),
    "CR": Item(
        title="More about C(R)",
        blurb="Height–height correlation ⟨z(R)z(0)⟩. Solid: theory. Dashed: estimated from the map. C(0)=σ²; C(∞)→0 if a cutoff exists.",
        what="PRB’s C (ch. 4.1). Some communities plot C/σ². This app plots Å², un-normalised, like PRB.",
        eq=r"$$C(\mathbf{R})=\bigl\langle z(\mathbf{R})z(\mathbf{0})\bigr\rangle$$",
        inline=r"The dashed curve is the radial bin of the FFT autocorrelation of the map (ergodic stand-in for \(\langle z(0)z(R)\rangle\), ch. 3.3).",
        scattering="S_diff ∝ Hankel[e^{q_z² C}−1]. At small q_z σ, ≈ Hankel[C] = PSD.",
        slider="σ sets the intercept. ξ sets the decay length. h sets the short-R shape. A ragged dashed line means the box is too small to sample C.",
        limits="Finite-R cosine taper on Hankel integrals (not shown on this plot). Empirical C is biased at large R by the periodic image.",
    ),
    "gR": Item(
        title="More about g(R)",
        blurb="Height-difference function ⟨[z(R)−z(0)]²⟩=2σ²−2C(R). Saturates at 2σ² when points become independent.",
        what="PRB (2.5), also called the structure function (ch. 4.2). Self-affine without cutoff: g∝R^{2h} forever.",
        eq=r"$$g(R)=2\sigma^{2}-2C(R)$$",
        inline=r"The Gaussian average in Born is \(e^{-q_z^{2} g(R)/2}=e^{-q_z^{2}\sigma^{2}}e^{q_z^{2} C(R)}\) (ch. 5.1).",
        scattering="You never measure g directly; you measure its consequence in S_spec and S_diff.",
        slider="Tracks C: if C fails to decay, g fails to saturate — usually ξ too large versus L.",
        limits="Plotted from theory C, not from pairwise heights on the map.",
    ),
    "psd": Item(
        title="More about the PSD",
        blurb="Power spectral density of height: FT of C(R) (Wiener–Khinchin). Not equal to intensity except at small q_z σ.",
        what="P(q∥)=⟨|z̃|²⟩/area (ch. 4.4). Parseval: σ² is the integral of P. Large ξ ⇒ P concentrated at small q.",
        eq=r"$$P(q_\parallel)=2\pi\int_0^{\infty} R\,dR\,C(R)\,J_0(q_\parallel R)$$",
        inline=r"Isotropy turned the 2D FT into a Hankel transform of order 0 (ch. 4.5). Intensity at large \(q_z\sigma\) uses \(e^{q_z^{2}C}-1\), not \(C\).",
        scattering="PRB (4.43): S_diff ∝ P only after linearising e^{q_z² C}−1≈q_z² C.",
        slider="h controls the high-q slope-ish tail; ξ the low-q pile-up. Log y-scale hides nothing but needs P>0 (we clip at 1e−30).",
        limits="Computed from analytic C with a cosine taper, not from |FFT(map)|².",
    ),
    "wavelength": Item(
        title="More about wavelength λ",
        blurb="X-ray wavelength (Å). Cu Kα is 1.54 Å. Sets k=2π/λ and therefore how angles map into q.",
        what="Vacuum wavevector k_0=2π/λ (ch. 8.4). Smaller λ ⇒ larger q at the same angle.",
        eq=r"$$k=2\pi/\lambda,\quad q_z=k(\sin\alpha+\sin\beta),\quad q_x=k(\cos\beta-\cos\alpha)$$",
        inline=r"Rocking at fixed \(2\theta=2\alpha\) (this app) moves \(\alpha\) and \(\beta\) in opposite directions so \(q_z\) stays nearly constant.",
        scattering="Enters only through kinematics, not through C(R). Born S is a function of q, not of λ separately.",
        slider="Shorter λ stretches the q_x axis of a rocking scan (same degree range covers more q). Critical angle also depends on λ via n, but δ,β here are fixed numbers, not scaled with λ².",
        limits="Optical constants δ,β are the PRB-like Pyrex illustration (6.3×10⁻⁶, 8.5×10⁻⁸) and do not track λ. Toy.",
    ),
    "alpha": Item(
        title="More about incidence α",
        blurb="Grazing incidence (degrees). Rocking is centred here. Default 0.55° so q_x is visible. Footprint ~1/sinα.",
        what="Grazing geometry of PRB / ch. 8. α and exit β define q. Below the critical angle α_c≈√(2δ) one has total external reflection and |T| is small except near α_c (Yoneda).",
        eq=r"$$\alpha_c\approx\sqrt{2\delta},\qquad \lvert T(\alpha)\rvert^{2}\ \text{peaks near }\alpha_c$$",
        inline=r"With \(\delta=6.3\times 10^{-6}\), \(\alpha_c\sim 0.20^{\circ}\). The slider default sits above that.",
        scattering="Rocking: 2θ=2α fixed, scan offset in α. Specular: α=β, q_z=4π sinα / λ. DWBA multiplies by |T(α)T(β)|² when ticked.",
        slider="Very small α: rocking q_x range collapses (cosines almost equal) and footprint blows up. That is why the default is 0.55°, not 0.40°.",
        limits="No sample-size overfill model (ch. 8.2 warned that is ‘tricky’).",
    ),
    "scan": Item(
        title="More about scan type",
        blurb="Rocking: transverse S_diff vs q_x at nearly fixed q_z. Specular: Debye–Waller envelope vs q_z. q-map: 2D (q∥, q_z).",
        what="What you can identify (ch. 5.4): specular constrains σ (and density); rocking/transverse constrains h,ξ via S_diff(q∥). Only specular cannot see h,ξ.",
        eq=r"$$S_{\mathrm{diff}}\propto\frac{e^{-q_z^{2}\sigma^{2}}}{q_z^{2}}\int_0^{\infty} R\,dR\,J_0(q_\parallel R)\bigl(e^{q_z^{2}C(R)}-1\bigr)$$",
        inline=r"Specular in the toy is \(e^{-q_z^{2}\sigma^{2}}/q_z^{4}\) (Porod × Debye–Waller), not a δ-function sampled by resolution.",
        scattering="Rocking uses the Born (2.28b) kernel along a trajectory q_x(α), q_z(α). q-map evaluates that kernel on a grid. Specular does not call S_diff.",
        slider="Switch to specular: the fit table still shows ξ,h because the app runs an auxiliary noiseless rocking kernel — labelled as a toy, not extra data. q-map fits the middle q_z row.",
        limits="Shapes only: no (Nb)², no flux, no dead time. Rocking is in-plane (q_y=0), not a full 3D resolution ellipsoid.",
    ),
    "npts": Item(
        title="More about detector points",
        blurb="How many samples along the scan (or √n on a q-map). More points: smoother curves, slightly slower Hankel loop.",
        what="A real detector has pixels; here it is just a sampling of the model I(q).",
        eq=r"$$I_i=I_{\mathrm{model}}(q_i)$$",
        inline=r"q-map side length is \(\max(16,\min(40,\sqrt{n}))\).",
        scattering="Does not change physics, only discretisation and the resolution/pixel rebin grid.",
        slider="Watch compute time in the status line. Fit quality barely needs >81 on the default rocking.",
        limits="Not a real detector solid angle.",
    ),
    "rock": Item(
        title="More about rocking range",
        blurb="Half-width in degrees of the rocking offset. Converts to q_x≈k α_off at small angles (α in rad).",
        what="A rocking scan at fixed 2θ swings the sample (or the two angles oppositely) through the specular ridge (ch. 8).",
        eq=r"$$q_x=k\bigl(\cos\beta-\cos\alpha\bigr)\approx k\,\omega\cos\theta$$",
        inline=r"\(\omega\) is the offset from specular. At \(\alpha=0.55^{\circ}\) and \(\lambda=1.54\,\mathrm{\AA}\) a \(0.45^{\circ}\) range is a modest \(q_x\) window.",
        scattering="Sets which part of S_diff(q∥) you see. Too narrow: looks like a spike and ξ is ill-posed. Too wide: you leave the near-specular Born/DWBA comfort zone.",
        slider="Unused for specular and only indirectly for q-map (q-map uses a fixed 0–0.22 Å⁻¹ q∥ axis).",
        limits="Points with α or β < 0.03° are dropped so we do not hit the horizon.",
    ),
    "dq": Item(
        title="More about resolution Δq",
        blurb="Gaussian FWHM in Å⁻¹ convolved along the scan. A δ-function specular would become this blob (ch. 8.1).",
        what="I_meas=S∗R_res. Never fit S_diff line shapes without stating R_res (ch. 8.1, PRB Sec. V).",
        eq=r"$$I_{\mathrm{meas}}(q)=\int dq'\,S(q')\,R_{\mathrm{res}}(q-q')$$",
        inline=r"FWHM \(\Delta q\) maps to Gaussian \(\sigma=\Delta q/2.355\) in bin units. Convolution theorem: a finite real-space window is this blur in \(q\).",
        scattering="Widens the rocking peak, mimicking a shorter effective ξ. The fitter does not deconvolve, so fitted ξ shrinks as you raise Δq.",
        slider="Set to 0 for a clean theory curve. q-map blurs only along q∥.",
        limits="1D Gaussian, not the actual slit machine. Out-of-plane q_y integration (PRB (2.30)) is omitted.",
    ),
    "xic": Item(
        title="More about coherence length ξ_coh",
        blurb="Multiplies C(R) by e^{−R/ξ_coh} in the detector model only. Caps the R integral; can restore a specular-like peak for logs (ch. 6, 8.3).",
        what="Projected coherence from bandwidth and source size. Distinct from the sample’s ξ. PRB used a Kummer-function cutoff (2.33) following Dutta & Sinha; we use a simple exponential window.",
        eq=r"$$C_{\mathrm{eff}}(R)=C(R)\,e^{-R/\xi_{\mathrm{coh}}}$$",
        inline=r"Equivalently, \(S(q_\parallel)\) is convolved with a kernel of width \(\sim 2\pi/\xi_{\mathrm{coh}}\).",
        scattering="Damps large-R correlations → extra blur in q∥ and a slightly higher apparent specular weight in the split (because C_eff(∞)=0 even for logs).",
        slider="Does not change the left-hand true C(R). Only the detector and the fit (which sees the detector) move. Lower ξ_coh: wider rocking peak.",
        limits="Exponential window, not the Kummer/Dutta–Sinha form. Default 600 Å is shorter than PRB’s micron-scale illustration, matched to this tiny box.",
    ),
    "foot": Item(
        title="More about footprint 1/sinα",
        blurb="When on, intensity is divided by sinα (PRB (2.13) flux-to-reflectivity). Grazing beams illuminate a long stripe.",
        what="Beam width w intercepts length w/sinα on the surface, until the beam spills off the sample (ch. 8.2).",
        eq=r"$$I\to I/\sin\alpha$$",
        inline=r"Overfill (beam larger than the sample) is not modelled; the factor is only \(1/\sin\alpha\). PRB Sec. V called a finite-sample correction “tricky”.",
        scattering="Weights low-α ends of a rocking scan up. Specular: extra 1/sinα on top of 1/q_z⁴.",
        slider="Untick to see the raw Born/DWBA shape. Most visible at the lowest α on a wide rocking scan.",
        limits="No finite sample length, no beam profile.",
    ),
    "dwba": Item(
        title="More about DWBA |T|² wings",
        blurb="Optional factor |T(α)T(β)|² on diffuse (PRB (4.41)). Makes Yoneda-like wings near α_c. Uses vacuum q, not in-medium q_z′.",
        what="Distorted-wave Born: roughness perturbs the exact smooth-surface waves (ch. 8.5, PRB Sec. IV). Leading diffuse ~ Born S × |T(α)|²|T(β)|².",
        eq=r"$$T=\frac{2k_{z0}}{k_{z0}+k_{z1}},\qquad k_{z0}=k\sin\alpha,\quad k_{z1}=k\sqrt{n^{2}-\cos^{2}\alpha}$$",
        inline=r"This toy multiplies \(S_{\mathrm{diff}}\) by \(\lvert T(\alpha)T(\beta)\rvert^{2}\) and keeps vacuum \(q_z\). In-medium \(q_z'\) (PRB (4.41), Physica (8)) is omitted.",
        scattering="Yoneda: |T| peaks near α_c so rocking grows shoulders when α or β crosses α_c. Specular scan does not apply this factor (it uses Born DW × Porod).",
        slider="Tick on a rocking scan at α near 0.2–0.4° to see wings. Far above α_c, |T|→1 and little changes.",
        limits="n=1−δ+iβ with Pyrex-like δ,β from PRB Sec. V as optics illustration. First-order DWBA is not unitary below θ_c. Not Nevot–Croce (that would be e^{−q_z q_z′ σ²} on |R|²).",
    ),
    "noise": Item(
        title="More about noise mix",
        blurb="0 = noiseless model. 1 = Poisson draws at counts_scale=1e5 mixed in. Fit uncertainties explode when the curve is noisy.",
        what="Photon counting is Poisson. Mixed here as (1−m) I + m Poisson(I×scale)/scale so you can morph from theory to counts.",
        eq=r"$$I_{\mathrm{obs}}=(1-m)I + m\,\mathrm{Poisson}(I\cdot S)/S$$",
        inline=r"\(m\) is the slider, \(S=10^{5}\). Seed for noise is the surface seed + 17.",
        scattering="Does not change the expected S; it changes one draw. The fitter treats all points equally (no Poisson weights).",
        slider="At 0 the inversion/fit can recover C reasonably. At large m the table’s 1σ balloons and C_inv rings.",
        limits="Not a full error model (no dead time, no cosmic, no background except the unused background parameter defaulting to 0).",
    ),
    "pix": Item(
        title="More about pixel Δq",
        blurb="Rebins the scan into pixels of this width (Å⁻¹). 0 keeps native samples. A crude detector-pixel model.",
        what="Distinct from resolution FWHM: rebin is averaging into fewer bins, not a Gaussian smear (though both lose information).",
        eq=r"$$I_{\mathrm{pix}}(q_c)=\mathrm{mean}\{I(q):q\in\mathrm{bin}(q_c)\}$$",
        inline=r"Number of bins is \(\max\bigl(8,\mathrm{round}((q_{\max}-q_{\min})/\Delta q_{\mathrm{pix}})\bigr)\).",
        scattering="Coarse pixels hide the rocking peak shape and bias ξ like a poor resolution function.",
        slider="Leave at 0 unless you want to see discretisation. Unused in a useful way on q-map (q-map uses its own grid).",
        limits="Uniform bins in the plotted x, not equal solid angle.",
    ),
    "detector": Item(
        title="More about detector data",
        blurb="Toy counts (arbitrary units, peak often normalised). Not measured data. Shape from Born S_diff or specular DW, then resolution, footprint, noise.",
        what="A detector records I(q), not z(x,y) (ch. 2, 8). Constants (Nb)², area, flux are dropped; curves are shapes.",
        eq=r"$$S(\mathbf{q})\propto\frac{e^{-q_z^{2}\sigma^{2}}}{q_z^{2}}\int d^{2}R\,e^{q_z^{2}C(\mathbf{R})}\,e^{-i\mathbf{q}_\parallel\cdot\mathbf{R}}$$",
        inline=r"Split \(e^{q_z^{2}C}=1+(e^{q_z^{2}C}-1)\) into specular \(\delta(\mathbf{q}_\parallel)\) plus diffuse (PRB (2.28a,b)).",
        scattering="This is the forward model. Inverse problems live in the panels below.",
        slider="Every right-hand control, plus surface σ,ξ,h,family (via C). Not N,L,seed (except islands visual). Cache: changing only measurement knobs skips regenerating z(x,y).",
        limits="No beam divergence ellipsoid, no sample curvature, no absorption beyond β in optional T.",
    ),
    "fit_table": Item(
        title="More about the fit vs true table",
        blurb="Least-squares (σ, ξ, h) of a self-affine Born S_diff to the 1D q∥ line, after normalising both curves to 1. 1σ is √diag(pcov) from curve_fit — not an experimental error bar.",
        what="Ch. 8.6 sketch: pick a morphology class, compute S, optionally smear, then fit. Here the class is self-affine (Gaussian family forces h=1). Capillary surfaces are still fitted as self-affine, so expect mismatch.",
        eq=r"$$\min_{\sigma,\xi,h}\ \bigl\lVert \hat S_{\mathrm{diff}}(q_\parallel;\sigma,\xi,h)-\hat I(q_\parallel)\bigr\rVert^{2}$$",
        inline=r"Hats mean ‘divided by their max’. Specular scans have no \(q_\parallel\), so the fitter is fed an auxiliary noiseless rocking kernel at the same surface.",
        scattering="Identifiability: σ also sits in the DW prefactor; ξ,h in the Hankel kernel. Resolution and ξ_coh are not fitted — they bias ξ.",
        slider="Noiseless rocking at default N usually recovers σ,ξ,h to a few percent. Specular-only would not; the auxiliary rocking is why the table still fills.",
        limits="pcov 1σ assumes Gaussian residuals of the normalised curve. Bounds σ∈[0.3,25], ξ∈[5, min(R_max,250)], h∈[0.15,0.95]. If curve_fit fails, the table shows the initial guess and ‘—’ errors.",
    ),
    "fit_curves": Item(
        title="More about rebuilt C(R) / PSD",
        blurb="Black: true C and P. Red: self-affine C from the fitted (σ,ξ,h). Dotted: Hankel inversion of S_diff for C (needs a σ). Shapes only.",
        what="Forward: C→S_diff. Inverse: (i) parametric fit; (ii) invert the Hankel of (e^{q_z² C}−1) given σ (ch. 5, 4.5).",
        eq=r"$$e^{q_z^{2}C(R)}-1=\mathcal{H}^{-1}\!\bigl[q_z^{2} e^{q_z^{2}\sigma^{2}}S_{\mathrm{diff}}\bigr]$$",
        inline=r"Then \(C=\ln(1+f)/q_z^{2}\). That inversion assumes the Born kernel, no DWBA wings, no resolution, and a known \(\sigma\).",
        scattering="PSD panels are Hankel[C_true] vs Hankel[C_fit], not |I(q)|. Do not read the red PSD as ‘the measurement’.",
        slider="On a clean rocking scan, red overlaps black. Resolution, noise, ξ_coh, DWBA, or capillary family peel them apart. Dotted C_inv rings near R=0 from finite-q truncation.",
        limits="Tapered Hankel; C_inv is clipped to ±5σ². Specular uses auxiliary rocking for both the fit and this inversion.",
    ),
    "rebuild": Item(
        title="More about the rebuilt map",
        blurb="NOT the original. A new random-phase FFT field whose C(R) is the fitted one. Scattering measures intensity (no phase of z̃).",
        what="Wiener–Khinchin gives P=FT[C], which is |z̃|² in expectation, not arg(z̃). Drawing a new phase is the same algorithm as the true map, different seed (ch. 3–4).",
        eq=r"$$z_{\mathrm{reb}}=\mathcal{F}^{-1}\!\bigl[e^{i\theta_{\mathrm{new}}}\sqrt{P_{\mathrm{fit}}}\bigr]$$",
        inline=r"\(\theta_{\mathrm{new}}\) is not the true phase. There is no unique \(z(x,y)\) compatible with \(S_{\mathrm{diff}}\).",
        scattering="This is pedagogy, not phase retrieval (CDI/ptychography would need coherent oversampling and a different inverse).",
        slider="It should look statistically like the left map (same blob size) but the hills are elsewhere. If the fit is bad, the blob size is wrong too.",
        limits="Uses fitted self-affine C even when the truth was capillary or had islands. Seed is original+3 so it cannot accidentally match.",
    ),
    "sweep": Item(
        title="More about the diagnostic sweep",
        blurb="Locks the current left-hand surface and sweeps one measurement knob at a time. Scores fitted C(R) and (σ, ξ, h) against the true surface — never RMSE of a rebuilt z(x,y). Click Run sweep; sliders do not trigger it.",
        what="Scattering measures intensity, not phase of z̃, so there is no unique z(x,y) to score against (ch. 3–5). The honest accuracy measures are relative errors on the isotropic parameters and the shape of C(R) (or S(q∥)) over the measured window. The knee is the first grid point (walking from the good end) where |Δξ|/ξ exceeds a threshold (default 10%). The limiter is whichever swept quantity is closest to, or past, that knee at the current settings.",
        eq=r"$$e_\sigma=\lvert\hat\sigma-\sigma\rvert/\sigma,\quad e_\xi=\lvert\hat\xi-\xi\rvert/\xi,\quad e_h=\lvert\hat h-h\rvert,\quad \mathrm{RMS}\log C=\bigl\langle[\ln C_{\mathrm{fit}}-\ln C_{\mathrm{true}}]^{2}\bigr\rangle^{1/2}$$",
        inline=r"Specular has no \(q_\parallel\): \(\xi\) and \(h\) are unidentified. An auxiliary noiseless rocking kernel in the live table is a cheat, not a recovery from the specular scan.",
        scattering="Each sweep point reuses the same forward model + fit as the two-column view. Coherence multiplies C by e^{−R/ξ_coh} in the detector only. Resolution convolves I(q). Noise mixes Poisson counts. Incidence sets kinematics (and footprint). Scan type is discrete: rocking/q-map have q∥; specular does not.",
        slider="Run sweep is a button, not a slider. The surface (σ, ξ, h, family, N, L, seed, islands) is locked at click time. Hold-ideal freezes the other knobs at noiseless / Δq=0 / ξ_coh=2000 Å / rocking while one axis walks. Cached plots stay until you run again; the main view is not recomputed.",
        limits="Illustrative, not experimental data. qz_min/qz_max are derived, not swept as live controls; rock_range_deg is the optional q-window. N is the current grid (≤96 in WASM). A full 6-axis × 8-point sweep is tens of forward+fit calls and is slow in Pyodide — pick one axis (coherence) there.",
    ),
    "json": Item(
        title="More about session JSON",
        blurb="Snapshot of the sliders for reproducibility. Session only — nothing is written to disk unless you copy it.",
        what="A dict with illustrative=True and not_experimental_data=True so a pasted file cannot be mistaken for a measurement.",
        eq=r"$$\text{params}=\{\text{surface},\ \text{measure}\}$$",
        inline=r"No hidden state: the seed in the JSON is the surface seed; detector noise uses \(\mathrm{seed}+17\).",
        scattering="Does not enter physics.",
        slider="Updates after every refresh. Copy from the box if you want to quote a setting.",
        limits="Not a NeXus file. No units metadata beyond the comments in this page.",
    ),
}


REQUIRED_KEYS = tuple(ITEMS.keys())
