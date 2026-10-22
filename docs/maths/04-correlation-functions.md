# 4. Correlation functions, power spectra, and J<sub>0</sub>

## 4.1 Height–height correlation

With ⟨z⟩=0, define the **height–height correlation** (PRB <i>C</i>)

$$
C(\mathbf{R})=\bigl\langle z(\mathbf{R})z(\mathbf{0})\bigr\rangle.
$$

At <b>R</b>=<b>0</b>, C(<b>0</b>)=⟨z<sup>2</sup>⟩=σ<sup>2</sup>. If distant points are uncorrelated, C(<b>R</b>)→ 0 as R→∞.

## 4.2 The structure function g(R)

PRB (2.5) uses the **height-difference (structure) function**

$$
g(\mathbf{R})=\bigl\langle\bigl[z(\mathbf{R})-z(\mathbf{0})\bigr]^2\bigr\rangle.
$$

Expand the square:

$$
g(\mathbf{R})=\langle z(\mathbf{R})^2\rangle+\langle z(\mathbf{0})^2\rangle-2\langle z(\mathbf{R})z(\mathbf{0})\rangle=2\sigma^2-2C(\mathbf{R}),
$$

which is PRB (2.23)–(2.24) (their ⟨z<sup>2</sup>⟩=σ<sup>2</sup>). Rearranged: C=σ<sup>2</sup>-g/2. If C(∞)=0, then g(∞)=2σ<sup>2</sup>: widely separated points differ by two independent copies of <i>z</i>, so the mean-square difference is 2σ<sup>2</sup>.

## 4.3 Autocorrelation versus <i>C</i>

For zero-mean stationary fields, “autocorrelation” *is* C(<b>R</b>). Some communities normalise C(<b>R</b>)/σ<sup>2</sup>, which runs from 1 to 0. PRB does not normalise.

## 4.4 Power spectral density and Wiener–Khinchin

The **power spectral density** (PSD) of the height is the expected squared FT of one realisation, per area:

$$
P(\mathbf{q}_\parallel)=\lim_{A\to\infty}\frac{1}{A}\bigl\langle\lvert \tilde z_A(\mathbf{q}_\parallel)\rvert^2\bigr\rangle,
$$

where z̃<sub>A</sub> is the FT of <i>z</i> restricted to a patch of area <i>A</i>.

**Wiener–Khinchin theorem:** <i>P</i> is the FT of <i>C</i>,

$$
P(\mathbf{q}_\parallel)=\int d^2R\,C(\mathbf{R})\,e^{-i\mathbf{q}_\parallel\cdot\mathbf{R}},\qquad
C(\mathbf{R})=\frac{1}{(2\pi)^2}\int d^2q_\parallel\,P(\mathbf{q}_\parallel)\,e^{i\mathbf{q}_\parallel\cdot\mathbf{R}}.
$$

**Why (sketch).** |z̃|<sup>2</sup>=∫ d<sup>2</sup>R∫ d<sup>2</sup>R' z(<b>R</b>)z(<b>R</b>')e<sup>-i<b>q</b>·(<b>R</b>-<b>R</b>')</sup>. Stationarity: the inner average is C(<b>R</b>-<b>R</b>'). One integral gives the area <i>A</i>, the other is the FT of <i>C</i>.

Parseval: σ<sup>2</sup>=C(<b>0</b>)=(2π)<sup>-2</sup>∫ d<sup>2</sup>q P(<b>q</b>). Roughness is the integral of the PSD.

**Link to intensity.** Chapter 2: ∣A∣<sup>2</sup> is the FT of ⟨ρ(<b>r</b>)ρ(<b>r</b>')⟩. For a surface, after the Gaussian average (chapter 5), the *diffuse* part of the intensity is the FT of e<sup>q<sub>z</sub><sup>2</sup> C(R)</sup>-1. At **small** q<sub>z</sub>σ, e<sup>q<sub>z</sub><sup>2</sup> C</sup>-1≈ q<sub>z</sub><sup>2</sup> C, so S<sub>diff</sub> is proportional to the FT of <i>C</i>, i.e. to the height PSD (PRB (4.43)). At large q<sub>z</sub>σ that linearisation is false: intensity is **not** the PSD of height. Numeric: `code/06_wiener_khinchin.py`.

## 4.5 Radial averaging and the Hankel transform

If C=C(R) only, its 2D FT is a **Hankel transform of order 0**. Derivation of J<sub>0</sub>:

Write <b>q</b><sub>∥</sub>·<b>R</b>=q<sub>∥</sub> R cosθ, where <i>θ</i> is the angle between <b>q</b><sub>∥</sub> and <b>R</b>. Then

$$
\int d^2R\,C(R)e^{-i\mathbf{q}_\parallel\cdot\mathbf{R}}
=\int_0^\infty R\,dR\,C(R)\int_0^{2\pi}d\theta\,e^{-i q_\parallel R\cos\theta}.
$$

The **Bessel function of the first kind of order zero** is *defined* by that angular integral (any of the equivalent standard forms; J<sub>0</sub> is even):

$$
J_0(x)=\frac{1}{2\pi}\int_0^{2\pi}d\theta\,e^{i x\cos\theta}.
$$

Hence ∫<sub>0</sub><sup>2π</sup>dθ e<sup>-i q R cosθ</sup>=2π J<sub>0</sub>(q R), and

$$
\int d^2R\,C(R)e^{-i\mathbf{q}_\parallel\cdot\mathbf{R}}=2\pi\int_0^\infty R\,dR\,C(R)\,J_0(q_\parallel R).
$$

That is why PRB (2.28b) contains ∫ R dR J<sub>0</sub>(q<sub>∥</sub> R)F(q<sub>z</sub>,R). Numeric check of the angular integral: `code/05_hankel_j0.py`.

Series: J<sub>0</sub>(x)=1-x<sup>2</sup>/4+⋯. For x≫ 1, J<sub>0</sub> oscillates and decays as √(2/(π x)) cos(x-π/4). Small q<sub>∥</sub> (large islands) samples the large-<i>R</i> part of <i>C</i>.
