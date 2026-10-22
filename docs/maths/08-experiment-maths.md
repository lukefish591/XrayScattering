# 8. Experiment-side maths

Theory gives S(<b>q</b>). A detector gives counts. This chapter is the map between them, plus Fresnel / DWBA.

## 8.1 Resolution convolution

The instrument accepts a blob of <b>q</b> around the nominal setting. If R<sub>res</sub>(<b>q</b>) is that blob (normalised to 1), the measured intensity is a convolution

$$
I_{\mathrm{meas}}(\mathbf{q})=\int d^3q'\,S(\mathbf{q}')\,R_{\mathrm{res}}(\mathbf{q}-\mathbf{q}').
$$

A sharp specular δ(q<sub>x</sub>)δ(q<sub>y</sub>) becomes a peak with the shape of R<sub>res</sub> in q<sub>x</sub>,q<sub>y</sub>. PRB Sec. V: they used a Gaussian width taken from the no-pit / high-resolution specular. Wide open out-of-plane slits ≈ integrate <i>S</i> over q<sub>y</sub> (PRB (2.30)).

Never fit S<sub>diff</sub> line shapes without stating R<sub>res</sub>. Convolution theorem: multiplying the sample by a finite illuminated footprint in real space *is* this blur in <i>q</i>.

## 8.2 Illuminated footprint

A beam of width <i>w</i> in the scattering plane hits a grazing surface of angle <i>α</i>. The **footprint** along <i>x</i> is w/ sinα (for <i>α</i> larger than the angle where the beam spills off the sample). Intensity formulae in PRB (2.13) include a 1/ sinθ<sub>1</sub> converting flux to reflectivity.

When <i>α</i> is so small that the beam overfills the sample, you must correct by the intercepted fraction (PRB Sec. V warns this is “tricky”). Teaching scripts ignored overfill.

## 8.3 Coherence length as a cutoff

A quasi-monochromatic beam is coherent over a length ξ<sub>coh</sub> projected on the surface (longitudinal and transverse coherence from bandwidth and source size). The <i>R</i> integrals in S<sub>diff</sub> are cut off at ∼ξ<sub>coh</sub>. That:

- restores a specular-like peak for capillary waves (ch. 6);
- washes out island side peaks if d≳ξ<sub>coh</sub> (ch. 7).

Model it as multiplying C(R) or g<sub>pair</sub>(r)-1 by a window W(R/ξ<sub>coh</sub>), or as convolving S(q<sub>∥</sub>) with a kernel of width ∼ 2π/ξ<sub>coh</sub>.

## 8.4 One-dimensional wave equation, Fresnel <i>R</i> and <i>T</i>

Ignore roughness. Density (hence refractive index) jumps at z=0: n=1 for z>0 (vacuum) and n=1-δ+iβ for z<0 (sample). X-ray n<1, so **total external reflection** is possible.

TE field (or the neutron wave function) obeys the Helmholtz / Schrödinger equation PRB (4.1):

$$
\nabla^2\psi+k_0^2 n^2(z)\psi=0,\qquad k_0=2\pi/\lambda.
$$

For a plane wave with grazing angle <i>α</i>, ψ=u(z)e<sup>ik<sub>x</sub> x</sup> and k<sub>x</sub>=k<sub>0</sub> cosα is conserved (Snell). Then

$$
u''(z)+k_z^2(z)u=0,\qquad k_z(z)=k_0\sqrt{n(z)^2-\cos^2\alpha}.
$$

**Vacuum:** k<sub>z0</sub>=k<sub>0</sub> sinα. **Medium:** k<sub>z1</sub>=k<sub>0</sub>√(n<sup>2</sup>- cos<sup>2</sup>α) (branch Im k<sub>z1</sub>≥ 0 so the wave decays into an absorbing sample).

General solution: incident + reflected for z>0, transmitted for z<0. Continuity of <i>u</i> and u' at z=0 (Maxwell / Schrödinger matching) gives PRB (4.8):

$$
R=\frac{k_{z0}-k_{z1}}{k_{z0}+k_{z1}},\qquad
T=\frac{2k_{z0}}{k_{z0}+k_{z1}}.
$$

(The paper writes the same in terms of sinθ<sub>1</sub> and n sinθ<sub>t</sub>.) **Critical angle:** k<sub>z1</sub>=0 when cosα=n (real <i>n</i>), i.e. α<sub>c</sub>=arccos(n)≈√(2δ). Below α<sub>c</sub>, k<sub>z1</sub> is imaginary and ∣R∣≈ 1. ∣T∣ **peaks near α<sub>c</sub>** (the field at the surface is large). Numeric: `code/10_fresnel_matching.py`.

## 8.5 DWBA and Nevot–Croce

**Distorted-wave Born:** treat roughness as a perturbation V<sub>2</sub> on the *exact* smooth-surface wave functions (PRB Sec. IV). To leading order, diffuse intensity is the Born <i>S</i> of chapter 5 multiplied by ∣T(α)∣<sup>2</sup>∣T(β)∣<sup>2</sup> and with q<sub>z</sub> replaced by the in-medium q<sub>z</sub>' (PRB (4.41); Physica (8)). Yoneda peaks: <i>α</i> or β=θ<sub>c</sub>.

**Nevot–Croce (PRB (4.34)), for q<sub>z</sub>σ≲ 1:**

$$
\lvert R\rvert^2\simeq\lvert R_F\rvert^2\exp(-q_z q_z'\sigma^2).
$$

Intuition: Born Debye–Waller used vacuum q<sub>z</sub> on both legs, e<sup>-q<sub>z</sub><sup>2</sup>σ<sup>2</sup></sup>. In DWBA one leg is the transmitted wave ∼ e<sup>ik<sub>z1</sub> z</sup>, so one factor is q<sub>z</sub>' rather than q<sub>z</sub>. Expanding PRB’s full (4.33) for small q<sub>z</sub>σ is stated to recover (4.34); for q<sub>z</sub>σ≫ 1 PRB says **use Born**, not (4.33).

**Uncertain:** this primer does **not** reproduce every matrix element F<sub>±</sub>(𝒦) in PRB (4.19)–(4.33). If you need that algebra, read Sec. IV of the PDF. We use (4.8), (4.34), and (4.41) as the working set.

Below θ<sub>c</sub>, first-order DWBA does **not** give ∣R∣<1 from diffuse losses (unitarity; PRB text after Fig. 5). Flag that if you ever fit α<θ<sub>c</sub>.

## 8.6 From counts to a fitted C(R)

**Forward model (what to code):**

1. Choose morphology class: continuous C(R;σ,h,ξ) or islands (φ,Δ,f,S), plus n(z) stack.
2. Compute S<sub>spec</sub>+S<sub>diff</sub> (Born), optionally ×∣T(α)T(β)∣<sup>2</sup>.
3. Convolve with R<sub>res</sub>; apply footprint; add background.
4. Compare to I<sub>meas</sub> with a weighted least-squares χ<sup>2</sup>=∑<sub>i</sub>(I<sub>i</sub>-I<sub>mod,i</sub>)<sup>2</sup>/Var<sub>i</sub>.

**Least squares:** parameters <b>p</b> minimise χ<sup>2</sup>(<b>p</b>). Identifiability is the curvature of χ<sup>2</sup>: a long valley means two parameters trade off.

**Identifiable / not (typical, not a theorem):**

| Usually identifiable | Often not, from specular alone |
| --- | --- |
| θ<sub>c</sub> / <i>δ</i>, film thickness <i>t</i> (Kiessig period) | <i>h</i> vs <i>ξ</i> |
| <i>σ</i> from specular falloff (if diffuse subtracted) | absolute <i>φ</i> vs island form factor |
| Yoneda position ⇒ θ<sub>c</sub> | global vs local island density |
| side-peak position ⇒ 2π/d | g<sub>pair</sub>(r) beyond the first shell |

**Do not invert** I(q<sub>∥</sub>) as if it were P(q<sub>∥</sub>) unless q<sub>z</sub>σ≪ 1. The honest fit is always **forward**. Fill [experiment-questionnaire.md](../experiment-questionnaire.md) before introducing extra parameters.
