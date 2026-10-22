# 1. Prerequisites

We will add waves, then add them with different phases, then integrate those phases over a surface. That is all scattering maths is. This chapter builds the four tools used constantly later.

## 1.1 Complex numbers as 2D arrows (phasors)

A **complex number** <i>z</i> is an ordered pair of real numbers (x,y), written z=x+iy, where <i>i</i> is a bookkeeping symbol with the single rule

$$
i^2=-1.
$$

Call x=Re z the **real part** and y=Im z the **imaginary part**. Plot <i>z</i> as an arrow from the origin to (x,y). The **modulus** (length) and **argument** (angle from the positive <i>x</i>-axis) are

$$
\lvert z\rvert=\sqrt{x^2+y^2},\qquad \arg z=\mathrm{atan2}(y,x).
$$

The **complex conjugate** is z<sup>∗</sup>=x-iy. Then ∣z∣<sup>2</sup>=z z<sup>∗</sup>. Intensities in physics are always of the form ∣amplitude∣<sup>2</sup>, never the amplitude itself.

**Why bother?** A travelling wave with amplitude <i>A</i> (real) and phase <i>φ</i> (real, radians) can be written

$$
A\cos(\omega t - \mathbf{k}\cdot\mathbf{r}+\varphi_0)=\mathrm{Re}\Bigl(A\,e^{i\varphi_0}\,e^{i(\omega t-\mathbf{k}\cdot\mathbf{r})}\Bigr).
$$

The complex number A e<sup>iφ<sub>0</sub></sup> is the **phasor**. Adding waves = adding arrows. Two arrows of equal length that point opposite ways cancel (destructive interference). Two that point the same way add (constructive interference).

Check: e<sup>iπ</sup>=-1, e<sup>iπ/2</sup>=i, ∣e<sup>iθ</sup>∣=1 for real <i>θ</i>. Script: `code/01_phasors.py`.

## 1.2 Euler’s formula, derived

The exponential of a complex number is defined by the same power series as the real exponential,

$$
e^z=\sum_{n=0}^\infty\frac{z^n}{n!}.
$$

Set z=iθ with <i>θ</i> real, separate even and odd powers, and use i<sup>2</sup>=-1, i<sup>3</sup>=-i, i<sup>4</sup>=1:

$$
e^{i\theta}=\sum_{k=0}^\infty\frac{(-1)^k\theta^{2k}}{(2k)!}+i\sum_{k=0}^\infty\frac{(-1)^k\theta^{2k+1}}{(2k+1)!}=\cos\theta+i\sin\theta.
$$

That is **Euler’s formula**. Inversion:

$$
\cos\theta=\frac{e^{i\theta}+e^{-i\theta}}{2},\qquad\sin\theta=\frac{e^{i\theta}-e^{-i\theta}}{2i}.
$$

A product of unit-modulus complex numbers **adds phases**:

$$
e^{i\alpha}e^{i\beta}=e^{i(\alpha+\beta)}.
$$

Scattering: each volume element contributes a phasor e<sup>-i<b>q</b>·<b>r</b></sup> (chapter 2). The detector adds them.

## 1.3 Vectors and the dot product

A 3-vector <b>a</b>=(a<sub>x</sub>,a<sub>y</sub>,a<sub>z</sub>) is an arrow in space. The **dot product** of <b>a</b> and <b>b</b> is

$$
\mathbf{a}\cdot\mathbf{b}=a_x b_x+a_y b_y+a_z b_z=\lvert\mathbf{a}\rvert\lvert\mathbf{b}\rvert\cos\psi,
$$

where <i>ψ</i> is the angle between them. It is a single real number.

The **wave vector** <b>k</b> of a plane wave points in the propagation direction and has length k=2π/λ, where <i>λ</i> is the wavelength (same units as length; we use Å). The phase of the wave at position <b>r</b> is <b>k</b>·<b>r</b>.

The **wave-vector transfer** used throughout both papers is

$$
\mathbf{q}=\mathbf{k}_1-\mathbf{k}_0,
$$

where <b>k</b><sub>0</sub> is the incident wave vector and <b>k</b><sub>1</sub> the scattered one (Physica Fig. 1; PRB Fig. 1). Elastic scattering: |<b>k</b><sub>0</sub>|=|<b>k</b><sub>1</sub>|=k. If <i>α</i> and <i>β</i> are **grazing** angles (from the surface, not from the normal),

$$
q_x=k(\cos\beta-\cos\alpha),\qquad q_z=k(\sin\alpha+\sin\beta).
$$

(We take the scattering plane as xz, surface as xy.) Specular: α=β ⇒ q<sub>x</sub>=0, q<sub>z</sub>=2k sinα.

## 1.4 The Dirac delta as a “unit spike”

The **Dirac delta** δ(x) is not a function in the calculus-I sense. It is defined by how it sits inside integrals: for a smooth test function <i>f</i>,

$$
\int_{-\infty}^{\infty} dx\,\delta(x-x_0)\,f(x)=f(x_0).
$$

Intuition: a spike of width <i>ε</i> and height 1/ε at x<sub>0</sub>, then ε→ 0. Area stays 1.

In <i>d</i> dimensions, δ(<b>q</b>)=δ(q<sub>x</sub>)δ(q<sub>y</sub>)⋯. Units: δ(x) has units 1/length if <i>x</i> is a length.

The representation we need (proved after Fourier transforms exist; take as a working identity for now) is

$$
\int_{-\infty}^{\infty} dx\,e^{-iqx}=2\pi\,\delta(q).
$$

In 2D: ∫ d<sup>2</sup>R e<sup>-i<b>q</b><sub>∥</sub>·<b>R</b></sup>=(2π)<sup>2</sup>δ(<b>q</b><sub>∥</sub>). A **perfectly flat, infinitely wide** surface therefore scatters only when <b>q</b><sub>∥</sub>=<b>0</b> — the specular ridge.

## 1.5 Area integrals and polar coordinates

A surface integral of a scalar f(x,y) over the plane is

$$
\int_{-\infty}^{\infty}dx\int_{-\infty}^{\infty}dy\,f(x,y)=\int d^2R\,f(\mathbf{R}).
$$

If <i>f</i> depends only on the radial distance R=√(x<sup>2</sup>+y<sup>2</sup>) (**isotropy**), switch to polar coordinates x=R cosθ, y=R sinθ. The area element is dx dy=R dR dθ, with R≥ 0 and θ∈[0,2π):

$$
\int d^2R\,f(R)=\int_0^{2\pi}d\theta\int_0^{\infty} R\,dR\,f(R)=2\pi\int_0^{\infty} R\,dR\,f(R).
$$

The extra <i>R</i> is the circumference factor: a ring of radius <i>R</i> and thickness dR has area 2π R dR.

Chapter 4: the angular <i>θ</i> integral of e<sup>-i q R cosθ</sup> **defines** the Bessel function J<sub>0</sub>. Do not skip this change of variables.

---

**Self-check.** (i) Compute ∣1+i∣ and arg(1+i). (ii) Why is ∣e<sup>-i<b>q</b>·<b>r</b></sup>∣=1? (iii) If a detector integrates a spike δ(q<sub>x</sub>) with a resolution window of width <i>w</i>, what does it record? (The area of the window times the spike: a finite peak of area 1, height ∼ 1/w.)
