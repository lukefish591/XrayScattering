# 5. From C(R) to specular + diffuse (PRB 1988)

This chapter is the core of correlation-function modelling for a **continuous** rough surface.

## 5.1 Average the Born phase

Start from PRB (2.4): intensity ∝ q<sub>z</sub><sup>-2</sup> times ∫ d<sup>2</sup>R d<sup>2</sup>R' ⟨exp(-iq<sub>z</sub>[z'-z])⟩ exp(-i<b>q</b><sub>∥</sub>·(<b>R</b>'-<b>R</b>)).

Assume X=z(<b>R</b>')-z(<b>R</b>) is Gaussian with mean 0 (heights measured from the average plane) and ⟨X<sup>2</sup>⟩=g(<b>R</b>'-<b>R</b>). Chapter 3:

$$
\bigl\langle e^{-iq_z X}\bigr\rangle=e^{-q_z^2 g(\mathbf{R}'-\mathbf{R})/2}.
$$

That is the **Gaussian-moment step**. Using g=2σ<sup>2</sup>-2C,

$$
e^{-q_z^2 g/2}=e^{-q_z^2\sigma^2}\,e^{q_z^2 C(\mathbf{R}'-\mathbf{R})}.
$$

Shift variables to <b>R</b>'-<b>R</b> and the centre of mass. The centre-of-mass integral gives the illuminated area <i>A</i>. What remains is PRB (2.26):

$$
S(\mathbf{q})\propto\frac{e^{-q_z^2\sigma^2}}{q_z^2}\int d^2R\,e^{q_z^2 C(\mathbf{R})}\,e^{-i\mathbf{q}_\parallel\cdot\mathbf{R}}.
$$

(PRB’s <i>S</i> is the cross section per unit area per (Nb)<sup>2</sup>.)

## 5.2 Split: e<sup>q<sub>z</sub><sup>2</sup> C</sup>=1+(e<sup>q<sub>z</sub><sup>2</sup> C</sup>-1)

Write e<sup>q<sub>z</sub><sup>2</sup> C(<b>R</b>)</sup>=1+F(<b>R</b>) with F=e<sup>q<sub>z</sub><sup>2</sup> C</sup>-1. Then S=S<sub>spec</sub>+S<sub>diff</sub>.

**If C(R)→ 0 as R→∞** (finite cutoff <i>ξ</i>; next subsection), then F(∞)=0, so <i>F</i> is integrable, while the 1 is not:

$$
\int d^2R\,1\cdot e^{-i\mathbf{q}_\parallel\cdot\mathbf{R}}=(2\pi)^2\delta(q_x)\delta(q_y).
$$

**Specular (PRB (2.28a)):**

$$
S_{\mathrm{spec}}(\mathbf{q})\propto\frac{e^{-q_z^2\sigma^2}}{q_z^2}\,(2\pi)^2\delta(q_x)\delta(q_y).
$$

The <i>δ</i>-functions are the specular ridge. The factor e<sup>-q<sub>z</sub><sup>2</sup>σ<sup>2</sup></sup> is a **Debye–Waller** reduction of the smooth-surface reflectivity (PRB: this multiplies the Fresnel/Porod q<sub>z</sub><sup>-4</sup> after converting flux to reflectivity). Physically: uncorrelated height noise randomises the phase q<sub>z</sub> z and kills coherent addition along the specular.

**Diffuse (PRB (2.28b), isotropic):**

$$
S_{\mathrm{diff}}(\mathbf{q})\propto\frac{e^{-q_z^2\sigma^2}}{q_z^2}\int_0^\infty R\,dR\,J_0(q_\parallel R)\bigl(e^{q_z^2 C(R)}-1\bigr).
$$

The -1 subtracted the specular piece. F(R)→ 0 at large <i>R</i>, so the diffuse is a smooth function of q<sub>∥</sub>, not a delta.

**If there is no cutoff**, C(R) does not tend to 0 (or g(R) diverges), F(∞)≠ 0, and **there is no <i>δ</i>-function specular**. All intensity is diffuse (PRB Sec. II.B). Liquids without an IR cutoff are the textbook case (chapter 6).

Numeric: `code/08_specular_split.py`.

## 5.3 Self-affine C(R) with cutoff

PRB (2.6): ideal self-affine g(R)=A R<sup>2h</sup> with 0<h<1. That <i>g</i> diverges as R→∞, so they introduce a saturation (2.9) / (2.25):

$$
C(R)=\sigma^2\exp\bigl[-(R/\xi)^{2h}\bigr],\qquad
g(R)=2\sigma^2\bigl(1-e^{-(R/\xi)^{2h}}\bigr).
$$

**Symbols.** <i>σ</i>: rms roughness (vertical). <i>ξ</i>: **lateral cutoff** (beyond <i>ξ</i> the surface looks like a finite-amplitude hill, not an unbounded random walk). <i>h</i>: **Hurst exponent** (PRB’s <i>h</i>; also called roughness exponent <i>α</i>). Small <i>h</i>: jagged (high-frequency PSD). h→ 1: rolling hills.

**Surface fractal dimension** (PRB (2.8)): D<sub>s</sub>=3-h. Self-*affine* is not self-*similar*: <i>z</i> scales differently from x,y. At scales ≪ R<sub>0</sub>∼ξ(σ/ξ)<sup>1/(1-h)</sup> it looks fractal; at scales ≫ξ it looks flat in the sense that C→ 0.

**Limiting cases of S<sub>diff</sub>.**

- **Small q<sub>z</sub><sup>2</sup>σ<sup>2</sup>:** e<sup>q<sub>z</sub><sup>2</sup> C</sup>-1≈ q<sub>z</sub><sup>2</sup> C, so S<sub>diff</sub>∝∫ R dR J<sub>0</sub>(q<sub>∥</sub> R)C(R), i.e. the Hankel transform of <i>C</i>, i.e. the PSD (PRB (4.43)). Transverse scans at small q<sub>z</sub> measure <i>C</i> almost directly.
- **Large q<sub>z</sub>, no cutoff (2.6):** PRB (2.22) S(q<sub>∥</sub>=0)∝ q<sub>z</sub><sup>-2-2/h</sup> (power of q<sub>z</sub> set by <i>h</i>).
- **Born specular** always e<sup>-q<sub>z</sub><sup>2</sup>σ<sup>2</sup></sup> times the smooth reflectivity **if** a cutoff exists.

Generate a field, measure <i>C</i>, compare to the formula: `code/07_self_affine_surface.py`.

## 5.4 What is identifiable from which scan

| You measure | You mainly constrain |
| --- | --- |
| Specular ∣R(q<sub>z</sub>)∣<sup>2</sup> | <i>σ</i> (and the mean density profile / θ<sub>c</sub>) |
| Transverse / rocking at several q<sub>z</sub> | <i>h</i> and <i>ξ</i> (shape of <i>C</i>) via S<sub>diff</sub>(q<sub>∥</sub>) |
| Only specular | **not** h,ξ (they hide in the subtracted diffuse) |

PRB Sec. V: Pyrex fit used specular + near-specular diffuse + rocking together: σ=7.6 Å, h=0.2, ξ=7000 Å — an illustration, not your sample.
